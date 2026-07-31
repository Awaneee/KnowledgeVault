"""
Static HTML dashboard generator.

Reads historical manifest.json files from an evaluation results tree and
produces a self-contained dashboard.html with:
  1. Header (run info, benchmark version, git commit, corpus coverage)
  2. Strategy comparison table with CI columns
  3. MRR trend chart across historical runs (inline SVG via vanilla JS)
  4. Per-query heatmap (one row per query, one column per strategy)
  5. Failure analysis (queries sorted by worst MRR across all strategies)
  6. Gate check summary (regression floor status per strategy)

No external dependencies.  The output file can be opened directly in any
browser and committed to the repository alongside the CSV results.

Usage:
    python scripts/generate_dashboard.py \\
        --results-dir evaluation_results/sprint2b_fresh \\
        [--history-dir evaluation_results]  # for trend data
        [--output dashboard.html]

Sprint 2-C: called automatically by scripts/evaluate.py after each run.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
import sys
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def load_manifest(results_dir: Path) -> dict:
    path = results_dir / "manifest.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def load_results_csv(results_dir: Path) -> list[dict]:
    path = results_dir / "evaluation_results.csv"
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_history(history_dir: Path, current_run_id: str) -> list[dict]:
    """Load historical manifests sorted by creation date (oldest first)."""
    manifests: list[dict] = []
    for manifest_path in sorted(history_dir.glob("*/manifest.json")):
        try:
            m = json.loads(manifest_path.read_text(encoding="utf-8"))
            if m.get("run_id") != current_run_id:  # exclude current run (already shown)
                manifests.append(m)
        except Exception:
            pass
    return sorted(manifests, key=lambda m: m.get("created_at", ""))


# ---------------------------------------------------------------------------
# Per-query data extraction
# ---------------------------------------------------------------------------

def build_query_table(results: list[dict]) -> tuple[list[str], list[str], dict[tuple[str, str], dict]]:
    """
    Returns:
      - query_ids: ordered list of benchmark IDs
      - strategies: sorted list of strategy names
      - cell_data: (benchmark_id, strategy) → {rr, hit, precision, recall, query, difficulty}
    """
    query_ids: list[str] = []
    seen_qids: set[str] = set()
    strategies: set[str] = set()
    cell_data: dict[tuple[str, str], dict] = {}
    query_text: dict[str, str] = {}
    query_difficulty: dict[str, str] = {}

    for row in results:
        qid = row.get("benchmark_id", "")
        strat = row.get("strategy", "")
        if qid not in seen_qids:
            seen_qids.add(qid)
            query_ids.append(qid)
        strategies.add(strat)
        query_text[qid] = row.get("query", "")
        query_difficulty[qid] = row.get("difficulty", "")

        try:
            rr = float(row.get("reciprocal_rank", 0))
            hit = row.get("hit") == "True"
        except (ValueError, TypeError):
            rr, hit = 0.0, False

        cell_data[(qid, strat)] = {
            "rr": rr,
            "hit": hit,
            "query": query_text[qid],
            "difficulty": query_difficulty[qid],
        }

    return query_ids, sorted(strategies), cell_data


def compute_per_query_worst_rr(
    query_ids: list[str],
    strategies: list[str],
    cell_data: dict[tuple[str, str], dict],
) -> list[tuple[str, float, str]]:
    """Return (benchmark_id, worst_mrr, query_text) sorted by worst_mrr ascending."""
    rows = []
    for qid in query_ids:
        rrs = [
            cell_data.get((qid, s), {}).get("rr", 0.0)
            for s in strategies
        ]
        worst = min(rrs) if rrs else 0.0
        query = cell_data.get((qid, strategies[0] if strategies else ""), {}).get("query", qid)
        rows.append((qid, worst, query))
    return sorted(rows, key=lambda x: x[1])


# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------

def rr_to_colour(rr: float) -> str:
    """Map reciprocal rank [0,1] to a hex background colour."""
    if rr >= 1.0:
        return "#2ecc71"   # green — rank 1
    elif rr >= 0.5:
        return "#f1c40f"   # yellow — rank 2
    elif rr >= 0.333:
        return "#e67e22"   # orange — rank 3
    elif rr > 0.0:
        return "#e74c3c"   # red — rank > 3
    else:
        return "#95a5a6"   # grey — miss


# ---------------------------------------------------------------------------
# SVG trend chart
# ---------------------------------------------------------------------------

def _svg_trend_chart(
    history: list[dict],
    current: dict,
    width: int = 800,
    height: int = 300,
) -> str:
    """Render a minimal SVG line chart showing MRR over runs."""
    COLORS = {
        "SEMANTIC": "#3498db",
        "HYBRID": "#2ecc71",
        "RERANK": "#e74c3c",
        "INTENT": "#9b59b6",
    }
    PADDING = {"top": 30, "bottom": 50, "left": 50, "right": 20}

    all_runs = [*history, current]
    if not all_runs:
        return "<p><em>No historical data available.</em></p>"

    # Determine strategies present
    strategies: set[str] = set()
    for m in all_runs:
        strategies.update(m.get("summaries", {}).keys())
    strategies = sorted(strategies)

    # X positions — evenly spaced
    inner_w = width - PADDING["left"] - PADDING["right"]
    inner_h = height - PADDING["top"] - PADDING["bottom"]
    n = len(all_runs)
    x_step = inner_w / max(1, n - 1) if n > 1 else inner_w

    def x_pos(i: int) -> float:
        return PADDING["left"] + (i * x_step if n > 1 else inner_w / 2)

    def y_pos(mrr: float) -> float:
        # MRR range: 0 to 1, with 0 at the bottom
        return PADDING["top"] + inner_h - (mrr * inner_h)

    lines_svg: list[str] = []
    dots_svg: list[str] = []
    legend_svg: list[str] = []

    for idx_s, strat in enumerate(strategies):
        colour = COLORS.get(strat, "#7f8c8d")
        points: list[tuple[float, float]] = []
        for idx_r, m in enumerate(all_runs):
            mrr = m.get("summaries", {}).get(strat, {}).get("mrr")
            if mrr is not None:
                points.append((x_pos(idx_r), y_pos(float(mrr))))

        if len(points) >= 2:
            path_d = " ".join(
                f"{'M' if i == 0 else 'L'}{p[0]:.1f},{p[1]:.1f}"
                for i, p in enumerate(points)
            )
            lines_svg.append(
                f'<path d="{path_d}" fill="none" stroke="{colour}" stroke-width="2"/>'
            )
        for px, py in points:
            dots_svg.append(
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{colour}"/>'
            )

        # Legend
        lx = PADDING["left"] + idx_s * 120
        ly = height - 15
        legend_svg.append(
            f'<rect x="{lx}" y="{ly-10}" width="14" height="10" fill="{colour}"/>'
            f'<text x="{lx+18}" y="{ly}" font-size="12" fill="#333">{strat}</text>'
        )

    # Y-axis labels
    y_labels: list[str] = []
    for v in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        py = y_pos(v)
        y_labels.append(
            f'<line x1="{PADDING["left"]-5}" y1="{py:.1f}" '
            f'x2="{PADDING["left"]}" y2="{py:.1f}" stroke="#ccc"/>'
            f'<text x="{PADDING["left"]-8}" y="{py+4:.1f}" '
            f'font-size="11" text-anchor="end" fill="#666">{v:.1f}</text>'
            f'<line x1="{PADDING["left"]}" y1="{py:.1f}" '
            f'x2="{width-PADDING["right"]}" y2="{py:.1f}" '
            f'stroke="#eee" stroke-dasharray="4"/>'
        )

    # X-axis labels (run dates)
    x_labels: list[str] = []
    for i, m in enumerate(all_runs):
        xpos = x_pos(i)
        label = (m.get("created_at", "")[:10] or f"Run {i+1}")
        marker = " ◀ latest" if m is current else ""
        x_labels.append(
            f'<text x="{xpos:.1f}" y="{height - PADDING["bottom"] + 20}" '
            f'font-size="10" text-anchor="middle" fill="#666">{label}{marker}</text>'
        )

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">'
        f'<rect width="{width}" height="{height}" fill="#fafafa" rx="4"/>'
        f'<text x="{width//2}" y="20" text-anchor="middle" font-size="13" font-weight="bold" fill="#333">MRR Trend</text>'
        + "".join(y_labels)
        + "".join(lines_svg)
        + "".join(dots_svg)
        + "".join(x_labels)
        + "".join(legend_svg)
        + "</svg>"
    )
    return svg


# ---------------------------------------------------------------------------
# HTML generation
# ---------------------------------------------------------------------------

_CSS = """
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
       margin: 0; background: #f5f6fa; color: #2c3e50; }
