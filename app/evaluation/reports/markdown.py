"""
Markdown report generator.

Creates a GitHub-friendly Markdown report from an EvaluationReport.

No metrics are calculated here.
"""

from __future__ import annotations

from pathlib import Path

from app.evaluation.models import EvaluationReport


class MarkdownReport:

    @staticmethod
    def generate(
        report: EvaluationReport,
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)
        lines: list[str] = []

        # ── Header ───────────────────────────────────────────────────────

        lines.append("# KnowledgeVault Evaluation Report")
        lines.append("")
        lines.append(f"**Run ID:** `{report.run_id}`")
        lines.append("")
        lines.append(f"**Created:** {report.created_at}")
        if report.git_commit:
            lines.append("")
            lines.append(f"**Git Commit:** `{report.git_commit}`")
        lines.append("")
        lines.append(f"**Benchmark Version:** `{report.benchmark_version}`")
        lines.append("")
        lines.append(f"**Queries:** {report.total_queries}")
        lines.append("")
        lines.append(f"**K:** {report.k}")
        if report.corpus_coverage > 0:
            lines.append("")
            lines.append(
                f"**Corpus Coverage:** {report.corpus_coverage:.1%} "
                f"(fraction of notes touched across all retrieved sets)"
            )
        lines.append("")

        # ── Strategy Comparison ──────────────────────────────────────────

        lines.append("## Strategy Comparison")
        lines.append("")
        lines.append(
            "| Strategy | Precision | Recall | Hit Rate | MRR | MRR 95% CI | MAP@K | R-Prec | nDCG | Intent Acc | Category Acc | Avg Latency (ms) |"
        )
        lines.append(
            "|-----------|----------:|-------:|---------:|----:|:----------:|------:|-------:|-----:|------------:|-------------:|-----------------:|"
        )

        for summary in report.summaries:
            intent = (
                "-" if summary.intent_accuracy is None
                else f"{summary.intent_accuracy:.3f}"
            )
            category = (
                "-" if summary.category_accuracy is None
                else f"{summary.category_accuracy:.3f}"
            )
            ci = summary.mrr_ci
            ci_str = f"[{ci[0]:.3f}, {ci[1]:.3f}]" if ci else "-"

            lines.append(
                f"| {summary.strategy.value.upper()} "
                f"| {summary.mean_precision_at_k:.3f} "
                f"| {summary.mean_recall_at_k:.3f} "
                f"| {summary.hit_rate:.3f} "
                f"| {summary.mrr:.3f} "
                f"| {ci_str} "
                f"| {summary.mean_map_at_k:.3f} "
                f"| {summary.mean_r_precision:.3f} "
                f"| {summary.mean_ndcg_at_k:.3f} "
                f"| {intent} "
                f"| {category} "
                f"| {summary.avg_latency_ms:.2f} |"
            )

        lines.append("")

        # ── Statistical Comparisons ───────────────────────────────────────

        if report.strategy_comparisons:
            lines.append("## Statistical Comparisons (95% Bootstrap CI)")
            lines.append("")
            lines.append(
                "| Comparison | ΔMRR | MRR CI | Significant | ΔHIT | Hit CI | Recommendation |"
            )
            lines.append(
                "|-----------|-----:|:------:|:-----------:|-----:|:------:|:--------------|"
            )
            for comp in report.strategy_comparisons:
                mrr_ci = f"[{comp.mrr_ci_lower:.3f}, {comp.mrr_ci_upper:.3f}]"
                hit_ci = f"[{comp.hit_rate_ci_lower:.3f}, {comp.hit_rate_ci_upper:.3f}]"
                lines.append(
                    f"| {comp.candidate.value.upper()} vs {comp.baseline.value.upper()} "
                    f"| {comp.delta_mrr:+.4f} "
                    f"| {mrr_ci} "
                    f"| {'✓' if comp.mrr_significant else '✗'} "
                    f"| {comp.delta_hit_rate:+.4f} "
                    f"| {hit_ci} "
                    f"| {comp.recommendation} |"
                )
            lines.append("")

        # ── Difficulty Breakdown ──────────────────────────────────────────

        difficulty_data: dict[str, dict[str, dict[str, float]]] = {}
        for summary in report.summaries:
            if summary.difficulty_breakdown:
                difficulty_data[summary.strategy.value] = summary.difficulty_breakdown

        if difficulty_data:
            lines.append("## Per-Difficulty Breakdown")
            lines.append("")
            difficulties = sorted({
                d for s in difficulty_data.values() for d in s
            })
            lines.append(
                "| Strategy | " + " | ".join(
                    f"{d.capitalize()} MRR" for d in difficulties
                ) + " |"
            )
            lines.append(
                "| --- | " + " | ".join("---:" for _ in difficulties) + " |"
            )
            for strat, breakdown in sorted(difficulty_data.items()):
                row = f"| {strat.upper()} |"
                for d in difficulties:
                    val = breakdown.get(d, {}).get("mrr", None)
                    row += f" {val:.3f} |" if val is not None else " - |"
                lines.append(row)
            lines.append("")

        # ── Per Query Results ─────────────────────────────────────────────

        lines.append("## Query Results")
        lines.append("")

        for evaluation in report.evaluations:
            lines.append(
                f"### {evaluation.strategy.value.upper()} — {evaluation.query}"
            )
            lines.append("")
            lines.append(f"- **Benchmark ID:** {evaluation.benchmark_id}")
            lines.append(f"- **Difficulty:** {evaluation.difficulty}")
            if evaluation.retrieval_challenge:
                lines.append(f"- **Challenge:** {evaluation.retrieval_challenge}")
            lines.append(f"- **Relevant Notes:** {evaluation.relevant_note_ids}")
            lines.append(f"- **Retrieved Notes:** {evaluation.retrieved_note_ids}")
            lines.append("")

            lines.append("| Metric | Value |")
            lines.append("|-------|------:|")
            lines.append(f"| Precision@{report.k} | {evaluation.precision_at_k:.3f} |")
            lines.append(f"| Recall@{report.k} | {evaluation.recall_at_k:.3f} |")
            lines.append(f"| Hit | {evaluation.hit} |")
            lines.append(f"| Reciprocal Rank | {evaluation.reciprocal_rank:.3f} |")
            lines.append(f"| MAP@{report.k} | {evaluation.map_at_k:.3f} |")
            lines.append(f"| R-Precision | {evaluation.r_precision:.3f} |")
            lines.append(f"| Latency (ms) | {evaluation.latency_ms:.2f} |")

            if evaluation.intent_correct is not None:
                lines.append(f"| Predicted Intent | {evaluation.predicted_intent} |")
                lines.append(f"| Expected Intent | {evaluation.expected_intent} |")
                lines.append(f"| Intent Correct | {evaluation.intent_correct} |")

            if evaluation.category_correct is not None:
                lines.append(f"| Predicted Category | {evaluation.predicted_category} |")
                lines.append(f"| Expected Category | {evaluation.expected_category} |")
                lines.append(f"| Category Correct | {evaluation.category_correct} |")

            if evaluation.error:
                lines.append("")
                lines.append("**Error**")
                lines.append("")
                lines.append("```")
                lines.append(evaluation.error)
                lines.append("```")

            lines.append("")
            lines.append("---")
            lines.append("")

        # ── Footer ───────────────────────────────────────────────────────

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(
            "_Generated automatically by the KnowledgeVault Evaluation Framework._"
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("\n".join(lines), encoding="utf-8")
