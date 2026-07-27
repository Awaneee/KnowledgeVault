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

        lines = []

        # ======================================================
        # Header
        # ======================================================

        lines.append("# KnowledgeVault Evaluation Report")
        lines.append("")
        lines.append(f"**Run ID:** `{report.run_id}`")
        lines.append("")
        lines.append(f"**Created:** {report.created_at}")
        lines.append("")
        lines.append(f"**Queries:** {report.total_queries}")
        lines.append("")
        lines.append(f"**K:** {report.k}")
        lines.append("")

        # ======================================================
        # Strategy Summary
        # ======================================================

        lines.append("## Strategy Comparison")
        lines.append("")

        lines.append(
            "| Strategy | Precision | Recall | Hit Rate | MRR | Intent Acc | Category Acc | Avg Latency (ms) |"
        )

        lines.append(
            "|-----------|----------:|-------:|---------:|----:|------------:|-------------:|-----------------:|"
        )

        for summary in report.summaries:

            intent = (
                "-"
                if summary.intent_accuracy is None
                else f"{summary.intent_accuracy:.3f}"
            )

            category = (
                "-"
                if summary.category_accuracy is None
                else f"{summary.category_accuracy:.3f}"
            )

            lines.append(

                f"| {summary.strategy.value.upper()} "
                f"| {summary.mean_precision_at_k:.3f} "
                f"| {summary.mean_recall_at_k:.3f} "
                f"| {summary.hit_rate:.3f} "
                f"| {summary.mrr:.3f} "
                f"| {intent} "
                f"| {category} "
                f"| {summary.avg_latency_ms:.2f} |"

            )

        lines.append("")

        # ======================================================
        # Per Query Results
        # ======================================================

        lines.append("## Query Results")
        lines.append("")

        for evaluation in report.evaluations:

            lines.append(
                f"### {evaluation.strategy.value.upper()} — {evaluation.query}"
            )

            lines.append("")

            lines.append(
                f"- **Benchmark ID:** {evaluation.benchmark_id}"
            )

            lines.append(
                f"- **Difficulty:** {evaluation.difficulty}"
            )

            lines.append(
                f"- **Relevant Notes:** {evaluation.relevant_note_ids}"
            )

            lines.append(
                f"- **Retrieved Notes:** {evaluation.retrieved_note_ids}"
            )

            lines.append("")

            lines.append("| Metric | Value |")
            lines.append("|-------|------:|")

            lines.append(
                f"| Precision@{report.k} | {evaluation.precision_at_k:.3f} |"
            )

            lines.append(
                f"| Recall@{report.k} | {evaluation.recall_at_k:.3f} |"
            )

            lines.append(
                f"| Hit | {evaluation.hit} |"
            )

            lines.append(
                f"| Reciprocal Rank | {evaluation.reciprocal_rank:.3f} |"
            )

            lines.append(
                f"| Latency (ms) | {evaluation.latency_ms:.2f} |"
            )

            if evaluation.intent_correct is not None:

                lines.append(
                    f"| Predicted Intent | {evaluation.predicted_intent} |"
                )

                lines.append(
                    f"| Expected Intent | {evaluation.expected_intent} |"
                )

                lines.append(
                    f"| Intent Correct | {evaluation.intent_correct} |"
                )

            if evaluation.category_correct is not None:

                lines.append(
                    f"| Predicted Category | {evaluation.predicted_category} |"
                )

                lines.append(
                    f"| Expected Category | {evaluation.expected_category} |"
                )

                lines.append(
                    f"| Category Correct | {evaluation.category_correct} |"
                )

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

        # ======================================================
        # Footer
        # ======================================================

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(
            "_Generated automatically by the KnowledgeVault Evaluation Framework._"
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        output_path.write_text(
            "\n".join(lines),
            encoding="utf-8"
        )