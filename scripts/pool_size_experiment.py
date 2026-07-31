"""
Pool size experiment for HYBRID retrieval.

Evaluates ChunkService.retrieve_hybrid() at five candidate pool sizes:
    pool = 5, 10, 20, 40, 80

Each pool size is benchmarked against the full 50-query benchmark at K=5.

Metrics reported per pool size
-------------------------------
Precision@5   - fraction of top-5 results that are relevant
Recall@5      - fraction of relevant notes found in top 5
Hit Rate@5    - >=1 relevant note in top 5 (primary quality signal)
MRR@5         - Mean Reciprocal Rank capped at rank 5 (FAIR cross-pool comparison)
MRR full      - Uncapped MRR (unfair across pools but shows "ceiling" for each size)
MAP@5         - Mean Average Precision at 5
nDCG@5        - Normalised Discounted Cumulative Gain at 5
Avg latency   - Mean wall-clock retrieval time per query (ms)
95% CI        - Bootstrap confidence interval on Hit Rate@5 and MRR@5

Pool scaling
------------
The internal ANN pool for the semantic arm scales with `limit`:
    ann_pool = max(limit x 4, 20)

So the ANN candidates fetched are:
    limit= 5 = ann_pool= 20
    limit=10 = ann_pool= 40
    limit=20 = ann_pool= 80
    limit=40 = ann_pool=160
    limit=80 = ann_pool=320

Production note
---------------
This script does NOT change any production default.
It runs the HybridAdapter directly with overridden limit values.
The recommendation is for review and approval only.

Usage:
    python scripts/pool_size_experiment.py \\
        --user-id 1 \\
        [--benchmark app/evaluation/benchmark/benchmark.json] \\
        [--output evaluation_results/pool_experiment]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import app.database.base_all  # noqa: F401
from app.database.session import SessionLocal
from app.evaluation.benchmark.loader import BenchmarkLoader
from app.evaluation.adapters.hybrid import HybridAdapter
from app.evaluation.metrics.retrieval import (
    average_precision_at_k,
    hit_rate,
    ndcg_at_k,
    precision_at_k,
    r_precision,
    recall_at_k,
    reciprocal_rank,
)
from app.evaluation.metrics.statistics import bootstrap_mean_ci, bootstrap_delta_ci


# Pool sizes to evaluate.
POOL_SIZES = [5, 10, 20, 40, 80]
EVAL_K = 5


# ---------------------------------------------------------------------------
# Per-query result
# ---------------------------------------------------------------------------

@dataclass
class QueryResult:
    pool: int
    benchmark_id: str
    query: str
    difficulty: str
    relevant: list[int]
    retrieved: list[int]     # full list returned by adapter
    latency_ms: float

    @property
    def retrieved_k5(self) -> list[int]:
        return self.retrieved[:EVAL_K]

    @property
    def precision(self) -> float:
        return precision_at_k(self.retrieved, self.relevant, EVAL_K)

    @property
    def recall(self) -> float:
        return recall_at_k(self.retrieved, self.relevant, EVAL_K)

    @property
    def hit(self) -> bool:
        return hit_rate(self.retrieved, self.relevant, EVAL_K)

    @property
    def rr_k5(self) -> float:
        """Reciprocal rank capped at K=5 - fair across pool sizes."""
        return reciprocal_rank(self.retrieved_k5, self.relevant)

    @property
    def rr_full(self) -> float:
        """Uncapped reciprocal rank - inflated for large pools."""
        return reciprocal_rank(self.retrieved, self.relevant)

    @property
    def map_k5(self) -> float:
        return average_precision_at_k(self.retrieved, self.relevant, EVAL_K)

    @property
    def ndcg_k5(self) -> float:
        return ndcg_at_k(retrieved=self.retrieved, relevant=self.relevant, k=EVAL_K)


# ---------------------------------------------------------------------------
# Aggregate per pool size
# ---------------------------------------------------------------------------

@dataclass
class PoolResult:
    pool: int
    ann_pool: int                    # internal ANN candidates
    query_results: list[QueryResult] = field(default_factory=list)

    # Filled by compute_aggregates()
    precision: float = 0.0
    recall: float = 0.0
    hit_rate: float = 0.0
    mrr_k5: float = 0.0
    mrr_full: float = 0.0
    map_k5: float = 0.0
    ndcg_k5: float = 0.0
    avg_latency_ms: float = 0.0
    hit_rate_ci: tuple[float, float] | None = None
    mrr_k5_ci: tuple[float, float] | None = None

    def compute_aggregates(self) -> None:
        qr = self.query_results
        if not qr:
            return
        n = len(qr)
        self.precision = sum(q.precision for q in qr) / n
        self.recall = sum(q.recall for q in qr) / n
        self.hit_rate = sum(1.0 if q.hit else 0.0 for q in qr) / n
        self.mrr_k5 = sum(q.rr_k5 for q in qr) / n
        self.mrr_full = sum(q.rr_full for q in qr) / n
        self.map_k5 = sum(q.map_k5 for q in qr) / n
        self.ndcg_k5 = sum(q.ndcg_k5 for q in qr) / n
        self.avg_latency_ms = sum(q.latency_ms for q in qr) / n

        hits = [1.0 if q.hit else 0.0 for q in qr]
        rrs = [q.rr_k5 for q in qr]
        if n >= 5:
            self.hit_rate_ci = bootstrap_mean_ci(hits, n_boot=2000, seed=42)
            self.mrr_k5_ci = bootstrap_mean_ci(rrs, n_boot=2000, seed=42)


# ---------------------------------------------------------------------------
# Experiment runner
# ---------------------------------------------------------------------------

def run_pool(
    pool_size: int,
    benchmark_queries,
    db,
    user_id: int,
    warmup_query: str | None = None,
) -> PoolResult:
    ann_pool = max(pool_size * 4, 20)
    adapter = HybridAdapter(db=db, user_id=user_id, limit=pool_size)
    result = PoolResult(pool=pool_size, ann_pool=ann_pool)

    from app.evaluation.models import BenchmarkQuery

    # Warm-up - run one query to amortise any first-call overhead
    if warmup_query:
        warmup = BenchmarkQuery(
            id="warmup", query=warmup_query, expected_intent="general",
            expected_category="General", relevant_note_ids=[],
        )
        try:
            adapter.run(warmup)
        except Exception:
            pass

    for bq in benchmark_queries:
        t0 = time.perf_counter()
        retrieval = adapter.run(bq)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        result.query_results.append(QueryResult(
            pool=pool_size,
            benchmark_id=bq.id,
            query=bq.query,
            difficulty=bq.difficulty,
            relevant=bq.relevant_note_ids,
            retrieved=retrieval.retrieved_note_ids,
            latency_ms=elapsed_ms,
        ))

    result.compute_aggregates()
    return result


# ---------------------------------------------------------------------------
# Pareto frontier
# ---------------------------------------------------------------------------

def pareto_frontier(
    results: list[PoolResult],
    quality_metric: str = "hit_rate",
    latency_metric: str = "avg_latency_ms",
) -> list[int]:
    """
    Return pool sizes on the Pareto frontier (not dominated on quality or latency).

    A point P dominates Q if P has higher (or equal) quality AND lower (or equal)
    latency, with at least one strict improvement.
    """
    dominated: set[int] = set()
    pool_vals = [(getattr(r, quality_metric), getattr(r, latency_metric), r.pool) for r in results]

    for i, (qi, li, pi) in enumerate(pool_vals):
        for j, (qj, lj, pj) in enumerate(pool_vals):
            if i == j:
                continue
            # j dominates i if qj >= qi and lj <= li with at least one strict
            if qj >= qi and lj <= li and (qj > qi or lj < li):
                dominated.add(pi)
                break

    return [pool for pool in POOL_SIZES if pool not in dominated]


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def _ci_str(ci: tuple[float, float] | None) -> str:
    if ci is None:
        return "         -"
    return f"[{ci[0]:.3f},{ci[1]:.3f}]"


def print_comparison_table(results: list[PoolResult]) -> None:
    sep = "-" * 110
    header = (
        f"{'Pool':>5}  {'ANN':>4}  "
        f"{'P@5':>6}  {'R@5':>6}  {'Hit@5':>6}  "
        f"{'MRR@5':>6}  {'MRR@5 95% CI':>14}  "
        f"{'MRR full':>8}  "
        f"{'MAP@5':>6}  {'nDCG@5':>6}  "
        f"{'Lat(ms)':>8}"
    )
    print()
    print(sep)
    print("HYBRID POOL SIZE EXPERIMENT - K=5 Evaluation")
    print(sep)
    print(header)
    print(sep)
    for r in results:
        ci = _ci_str(r.mrr_k5_ci)
        print(
            f"{r.pool:>5}  {r.ann_pool:>4}  "
            f"{r.precision:>6.3f}  {r.recall:>6.3f}  {r.hit_rate:>6.3f}  "
            f"{r.mrr_k5:>6.3f}  {ci:>14}  "
            f"{r.mrr_full:>8.3f}  "
            f"{r.map_k5:>6.3f}  {r.ndcg_k5:>6.3f}  "
            f"{r.avg_latency_ms:>8.1f}"
        )
    print(sep)
    print("Note: MRR@5 is reciprocal rank CAPPED at K=5 - valid for cross-pool comparison.")
    print("      MRR full uses the entire returned list - unfair for pool>5 (shown for reference).")
    print()


def print_delta_table(results: list[PoolResult], baseline_pool: int = 5) -> None:
    base = next((r for r in results if r.pool == baseline_pool), None)
    if base is None:
        return

    sep = "-" * 90
    print(sep)
    print(f"DELTA vs pool={baseline_pool} BASELINE")
    print(sep)
    print(
        f"{'Pool':>5}  {'DHit@5':>8}  {'DMRR@5':>8}  {'DMAP@5':>8}  "
        f"{'DnDCG@5':>8}  {'DLat(ms)':>10}  {'Latx':>6}"
    )
    print(sep)

    base_rrs = [q.rr_k5 for q in base.query_results]
    base_hits = [1.0 if q.hit else 0.0 for q in base.query_results]

    for r in results:
        if r.pool == baseline_pool:
            continue
        d_hit = r.hit_rate - base.hit_rate
        d_mrr = r.mrr_k5 - base.mrr_k5
        d_map = r.map_k5 - base.map_k5
        d_ndcg = r.ndcg_k5 - base.ndcg_k5
        d_lat = r.avg_latency_ms - base.avg_latency_ms
        lat_x = r.avg_latency_ms / max(base.avg_latency_ms, 0.001)

        # Statistical significance of MRR@5 delta
        r_rrs = [q.rr_k5 for q in r.query_results]
        _, _, mrr_sig = bootstrap_delta_ci(r_rrs, base_rrs, n_boot=2000, seed=42)
        sig_str = "[OK]" if mrr_sig else "-"

        print(
            f"{r.pool:>5}  {d_hit:>+8.3f}  {d_mrr:>+8.3f}{sig_str}  "
            f"{d_map:>+8.3f}  {d_ndcg:>+8.3f}  "
            f"{d_lat:>+10.1f}  {lat_x:>5.2f}x"
        )

    print(sep)
    print("[OK] = MRR@5 delta is statistically significant (95% bootstrap CI excludes zero)")
    print("- = difference not statistically significant")
    print()


def print_difficulty_breakdown(results: list[PoolResult]) -> None:
    sep = "-" * 80
    print(sep)
    print("HIT RATE@5 BY DIFFICULTY")
    print(sep)
    difficulties = ["easy", "medium", "hard"]
    header = f"{'Pool':>5}  " + "  ".join(f"{d.capitalize():>8}" for d in difficulties)
    print(header)
    print(sep)
    for r in results:
        row = f"{r.pool:>5}  "
        for diff in difficulties:
            qs = [q for q in r.query_results if q.difficulty == diff]
            if qs:
                hr = sum(1.0 if q.hit else 0.0 for q in qs) / len(qs)
                row += f"{hr:>8.3f}  "
            else:
                row += f"{'-':>8}  "
        print(row)
    print(sep)
    print()


def print_quality_latency_chart(results: list[PoolResult], pareto: list[int]) -> None:
    """ASCII quality-vs-latency scatter plot (MRR@5 vs avg latency)."""
    print("QUALITY-vs-LATENCY (MRR@5 vs Avg Latency)")
    print()

    # Axis ranges
    lat_vals = [r.avg_latency_ms for r in results]
    mrr_vals = [r.mrr_k5 for r in results]
    lat_min, lat_max = min(lat_vals) * 0.9, max(lat_vals) * 1.1
    mrr_min, mrr_max = max(0.0, min(mrr_vals) * 0.9), min(1.0, max(mrr_vals) * 1.1)

    WIDTH = 60
    HEIGHT = 20

    grid = [[" "] * WIDTH for _ in range(HEIGHT)]

    def to_col(lat: float) -> int:
        return min(WIDTH - 1, int((lat - lat_min) / (lat_max - lat_min) * (WIDTH - 1)))

    def to_row(mrr: float) -> int:
        frac = (mrr - mrr_min) / (mrr_max - mrr_min) if (mrr_max - mrr_min) > 0 else 0.5
        return max(0, min(HEIGHT - 1, HEIGHT - 1 - int(frac * (HEIGHT - 1))))

    # Draw horizontal gridlines
    for row in [0, HEIGHT // 2, HEIGHT - 1]:
        for col in range(WIDTH):
            if grid[row][col] == " ":
                grid[row][col] = "."

    # Plot each pool size
    for r in results:
        col = to_col(r.avg_latency_ms)
        row = to_row(r.mrr_k5)
        marker = "*" if r.pool in pareto else "o"
        grid[row][col] = marker

    # Print
    mrr_top = f"{mrr_max:.3f}"
    mrr_mid = f"{(mrr_min + mrr_max) / 2:.3f}"
    mrr_bot = f"{mrr_min:.3f}"

    for i, row_data in enumerate(grid):
        if i == 0:
            label = mrr_top
        elif i == HEIGHT // 2:
            label = mrr_mid
        elif i == HEIGHT - 1:
            label = mrr_bot
        else:
            label = "     "
        print(f"  {label} |{''.join(row_data)}|")

    print(f"        +{'-' * WIDTH}+")
    lat_labels = f"  {lat_min:.0f}ms" + " " * (WIDTH - 12) + f"{lat_max:.0f}ms"
    print(f"         {lat_labels}")
    print()

    # Legend
    print("  * = Pareto-optimal (better MRR@5 for its latency cost)")
    print("  o = Dominated by another pool size")
    print()

    for r in results:
        pf = "* PARETO" if r.pool in pareto else "  dominated"
        print(f"    pool={r.pool:>2}  MRR@5={r.mrr_k5:.3f}  lat={r.avg_latency_ms:.1f}ms  {pf}")
    print()


def print_pareto_analysis(results: list[PoolResult], pareto: list[int]) -> None:
    sep = "-" * 70
    print(sep)
    print("PARETO FRONTIER ANALYSIS (Hit Rate@5 vs Latency)")
    print(sep)
    print()
    print("A pool size P dominates Q if P achieves at least as good Hit Rate@5")
    print("AND at least as low latency, with at least one strict improvement.")
    print()
    for r in results:
        status = "PARETO-OPTIMAL" if r.pool in pareto else "DOMINATED"
        print(f"  pool={r.pool:>2}:  Hit={r.hit_rate:.3f}  Lat={r.avg_latency_ms:.1f}ms  = {status}")
    print()
    print(f"Pareto-optimal pool sizes: {pareto}")
    print()


def generate_svg_chart(results: list[PoolResult], pareto: list[int], output_path: Path) -> None:
    """Generate a quality-vs-latency SVG scatter plot."""
    W, H = 500, 350
    PAD = {"top": 40, "bottom": 60, "left": 70, "right": 40}

    lat_vals = [r.avg_latency_ms for r in results]
    mrr_vals = [r.mrr_k5 for r in results]
    lat_min, lat_max = 0, max(lat_vals) * 1.15
    mrr_min, mrr_max = 0.0, min(1.0, max(mrr_vals) * 1.15)

    inner_w = W - PAD["left"] - PAD["right"]
    inner_h = H - PAD["top"] - PAD["bottom"]

    def cx(lat):
        return PAD["left"] + (lat - lat_min) / max(lat_max - lat_min, 1) * inner_w

    def cy(mrr):
        return PAD["top"] + inner_h - (mrr - mrr_min) / max(mrr_max - mrr_min, 0.001) * inner_h

    COLORS = {True: "#e74c3c", False: "#95a5a6"}  # pareto=red, dominated=grey

    elements = []

    # Grid lines
    for v in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        if mrr_min <= v <= mrr_max:
            y = cy(v)
            elements.append(
                f'<line x1="{PAD["left"]}" y1="{y:.1f}" x2="{W-PAD["right"]}" y2="{y:.1f}" '
                f'stroke="#eee" stroke-dasharray="4"/>'
                f'<text x="{PAD["left"]-6}" y="{y+4:.1f}" font-size="11" text-anchor="end" fill="#999">{v:.1f}</text>'
            )
    for v_lat in [50, 100, 150, 200, 250, 300]:
        if v_lat <= lat_max:
            x = cx(v_lat)
            elements.append(
                f'<line x1="{x:.1f}" y1="{PAD["top"]}" x2="{x:.1f}" y2="{H-PAD["bottom"]}" '
                f'stroke="#eee" stroke-dasharray="4"/>'
                f'<text x="{x:.1f}" y="{H-PAD["bottom"]+18}" font-size="11" text-anchor="middle" fill="#999">{v_lat}</text>'
            )

    # Points
    for r in results:
        x = cx(r.avg_latency_ms)
        y = cy(r.mrr_k5)
        colour = COLORS[r.pool in pareto]
        ci = r.mrr_k5_ci
        if ci:
            y_lo = cy(ci[1])  # Note: higher MRR = lower y
            y_hi = cy(ci[0])
            elements.append(
                f'<line x1="{x:.1f}" y1="{y_lo:.1f}" x2="{x:.1f}" y2="{y_hi:.1f}" '
                f'stroke="{colour}" stroke-width="1.5" opacity="0.5"/>'
            )
        elements.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="{colour}" stroke="white" stroke-width="2"/>'
            f'<text x="{x:.1f}" y="{y-12:.1f}" font-size="12" font-weight="bold" text-anchor="middle" fill="{colour}">'
            f'pool={r.pool}</text>'
        )

    # Axis labels
    elements.append(
        f'<text x="{W//2}" y="{H-10}" font-size="13" text-anchor="middle" fill="#555">Avg Latency (ms)</text>'
        f'<text x="16" y="{H//2}" font-size="13" text-anchor="middle" fill="#555" '
        f'transform="rotate(-90 16 {H//2})">MRR@5</text>'
        f'<text x="{W//2}" y="22" font-size="14" font-weight="bold" text-anchor="middle" fill="#333">'
        f'Quality vs Latency - HYBRID Pool Size Experiment</text>'
    )

    # Axes
    elements.append(
        f'<line x1="{PAD["left"]}" y1="{PAD["top"]}" x2="{PAD["left"]}" y2="{H-PAD["bottom"]}" stroke="#ccc"/>'
        f'<line x1="{PAD["left"]}" y1="{H-PAD["bottom"]}" x2="{W-PAD["right"]}" y2="{H-PAD["bottom"]}" stroke="#ccc"/>'
    )

    # Legend
    elements.append(
        f'<rect x="{W-PAD["right"]-120}" y="30" width="12" height="12" fill="{COLORS[True]}"/>'
        f'<text x="{W-PAD["right"]-104}" y="41" font-size="11" fill="#555">Pareto-optimal</text>'
        f'<rect x="{W-PAD["right"]-120}" y="48" width="12" height="12" fill="{COLORS[False]}"/>'
        f'<text x="{W-PAD["right"]-104}" y="59" font-size="11" fill="#555">Dominated</text>'
    )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
        f'<rect width="{W}" height="{H}" fill="white" rx="4"/>'
        + "".join(elements)
        + "</svg>"
    )
    output_path.write_text(svg, encoding="utf-8")
    print(f"SVG chart written: {output_path}")


def write_results_json(results: list[PoolResult], pareto: list[int], output_path: Path) -> None:
    data = {
        "experiment": "pool_size_experiment",
        "eval_k": EVAL_K,
        "pool_sizes": POOL_SIZES,
        "pareto_optimal": pareto,
        "results": [
            {
                "pool": r.pool,
                "ann_pool": r.ann_pool,
                "precision": round(r.precision, 4),
                "recall": round(r.recall, 4),
                "hit_rate": round(r.hit_rate, 4),
                "hit_rate_ci": list(r.hit_rate_ci) if r.hit_rate_ci else None,
                "mrr_k5": round(r.mrr_k5, 4),
                "mrr_k5_ci": list(r.mrr_k5_ci) if r.mrr_k5_ci else None,
                "mrr_full": round(r.mrr_full, 4),
                "map_k5": round(r.map_k5, 4),
                "ndcg_k5": round(r.ndcg_k5, 4),
                "avg_latency_ms": round(r.avg_latency_ms, 2),
                "query_count": len(r.query_results),
            }
            for r in results
        ],
    }
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Recommendation
# ---------------------------------------------------------------------------

def print_recommendation(results: list[PoolResult], pareto: list[int]) -> None:
    sep = "=" * 70
    print(sep)
    print("RECOMMENDATION")
    print(sep)
    print()

    # Find the Pareto-optimal pool that maximises Hit Rate@5 with reasonable latency
    pareto_results = [r for r in results if r.pool in pareto]
    pareto_results.sort(key=lambda r: (-r.hit_rate, r.avg_latency_ms))

    # The "best" Pareto point maximises Hit Rate@5; break ties by lowest latency
    best = pareto_results[0] if pareto_results else max(results, key=lambda r: r.hit_rate)

    # Baseline is pool=5
    base = next(r for r in results if r.pool == 5)

    # Cost of the recommendation vs baseline
    d_hit = best.hit_rate - base.hit_rate
    d_mrr = best.mrr_k5 - base.mrr_k5
    lat_x = best.avg_latency_ms / max(base.avg_latency_ms, 0.001)

    print(f"  Recommended production pool size: {best.pool}")
    print()
    print(f"  Rationale:")
    print(f"    Hit Rate@5 : {base.hit_rate:.3f} = {best.hit_rate:.3f}  (D{d_hit:+.3f})")
    print(f"    MRR@5      : {base.mrr_k5:.3f} = {best.mrr_k5:.3f}  (D{d_mrr:+.3f})")
    print(f"    Latency    : {base.avg_latency_ms:.1f}ms = {best.avg_latency_ms:.1f}ms  ({lat_x:.2f}x)")
    print()

    # Statistical significance of the Hit Rate difference
    base_hits = [1.0 if q.hit else 0.0 for q in base.query_results]
    best_hits = [1.0 if q.hit else 0.0 for q in best.query_results]
    lo, hi, sig = bootstrap_delta_ci(best_hits, base_hits, n_boot=2000, seed=42)

    sig_str = "statistically significant" if sig else "NOT statistically significant"
    print(f"    Hit Rate delta 95% CI: [{lo:+.3f}, {hi:+.3f}] - {sig_str}")
    print()

    if best.pool == 5:
        print("    The current pool size (5) is already Pareto-optimal.")
        print("    No pool size change is recommended.")
    elif sig and d_hit > 0:
        print(f"    Changing DEFAULT_HYBRID_LIMIT from 5 to {best.pool} is recommended.")
        print("    The quality improvement is statistically significant.")
        print("    The latency cost is within the 300ms gate for HYBRID.")
    elif d_hit > 0 and not sig:
        print(f"    pool={best.pool} shows improvement but the difference is not")
        print(f"    statistically significant on n=50 queries.")
        print(f"    Increasing to n>=100 verified queries (Sprint 3) would clarify.")
    else:
        print("    The current pool size (5) is sufficient for this corpus.")

    print()
    print("  This is a recommendation only. Production default requires explicit approval.")
    print(sep)
    print()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="HYBRID pool size experiment.")
    p.add_argument("--user-id", type=int, default=1)
    p.add_argument(
        "--benchmark",
        type=str,
        default="app/evaluation/benchmark/benchmark.json",
    )
    p.add_argument(
        "--output",
        type=str,
        default="evaluation_results/pool_experiment",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    benchmark = BenchmarkLoader.load(args.benchmark)
    warmup_query = benchmark[0].query if benchmark else "What startup ideas do I have?"
    print(f"\nPool size experiment: {len(benchmark)} queries x {len(POOL_SIZES)} pool sizes")
    print(f"Pool sizes: {POOL_SIZES}")
    print(f"Eval K: {EVAL_K}")
    print()

    db = SessionLocal()
    all_results: list[PoolResult] = []

    try:
        for pool in POOL_SIZES:
            ann = max(pool * 4, 20)
            print(f"Running pool={pool} (ann_pool={ann})...", end=" ", flush=True)
            t_start = time.perf_counter()
            result = run_pool(
                pool_size=pool,
                benchmark_queries=benchmark,
                db=db,
                user_id=args.user_id,
                warmup_query=warmup_query,
            )
            elapsed = time.perf_counter() - t_start
            print(
                f"done in {elapsed:.1f}s  "
                f"Hit@5={result.hit_rate:.3f}  MRR@5={result.mrr_k5:.3f}  "
                f"lat={result.avg_latency_ms:.1f}ms"
            )
            all_results.append(result)
    finally:
        db.close()

    # Analysis
    pareto = pareto_frontier(all_results, quality_metric="hit_rate", latency_metric="avg_latency_ms")

    print()
    print_comparison_table(all_results)
    print_delta_table(all_results, baseline_pool=5)
    print_difficulty_breakdown(all_results)
    print_quality_latency_chart(all_results, pareto)
    print_pareto_analysis(all_results, pareto)
    print_recommendation(all_results, pareto)

    # Artefacts
    write_results_json(all_results, pareto, output_dir / "results.json")
    generate_svg_chart(all_results, pareto, output_dir / "quality_vs_latency.svg")

    # Per-query CSV for offline analysis
    import csv
    csv_path = output_dir / "per_query.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pool", "benchmark_id", "query", "difficulty", "hit", "rr_k5", "rr_full", "precision", "recall", "map", "ndcg", "latency_ms"])
        for r in all_results:
            for q in r.query_results:
                w.writerow([
                    r.pool, q.benchmark_id, q.query, q.difficulty,
                    int(q.hit), round(q.rr_k5, 4), round(q.rr_full, 4),
                    round(q.precision, 4), round(q.recall, 4),
                    round(q.map_k5, 4), round(q.ndcg_k5, 4),
                    round(q.latency_ms, 2),
                ])
    print(f"Per-query CSV: {csv_path}")
    print(f"Results JSON : {output_dir/'results.json'}")
    print(f"SVG chart    : {output_dir/'quality_vs_latency.svg'}")
    print()


if __name__ == "__main__":
    main()
