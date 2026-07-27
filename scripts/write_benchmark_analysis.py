"""
Writes BENCHMARK_ANALYSIS.md from generated benchmark files + evaluation results.

Usage:
    python scripts/write_benchmark_analysis.py \
        --retrieval-benchmark evaluation_results/benchmarks/retrieval_benchmark.json \
        --ask-benchmark evaluation_results/benchmarks/ask_benchmark.json \
        --retrieval-results evaluation_results/evaluation_results.csv \
        --output evaluation_results/BENCHMARK_ANALYSIS.md
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import statistics
import sys
from collections import defaultdict
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("write_benchmark_analysis")


def load_json(path: Path) -> list | dict:
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def load_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def analyze_retrieval_benchmark(entries: list[dict]) -> dict:
    if not entries:
        return {}

    difficulties = defaultdict(int)
    intents = defaultdict(int)
    tag_types = defaultdict(int)
    notes_per_query = []
    queries_no_notes = 0

    for e in entries:
        difficulties[e.get("difficulty", "unknown")] += 1
        intents[e.get("expected_intent", "unknown")] += 1
        ids = e.get("relevant_note_ids", [])
        notes_per_query.append(len(ids))
        if not ids:
            queries_no_notes += 1
        for tag in e.get("tags", []):
            if tag in ("exact", "ambiguous", "comparison", "temporal", "multi_hop"):
                tag_types[tag] += 1

    return {
        "total": len(entries),
        "difficulties": dict(difficulties),
        "intent_distribution": dict(intents),
        "tag_types": dict(tag_types),
        "avg_relevant_per_query": round(statistics.mean(notes_per_query), 2) if notes_per_query else 0,
        "min_relevant": min(notes_per_query) if notes_per_query else 0,
        "max_relevant": max(notes_per_query) if notes_per_query else 0,
        "queries_with_no_notes": queries_no_notes,
    }


def analyze_ask_benchmark(entries: list[dict]) -> dict:
    if not entries:
        return {}

    categories = defaultdict(int)
    difficulties = defaultdict(int)
    notes_per_query = []

    for e in entries:
        categories[e.get("category", "unknown")] += 1
        difficulties[e.get("difficulty", "unknown")] += 1
        notes_per_query.append(len(e.get("expected_note_ids", [])))

    return {
        "total": len(entries),
        "categories": dict(categories),
        "difficulties": dict(difficulties),
        "avg_notes_per_query": round(statistics.mean(notes_per_query), 2) if notes_per_query else 0,
    }


def analyze_eval_results(rows: list[dict]) -> dict:
    if not rows:
        return {}

    by_strategy = defaultdict(list)
    for row in rows:
        by_strategy[row["strategy"]].append(row)

    results = {}
    for strategy, strategy_rows in by_strategy.items():
        rr = [float(r["reciprocal_rank"]) for r in strategy_rows]
        rec = [float(r["recall_at_k"]) for r in strategy_rows]
        pre = [float(r["precision_at_k"]) for r in strategy_rows]
        lat = [float(r["latency_ms"]) for r in strategy_rows]
        hits = sum(1 for r in strategy_rows if r.get("hit") == "True")
        results[strategy] = {
            "n": len(strategy_rows),
            "mrr": round(statistics.mean(rr), 4),
            "recall": round(statistics.mean(rec), 4),
            "precision": round(statistics.mean(pre), 4),
            "hit_rate": round(hits / len(strategy_rows), 4),
            "avg_latency_ms": round(statistics.mean(lat), 2),
        }
    return results


def write_md(
    ret_analysis: dict,
    ask_analysis: dict,
    eval_results: dict,
    out_path: Path,
) -> None:
    lines = []

    def h(n, t):
        lines.append(f"\n{'#'*n} {t}\n")
    def p(t=""):
        lines.append(t)
    def table(headers, rows):
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for row in rows:
            lines.append("| " + " | ".join(str(c) for c in row) + " |")

    h(1, "KnowledgeVault — Benchmark Analysis Report")
    p("This report describes the benchmark datasets generated for evaluating KnowledgeVault's")
    p("retrieval and RAG pipeline quality. Benchmarks were generated from 1000 notes ingested through the production pipeline.")

    h(2, "1. Retrieval Benchmark")

    if ret_analysis:
        table(
            ["Metric", "Value"],
            [
                ["Total Queries", ret_analysis["total"]],
                ["Avg Relevant Notes per Query", ret_analysis["avg_relevant_per_query"]],
                ["Min Relevant Notes", ret_analysis["min_relevant"]],
                ["Max Relevant Notes", ret_analysis["max_relevant"]],
                ["Queries with No Matched Notes", ret_analysis["queries_with_no_notes"]],
            ],
        )

        p()
        h(3, "By Difficulty")
        table(
            ["Difficulty", "Count", "Percentage"],
            [
                [d, c, f"{c / max(1, ret_analysis['total']):.1%}"]
                for d, c in sorted(ret_analysis["difficulties"].items())
            ],
        )

        h(3, "By Expected Intent Type")
        table(
            ["Intent", "Count"],
            sorted(ret_analysis["intent_distribution"].items(), key=lambda x: -x[1]),
        )

        h(3, "Special Query Types")
        table(
            ["Type", "Count", "Description"],
            [
                ["exact", ret_analysis["tag_types"].get("exact", 0), "Exact phrase from note content"],
                ["ambiguous", ret_analysis["tag_types"].get("ambiguous", 0), "Queries with multiple valid interpretations"],
                ["comparison", ret_analysis["tag_types"].get("comparison", 0), "X vs Y comparative queries"],
                ["temporal", ret_analysis["tag_types"].get("temporal", 0), "Time-relative queries (this week, upcoming)"],
                ["multi_hop", ret_analysis["tag_types"].get("multi_hop", 0), "Require synthesizing multiple notes"],
            ],
        )
    else:
        p("_Retrieval benchmark not generated yet. Run `generate_benchmarks.py` first._")

    h(2, "2. Ask / RAG Benchmark")
    if ask_analysis:
        table(
            ["Metric", "Value"],
            [
                ["Total Questions", ask_analysis["total"]],
                ["Avg Expected Notes per Question", ask_analysis["avg_notes_per_query"]],
            ],
        )

        h(3, "By Category")
        table(
            ["Category", "Count", "Description"],
            [
                [cat, count, {
                    "factual_lookup": "Direct fact retrieval from a single note",
                    "multi_hop": "Requires combining information from 2+ notes",
                    "temporal": "Time-sensitive or date-relative questions",
                    "comparison": "Asks to compare two technologies or approaches",
                    "synthesis": "Requests a summary across multiple notes",
                    "ambiguous": "Underspecified — multiple valid interpretations",
                    "category": "Category-browsing oriented",
                }.get(cat, "")]
                for cat, count in sorted(ask_analysis["categories"].items(), key=lambda x: -x[1])
            ],
        )

        h(3, "By Difficulty")
        table(
            ["Difficulty", "Count"],
            sorted(ask_analysis["difficulties"].items()),
        )
    else:
        p("_Ask benchmark not generated yet. Run `generate_benchmarks.py` first._")

    h(2, "3. Evaluation Results (if available)")
    if eval_results:
        table(
            ["Strategy", "N", "Precision@K", "Recall@K", "Hit Rate", "MRR", "Avg Latency (ms)"],
            [
                [
                    s.upper(),
                    m["n"],
                    f"{m['precision']:.4f}",
                    f"{m['recall']:.4f}",
                    f"{m['hit_rate']:.4f}",
                    f"{m['mrr']:.4f}",
                    f"{m['avg_latency_ms']:.2f}",
                ]
                for s, m in sorted(eval_results.items())
            ],
        )

        p()
        if "hybrid" in eval_results and "semantic" in eval_results:
            h_mrr = eval_results["hybrid"]["mrr"]
            s_mrr = eval_results["semantic"]["mrr"]
            delta = h_mrr - s_mrr
            p(f"**Hybrid vs Semantic ΔMRR: {delta:+.4f}**")
            if abs(delta) < 0.001:
                p("The hybrid arm produces no measurable improvement over pure semantic retrieval. See AI_ARCHITECTURE_REVIEW.md for root cause analysis.")
    else:
        p("_Evaluation results not yet available. Run `scripts/evaluate.py` with the new benchmark._")
        p()
        p("To run evaluation:")
        p("```bash")
        p("python scripts/evaluate.py \\")
        p("    --user-id 1 \\")
        p("    --benchmark evaluation_results/benchmarks/retrieval_benchmark.json \\")
        p("    --output evaluation_results/")
        p("")
        p("python scripts/evaluate_ask.py \\")
        p("    --user-id 1 \\")
        p("    --dataset evaluation_results/benchmarks/ask_benchmark.json \\")
        p("    --output evaluation_results/")
        p("```")

    h(2, "4. Benchmark Design Notes")
    p("### Query Type Coverage")
    p("The retrieval benchmark covers all major query types:")
    p("- **Factual lookup**: direct topic search (e.g., 'What is HNSW?')")
    p("- **Paraphrased**: same concept, different phrasing")
    p("- **Multi-hop**: combine multiple notes (e.g., 'KnowledgeVault RAG decisions and benchmark findings')")
    p("- **Temporal**: date/time relative (e.g., 'pending tasks this week')")
    p("- **Comparison**: X vs Y queries (e.g., 'Redis vs Kafka')")
    p("- **Synthesis**: summarize a category (e.g., 'all my AI notes')")
    p("- **Ambiguous**: underspecified intent (e.g., 'my project notes')")
    p("- **Exact keyword**: precise phrase from note content (e.g., 'HNSW index')")
    p("- **Semantic**: meaning-based, not keyword-based (e.g., 'strategies for improving code performance')")
    p("- **Category-oriented**: category browsing queries")
    p()
    p("### Known Limitations")
    p("1. `relevant_note_ids` are assigned by content keyword matching, which may miss notes where the same concept is expressed differently.")
    p("2. Temporal queries have inherently fuzzy ground truth — the expected set depends on what 'this week' means relative to note creation dates.")
    p("3. Multi-hop queries require the retrieval system to surface multiple notes; the current K=5 limit may prevent full recall for queries expecting 6+ notes.")
    p("4. The ask benchmark reference answers are written for the notes dataset and assume the notes contain the factual information. If a note was not correctly processed, the answer may be unreachable.")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    logger.info("BENCHMARK_ANALYSIS.md written: %s", out_path)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--retrieval-benchmark", type=Path, default=Path("evaluation_results/benchmarks/retrieval_benchmark.json"))
    p.add_argument("--ask-benchmark", type=Path, default=Path("evaluation_results/benchmarks/ask_benchmark.json"))
    p.add_argument("--retrieval-results", type=Path, default=Path("evaluation_results/evaluation_results.csv"))
    p.add_argument("--output", type=Path, default=Path("evaluation_results/BENCHMARK_ANALYSIS.md"))
    return p.parse_args()


def main():
    args = parse_args()

    ret_entries = load_json(args.retrieval_benchmark)
    ask_entries = load_json(args.ask_benchmark)
    eval_rows = load_csv(args.retrieval_results)

    ret_analysis = analyze_retrieval_benchmark(ret_entries)
    ask_analysis = analyze_ask_benchmark(ask_entries)
    eval_results = analyze_eval_results(eval_rows)

    write_md(ret_analysis, ask_analysis, eval_results, args.output)
    logger.info("Done.")


if __name__ == "__main__":
    main()
