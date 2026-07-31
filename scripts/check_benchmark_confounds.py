"""
Benchmark confound detector.

Checks for three classes of measurement confounds that invalidate
benchmark gate decisions:

  C1 — Pool-latency consistency
       If the RERANK strategy reports average latency within 50ms of HYBRID,
       the cross-encoder likely did not run (the expanded candidate pool alone
       looks identical to full reranking from a metrics perspective).
       Evidence: Sprint 2-B — RERANK showed 9ms overhead vs HYBRID when the
       env-var RERANKING_ENABLED=true was not propagated to the Windows
       Python binary.

  C2 — Note ID validity
       Every relevant_note_id in the benchmark must exist in the database.
       Stale IDs silently make queries unscoreable.

  C3 — Strategy result identity
       If RERANK retrieved_note_ids are identical to HYBRID across every
       benchmark query, reranking produced no reordering effect — the
       cross-encoder may be disabled or returning early.

Usage:
    python scripts/check_benchmark_confounds.py \\
        --results evaluation_results/sprint2b_fresh/evaluation_results.csv \\
        --benchmark app/evaluation/benchmark/benchmark.json \\
        [--user-id 1]

Exit code 0 = no confounds detected.
Exit code 1 = one or more confounds detected (print details to stdout).
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("confounds")


# ---------------------------------------------------------------------------
# Confound checks
# ---------------------------------------------------------------------------

def check_pool_latency_consistency(results: list[dict]) -> list[str]:
    """
    C1: RERANK avg latency within 50ms of HYBRID → cross-encoder likely not running.

    With inference enabled, the cross-encoder adds ~250–400ms on 20 candidates
    (CPU).  An overhead of < 50ms indicates a pass-through (model not loaded,
    RERANKING_ENABLED=False, or early return in RerankingService.rerank()).
    """
    issues: list[str] = []

    latency_by_strategy: dict[str, list[float]] = {}
    for row in results:
        s = row.get("strategy", "").lower()
        try:
            lat = float(row.get("latency_ms", 0))
        except (ValueError, TypeError):
            continue
        latency_by_strategy.setdefault(s, []).append(lat)

    hybrid_lats = latency_by_strategy.get("hybrid", [])
    rerank_lats = latency_by_strategy.get("rerank", [])

    if not hybrid_lats or not rerank_lats:
        return issues  # can't compare — not both present

    hybrid_avg = sum(hybrid_lats) / len(hybrid_lats)
    rerank_avg = sum(rerank_lats) / len(rerank_lats)
    delta = rerank_avg - hybrid_avg

    if delta < 50.0:
        issues.append(
            f"[C1] RERANK avg latency ({rerank_avg:.1f}ms) is only "
            f"{delta:.1f}ms above HYBRID ({hybrid_avg:.1f}ms). "
            f"Cross-encoder inference typically adds ≥ 250ms on 20 candidates. "
            f"Verify RERANKING_ENABLED=True was active and the model actually loaded."
        )
    return issues


def check_note_id_validity(benchmark: list[dict], db_note_ids: set[int]) -> list[str]:
    """
    C2: All relevant_note_ids in the benchmark must exist in the database.
    """
    issues: list[str] = []
    for entry in benchmark:
        for nid in entry.get("relevant_note_ids", []):
            if nid not in db_note_ids:
                issues.append(
                    f"[C2] Benchmark query {entry['id']!r} references note_id={nid} "
                    f"which does not exist in the database. "
                    f"The benchmark may be stale or the database was re-seeded."
                )
    return issues


def check_strategy_identity(results: list[dict]) -> list[str]:
    """
    C3: If RERANK and HYBRID retrieved_note_ids are identical across all
    queries, the reranker produced no effect.
    """
    issues: list[str] = []

    by_query_strategy: dict[tuple[str, str], str] = {}
    for row in results:
        key = (row.get("benchmark_id", ""), row.get("strategy", "").lower())
        by_query_strategy[key] = row.get("retrieved_note_ids", "")

    query_ids = sorted({k[0] for k in by_query_strategy})
    if not query_ids:
        return issues

    identical_count = 0
    for qid in query_ids:
        hybrid_ids = by_query_strategy.get((qid, "hybrid"), "")
        rerank_ids = by_query_strategy.get((qid, "rerank"), "")
        if hybrid_ids and rerank_ids and hybrid_ids == rerank_ids:
            identical_count += 1

    if identical_count == len(query_ids):
        issues.append(
            f"[C3] RERANK retrieved_note_ids are identical to HYBRID across all "
            f"{identical_count} queries. The reranker produced no reordering. "
            f"This is expected when RERANKING_ENABLED=False. "
            f"If reranking was supposed to be active, verify the model loaded correctly."
        )
    elif identical_count >= len(query_ids) * 0.9:
        issues.append(
            f"[C3] RERANK retrieved_note_ids match HYBRID on {identical_count}/{len(query_ids)} "
            f"queries (>{100 * identical_count // len(query_ids)}%). "
            f"Very low reranking effect — check that inference is executing."
        )
    return issues


def check_gates(results: list[dict], gates: dict) -> list[str]:
    """
    Check that strategy metrics are above the regression floor values in gates.json.
    """
    issues: list[str] = []
    strategy_gates = gates.get("strategies", {})

    latency_by_strategy: dict[str, list[float]] = {}
    rr_by_strategy: dict[str, list[float]] = {}
    hit_by_strategy: dict[str, list[float]] = {}

    for row in results:
        s = row.get("strategy", "").lower()
        try:
            lat = float(row.get("latency_ms", 0))
            rr = float(row.get("reciprocal_rank", 0))
            hit = 1.0 if row.get("hit") == "True" else 0.0
        except (ValueError, TypeError):
            continue
        latency_by_strategy.setdefault(s, []).append(lat)
        rr_by_strategy.setdefault(s, []).append(rr)
        hit_by_strategy.setdefault(s, []).append(hit)

    for strategy_key, gate in strategy_gates.items():
        s = strategy_key.lower()
        lats = latency_by_strategy.get(s, [])
        rrs = rr_by_strategy.get(s, [])
        hits = hit_by_strategy.get(s, [])

        if not rrs:
            continue

        mrr = sum(rrs) / len(rrs)
        hit_rate = sum(hits) / len(hits)
        avg_lat = sum(lats) / len(lats) if lats else 0.0

        mrr_floor = gate.get("mrr_floor")
        hit_floor = gate.get("hit_rate_floor")
        lat_ceil = gate.get("avg_latency_ms_ceiling")

        if mrr_floor is not None and mrr < mrr_floor:
            issues.append(
                f"[GATE] {strategy_key} MRR={mrr:.4f} < floor={mrr_floor:.4f} — REGRESSION"
            )
        if hit_floor is not None and hit_rate < hit_floor:
            issues.append(
                f"[GATE] {strategy_key} HitRate={hit_rate:.4f} < floor={hit_floor:.4f} — REGRESSION"
            )
        if lat_ceil is not None and avg_lat > lat_ceil:
            issues.append(
                f"[GATE] {strategy_key} AvgLatency={avg_lat:.1f}ms > ceiling={lat_ceil:.1f}ms"
            )
    return issues


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _load_benchmark(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _load_results(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _load_gates(gates_path: Path) -> dict:
    if not gates_path.exists():
        return {}
    return json.loads(gates_path.read_text(encoding="utf-8"))


def _load_db_note_ids(user_id: int) -> set[int]:
    try:
        import app.database.base_all  # noqa: F401
        from app.database.session import SessionLocal
        from app.models.notes import Note
        db = SessionLocal()
        try:
            rows = db.query(Note.id).filter(Note.user_id == user_id).all()
            return {r.id for r in rows}
        finally:
            db.close()
    except Exception as exc:
        logger.warning("Could not load note IDs from DB: %s (skipping C2 check)", exc)
        return set()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Detect benchmark measurement confounds."
    )
    p.add_argument(
        "--results", type=Path,
        default=Path("evaluation_results/evaluation_results.csv"),
        help="Path to evaluation_results.csv from a benchmark run.",
    )
    p.add_argument(
        "--benchmark", type=Path,
        default=Path("app/evaluation/benchmark/benchmark.json"),
        help="Path to the benchmark JSON file.",
    )
    p.add_argument(
        "--gates", type=Path,
        default=Path("evaluation_results/gates.json"),
        help="Path to gates.json for regression floor checking.",
    )
    p.add_argument(
        "--user-id", type=int, default=1,
        help="DB user ID for note ID existence check (default 1).",
    )
    p.add_argument(
        "--skip-db", action="store_true",
        help="Skip the C2 database note-ID existence check.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    results = _load_results(args.results)
    benchmark = _load_benchmark(args.benchmark)
    gates = _load_gates(args.gates)

    if not results:
        logger.warning("No results found at %s — skipping latency/identity checks.", args.results)

    all_issues: list[str] = []

    # C1: Pool-latency consistency
    all_issues.extend(check_pool_latency_consistency(results))

    # C2: Note ID validity
    if not args.skip_db and benchmark:
        db_note_ids = _load_db_note_ids(args.user_id)
        if db_note_ids:
            all_issues.extend(check_note_id_validity(benchmark, db_note_ids))

    # C3: Strategy identity
    if results:
        all_issues.extend(check_strategy_identity(results))

    # Gate check
    if results and gates:
        all_issues.extend(check_gates(results, gates))

    if all_issues:
        print(f"\n{'='*70}")
        print("BENCHMARK CONFOUNDS DETECTED")
        print(f"{'='*70}")
        for issue in all_issues:
            print(f"\n  {issue}")
        print(f"\n{'='*70}")
        print(f"\n{len(all_issues)} confound(s) detected. Review before using this run for gate decisions.\n")
        sys.exit(1)
    else:
        print("\n✓ No confounds detected. Benchmark run is clean.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