.header { background: #2c3e50; color: white; padding: 20px 30px; }
.header h1 { margin: 0 0 8px; font-size: 22px; }
.header .meta { font-size: 13px; opacity: 0.8; }
.header .meta span { margin-right: 20px; }
.section { background: white; margin: 16px 24px; padding: 20px 24px;
           border-radius: 6px; box-shadow: 0 1px 4px rgba(0,0,0,.07); }
.section h2 { margin: 0 0 16px; font-size: 16px; color: #2c3e50; border-bottom: 2px solid #ecf0f1; padding-bottom: 8px; }
table { border-collapse: collapse; width: 100%; font-size: 13px; }
th { background: #ecf0f1; text-align: left; padding: 8px 10px; font-weight: 600; }
td { padding: 7px 10px; border-bottom: 1px solid #f0f0f0; }
tr:hover td { background: #f9f9f9; }
.hit-cell { width: 60px; text-align: center; border-radius: 3px; color: white; font-weight: bold; font-size: 12px; padding: 3px 6px; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 11px; font-weight: bold; }
.badge-pass { background: #2ecc71; color: white; }
.badge-fail { background: #e74c3c; color: white; }
.badge-warn { background: #f39c12; color: white; }
.gate-table td:first-child { font-weight: 600; }
.failure-query { font-size: 12px; color: #7f8c8d; }
"""

def _gate_badge(passed: Optional[bool]) -> str:
    if passed is None:
        return '<span class="badge badge-warn">N/A</span>'
    return (
        '<span class="badge badge-pass">PASS</span>'
        if passed else
        '<span class="badge badge-fail">FAIL</span>'
    )


def generate_html(
    manifest: dict,
    results: list[dict],
    history: list[dict],
) -> str:
    run_id = manifest.get("run_id", "unknown")[:8]
    created_at = manifest.get("created_at", "")[:19]
    bv = manifest.get("benchmark_version", "unknown")
    git = manifest.get("git_commit") or "unknown"
    coverage = manifest.get("corpus_coverage", 0)
    k = manifest.get("k", 5)
    q_count = manifest.get("total_queries", 0)
    summaries = manifest.get("summaries", {})
    gate_check = manifest.get("gate_check", {})
    comparisons = manifest.get("comparisons", [])

    query_ids, strategies, cell_data = build_query_table(results)
    failures = compute_per_query_worst_rr(query_ids, strategies, cell_data)

    trend_svg = _svg_trend_chart(history, manifest)

    # ── Strategy comparison table ──
    strat_rows = ""
    for strat, sm in sorted(summaries.items()):
        ci = sm.get("mrr_ci")
        ci_str = f"[{ci[0]:.3f}, {ci[1]:.3f}]" if ci else "—"
        gates = gate_check.get(strat, {})
        pass_icon = "✓" if all(gates.values()) else "✗"
        strat_rows += (
            f"<tr>"
            f"<td><strong>{strat}</strong></td>"
            f"<td>{sm.get('precision', 0):.3f}</td>"
            f"<td>{sm.get('recall', 0):.3f}</td>"
            f"<td>{sm.get('hit_rate', 0):.3f}</td>"
            f"<td>{sm.get('mrr', 0):.3f}</td>"
            f"<td style='font-size:11px;color:#7f8c8d'>{ci_str}</td>"
            f"<td>{sm.get('map_at_k', 0):.3f}</td>"
            f"<td>{sm.get('avg_latency_ms', 0):.1f}</td>"
            f"<td>{pass_icon}</td>"
            f"</tr>"
        )

    # ── Statistical comparisons ──
    comp_rows = ""
    for comp in comparisons:
        sig = "✓" if comp.get("mrr_significant") else "—"
        ci = comp.get("mrr_ci", [None, None])
        ci_str = f"[{ci[0]:.3f}, {ci[1]:.3f}]" if ci[0] is not None else "—"
        rec = comp.get("recommendation", "")
        rec_style = "color:green" if "approve" in rec else ("color:red" if "keep_baseline" in rec else "color:#e67e22")
        comp_rows += (
            f"<tr>"
            f"<td>{comp.get('candidate','').upper()} vs {comp.get('baseline','').upper()}</td>"
            f"<td>{comp.get('delta_mrr',0):+.4f}</td>"
            f"<td>{ci_str}</td>"
            f"<td>{sig}</td>"
            f"<td style='{rec_style}'>{rec}</td>"
            f"</tr>"
        )

    # ── Per-query heatmap ──
    heatmap_header = (
        "<tr><th>#</th><th>Query</th><th>Diff</th>"
        + "".join(f"<th>{s.upper()}</th>" for s in strategies)
        + "</tr>"
    )
    heatmap_rows = ""
    for qid in query_ids:
        first_cell = cell_data.get((qid, strategies[0] if strategies else ""), {})
        query_text = first_cell.get("query", qid)[:60]
        difficulty = first_cell.get("difficulty", "")
        diff_style = {"easy": "color:green", "medium": "color:orange", "hard": "color:red"}.get(difficulty, "")
        cells = ""
        for strat in strategies:
            cell = cell_data.get((qid, strat), {})
            rr = cell.get("rr", 0.0)
            colour = rr_to_colour(rr)
            txt = f"1/{round(1/rr)}" if rr > 0 else "✗"
            cells += f'<td><span class="hit-cell" style="background:{colour}">{txt}</span></td>'
        heatmap_rows += (
            f"<tr>"
            f"<td style='font-size:11px;color:#999'>{qid}</td>"
            f"<td style='font-size:12px'>{query_text}</td>"
            f"<td style='font-size:11px;{diff_style}'>{difficulty}</td>"
            f"{cells}"
            f"</tr>"
        )

    # ── Failure analysis (10 worst) ──
    failure_rows = ""
    for qid, worst_rr, query_text in failures[:15]:
        colour = rr_to_colour(worst_rr)
        failure_rows += (
            f"<tr>"
            f"<td style='font-size:11px;color:#999'>{qid}</td>"
            f"<td class='failure-query'>{query_text[:80]}</td>"
            f"<td><span class='hit-cell' style='background:{colour}'>"
            f"{'miss' if worst_rr == 0 else f'{worst_rr:.2f}'}</span></td>"
            f"</tr>"
        )

    # ── Gate summary table ──
    gate_rows = ""
    for strat, gates in sorted(gate_check.items()):
        gate_rows += (
            f"<tr>"
            f"<td>{strat}</td>"
            f"<td>{_gate_badge(gates.get('mrr_pass'))}</td>"
            f"<td>{_gate_badge(gates.get('hit_rate_pass'))}</td>"
            f"<td>{_gate_badge(gates.get('latency_pass'))}</td>"
            f"</tr>"
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>KnowledgeVault Benchmark Dashboard — {run_id}</title>
<style>{_CSS}</style>
</head>
<body>

<div class="header">
  <h1>KnowledgeVault Retrieval Benchmark Dashboard</h1>
  <div class="meta">
    <span>Run: <strong>{run_id}</strong></span>
    <span>Date: <strong>{created_at}</strong></span>
    <span>Commit: <strong>{git}</strong></span>
    <span>Benchmark: <strong>v{bv}</strong></span>
    <span>Queries: <strong>{q_count}</strong> @ K={k}</span>
    <span>Corpus coverage: <strong>{coverage:.1%}</strong></span>
  </div>
</div>

<div class="section">
  <h2>Strategy Comparison</h2>
  <table>
    <tr>
      <th>Strategy</th><th>Precision</th><th>Recall</th>
      <th>Hit Rate</th><th>MRR</th><th>MRR 95% CI</th>
      <th>MAP@K</th><th>Avg Latency (ms)</th><th>Gates</th>
    </tr>
    {strat_rows}
  </table>
</div>

{'<div class="section"><h2>Statistical Comparisons (95% Bootstrap CI)</h2><table><tr><th>Comparison</th><th>ΔMRR</th><th>MRR CI</th><th>Significant</th><th>Recommendation</th></tr>' + comp_rows + '</table></div>' if comp_rows else ''}

<div class="section">
  <h2>MRR Trend Across Runs</h2>
  {trend_svg}
</div>

<div class="section">
  <h2>Regression Gates</h2>
  <table class="gate-table">
    <tr><th>Strategy</th><th>MRR</th><th>Hit Rate</th><th>Latency</th></tr>
    {gate_rows}
  </table>
</div>

<div class="section">
  <h2>Per-Query Heatmap
    <span style="font-size:12px;font-weight:normal;margin-left:12px;color:#7f8c8d">
      🟢 rank 1 &nbsp; 🟡 rank 2 &nbsp; 🟠 rank 3 &nbsp; 🔴 rank >3 &nbsp; ⬜ miss
    </span>
  </h2>
  <div style="overflow-x:auto">
  <table>
    {heatmap_header}
    {heatmap_rows}
  </table>
  </div>
</div>

<div class="section">
  <h2>Worst-Performing Queries (worst MRR across all strategies)</h2>
  <table>
    <tr><th>#</th><th>Query</th><th>Worst MRR</th></tr>
    {failure_rows}
  </table>
</div>

<div style="text-align:center;padding:16px;font-size:12px;color:#999">
  Generated by KnowledgeVault Evaluation Framework &mdash;
  <a href="evaluation_report.md">Markdown Report</a> &middot;
  <a href="evaluation_results.csv">CSV Results</a>
</div>

</body>
</html>"""
    return html


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate static HTML dashboard.")
    p.add_argument(
        "--results-dir", type=Path, required=True,
        help="Directory containing manifest.json and evaluation_results.csv for the current run.",
    )
    p.add_argument(
        "--history-dir", type=Path, default=None,
        help="Parent directory to scan for historical manifest.json files "
             "(defaults to --results-dir parent).",
    )
    p.add_argument(
        "--output", type=Path, default=None,
        help="Output path for dashboard.html (defaults to <results-dir>/dashboard.html).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    results_dir: Path = args.results_dir
    history_dir: Path = args.history_dir or results_dir.parent
    output_path: Path = args.output or results_dir / "dashboard.html"

    manifest = load_manifest(results_dir)
    if not manifest:
        print(f"No manifest.json in {results_dir} — skipping dashboard generation.")
        return

    results = load_results_csv(results_dir)
    history = load_history(history_dir, manifest.get("run_id", ""))

    html = generate_html(manifest, results, history)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(f"Dashboard written: {output_path}")


if __name__ == "__main__":
    main()
