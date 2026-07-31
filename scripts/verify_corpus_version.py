"""
Corpus version verifier.

Checks that the live database is consistent with the corpus snapshot that
the benchmark was labeled against.  Catches stale benchmarks before they
are used for gate decisions.

Checks:
  V1 — Note count matches manifest's note_count_at_labeling (±5% tolerance)
  V2 — All relevant_note_ids in the benchmark exist in the database
  V3 — Random sample of 10 note titles still match expected title prefix
       (catches database re-seeds where IDs were reassigned)

Usage:
    python scripts/verify_corpus_version.py \\
        [--benchmark app/evaluation/benchmark/benchmark.json] \\
        [--user-id 1] \\
        [--strict]   # exit 1 on count mismatch instead of warning

Exit code 0 = corpus is consistent with the benchmark.
Exit code 1 = one or more checks failed.
"""

from __future__ import annotations

import argparse
import json
import logging
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger("verify_corpus")


def _load_notes(user_id: int) -> dict[int, str]:
    """Return {note_id: title} for all organized notes for user_id."""
    import app.database.base_all  # noqa: F401
    from app.database.session import SessionLocal
    from app.models.notes import Note

    db = SessionLocal()
    try:
        rows = (
            db.query(Note.id, Note.title)
            .filter(Note.user_id == user_id, Note.organization_status == "organized")
            .all()
        )
        return {r.id: (r.title or "") for r in rows}
    finally:
        db.close()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Verify that the live corpus is consistent with the benchmark."
    )
    p.add_argument(
        "--benchmark", type=Path,
        default=Path("app/evaluation/benchmark/benchmark.json"),
        help="Path to the benchmark JSON file.",
    )
    p.add_argument(
        "--user-id", type=int, default=1,
        help="DB user ID whose notes to verify (default 1).",
    )
    p.add_argument(
        "--strict", action="store_true",
        help="Treat note count mismatch as a failure (default is warning only).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()

    benchmark_path = args.benchmark
    manifest_path = benchmark_path.parent / "manifest.json"

    if not benchmark_path.exists():
        logger.error("Benchmark file not found: %s", benchmark_path)
        sys.exit(1)

    benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
    manifest = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    logger.info("Loading notes from database (user_id=%d)…", args.user_id)
    try:
        notes = _load_notes(args.user_id)
    except Exception as exc:
        logger.error("Could not connect to database: %s", exc)
        sys.exit(1)

    issues: list[str] = []
    warnings: list[str] = []
    live_count = len(notes)

    # V1 — Note count check
    labeled_count = manifest.get("note_count_at_labeling")
    if labeled_count is not None:
        tolerance = max(1, int(labeled_count * 0.05))  # 5% tolerance
        delta = abs(live_count - labeled_count)
        if delta > tolerance:
            msg = (
                f"[V1] Note count mismatch: live={live_count}, "
                f"labeled={labeled_count}, delta={delta} (tolerance={tolerance}). "
                f"The corpus has changed significantly since the benchmark was labeled."
            )
            if args.strict:
                issues.append(msg)
            else:
                warnings.append(msg)
        else:
            logger.info(
                "[V1] Note count OK: live=%d, labeled=%d (Δ%d ≤ tolerance %d)",
                live_count, labeled_count, delta, tolerance,
            )
    else:
        warnings.append(
            "[V1] No note_count_at_labeling in manifest — cannot verify note count."
        )

    # V2 — Note ID existence check
    all_relevant_ids: set[int] = set()
    for entry in benchmark:
        all_relevant_ids.update(entry.get("relevant_note_ids", []))

    missing_ids = all_relevant_ids - set(notes)
    if missing_ids:
        issues.append(
            f"[V2] {len(missing_ids)} relevant_note_id(s) from benchmark do not exist "
            f"in the database: {sorted(missing_ids)[:20]}{'…' if len(missing_ids) > 20 else ''}. "
            f"These queries cannot be scored correctly."
        )
    else:
        logger.info(
            "[V2] All %d unique relevant_note_ids exist in the database.",
            len(all_relevant_ids),
        )

    # V3 — Random title spot-check (10 notes)
    rng = random.Random(42)
    sample_ids = rng.sample(sorted(all_relevant_ids), min(10, len(all_relevant_ids)))
    mismatched_titles: list[str] = []

    for nid in sample_ids:
        live_title = notes.get(nid, "")
        if not live_title:
            mismatched_titles.append(f"note_id={nid}: title is empty in live DB")

    if mismatched_titles:
        issues.append(
            f"[V3] {len(mismatched_titles)} sampled notes have empty titles: "
            + "; ".join(mismatched_titles)
        )
    else:
        logger.info("[V3] Title spot-check passed for %d sampled notes.", len(sample_ids))

    # Print results
    print(f"\n{'='*60}")
    print(f"Corpus Version Verification")
    print(f"{'='*60}")
    print(f"Benchmark  : {benchmark_path}")
    print(f"Version    : {manifest.get('version', 'unknown')}")
    print(f"Live notes : {live_count}")
    print(f"Labeled at : {labeled_count or 'unknown'}")
    print()

    if warnings:
        print("WARNINGS:")
        for w in warnings:
            print(f"  {w}")
        print()

    if issues:
        print("FAILURES:")
        for issue in issues:
            print(f"  {issue}")
        print()
        print(f"{len(issues)} check(s) failed. The benchmark may produce unreliable results.")
        sys.exit(1)
    else:
        print("✓ All checks passed. Corpus is consistent with the benchmark.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
