"""
Ask evaluation report generators.

Produces GitHub-style Markdown and CSV reports from AskEvalReport.
No metrics are computed here — all numbers come from the report object.
"""

from __future__ import annotations

import csv
from pathlib import Path

from app.evaluation.ask.models import AskEvalReport, AskEvalResult


class AskMarkdownReport:
    """Generates a Markdown evaluation report."""

    @staticmethod
    def generate(report: AskEvalReport, output_path: str | Path) -> None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        lines: list[str] = []

        # Header
        lines += [
            "# KnowledgeVault — Ask Endpoint Evaluation Report",
            "",
            f"**Run ID:** `{report.run_id}`",
            f"**Created:** {report.created_at}",
            f"**Total Queries:** {report.total_queries}",
            f"**Estimated Total Cost:** ${report.total_estimated_cost_usd:.6f} USD",
            "",
        ]

        # Overall averages
        lines += [
            "## Overall Averages",
            "",
            "| Metric | Score |",
            "|---|---|",
            f"| Correctness | {report.avg_correctness:.3f} |",
            f"| Groundedness | {report.avg_groundedness:.3f} |",
            f"| Faithfulness | {report.avg_faithfulness:.3f} |",
            f"| Hallucination (1=none) | {report.avg_hallucination:.3f} |",
            f"| Completeness | {report.avg_completeness:.3f} |",
            f"| **Overall (Weighted)** | **{report.avg_overall:.3f}** |",
            "",
            "### Latency",
            "",
            "| Metric | ms |",
            "|---|---|",
            f"| Avg Retrieval | {report.avg_retrieval_ms:.1f} |",
            f"| Avg LLM | {report.avg_llm_ms:.1f} |",
            f"| Avg End-to-End | {report.avg_total_ms:.1f} |",
            "",
        ]

        # Per-category breakdown
        lines += ["## Per-Category Breakdown", ""]
        lines += [
            "| Category | N | Correctness | Groundedness | Faithfulness | Hallucination | Completeness | Overall | Avg ms |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        for cat in report.category_summaries:
            lines.append(
                f"| {cat.category} | {cat.query_count} "
                f"| {cat.avg_correctness:.3f} | {cat.avg_groundedness:.3f} "
                f"| {cat.avg_faithfulness:.3f} | {cat.avg_hallucination:.3f} "
                f"| {cat.avg_completeness:.3f} | {cat.avg_overall:.3f} "
                f"| {cat.avg_total_ms:.1f} |"
            )
        lines.append("")

        # Root cause distribution
        if report.root_cause_counts:
            lines += ["## Failure Root Cause Distribution", ""]
            lines += ["| Root Cause | Count |", "|---|---|"]
            for cause, count in sorted(
                report.root_cause_counts.items(), key=lambda x: -x[1]
            ):
                lines.append(f"| {cause} | {count} |")
            lines.append("")

        # Hardest queries
        lines += ["## Hardest Queries (Lowest Overall Score)", ""]
        hard_results = {r.query_id: r for r in report.results}
        for qid in report.hardest_queries:
            r = hard_results.get(qid)
            if r:
                score = r.scores.weighted_overall if r.scores else 0.0
                lines.append(
                    f"- **[{qid}]** `{r.question}` — Overall: {score:.3f} "
                    f"| Root cause: {r.root_cause.value if r.root_cause else 'n/a'}"
                )
        lines.append("")

        # Easiest queries
        lines += ["## Easiest Queries (Highest Overall Score)", ""]
        for qid in reversed(report.easiest_queries):
            r = hard_results.get(qid)
            if r:
                score = r.scores.weighted_overall if r.scores else 0.0
                lines.append(f"- **[{qid}]** `{r.question}` — Overall: {score:.3f}")
        lines.append("")

        # Per-query detail
        lines += ["## Per-Query Results", ""]
        for r in report.results:
            score_str = f"{r.scores.weighted_overall:.3f}" if r.scores else "N/A"
            lines += [
                f"### [{r.query_id}] {r.question}",
                "",
                f"- **Category:** {r.category} | **Difficulty:** {r.difficulty}",
                f"- **Status:** {r.status} | **Retrieval-Only:** {r.retrieval_only}",
                f"- **Expected Notes:** {r.expected_note_ids}",
                f"- **Retrieved Notes:** {r.retrieved_note_ids}",
                f"- **Recall@Expected:** {r.recall_at_expected:.3f} | **Context Utilisation:** {r.context_utilisation:.3f}",
                f"- **Latency:** retrieval={r.retrieval_ms:.0f}ms, llm={r.llm_ms:.0f}ms, total={r.total_ms:.0f}ms",
                f"- **Cost:** ${r.estimated_cost_usd:.8f} USD",
                "",
            ]

            if r.scores:
                lines += [
                    "| Metric | Score |",
                    "|---|---|",
                    f"| Correctness | {r.scores.correctness:.3f} |",
                    f"| Groundedness | {r.scores.groundedness:.3f} |",
                    f"| Faithfulness | {r.scores.faithfulness:.3f} |",
                    f"| Hallucination | {r.scores.hallucination:.3f} |",
                    f"| Completeness | {r.scores.completeness:.3f} |",
                    f"| **Overall (Weighted)** | **{score_str}** |",
                    "",
                    f"**Justification:** {r.scores.justification}",
                    "",
                ]
                if r.scores.hallucinated_claims:
                    lines.append(f"**Hallucinated claims:** {r.scores.hallucinated_claims}")
                    lines.append("")
                if r.scores.ungrounded_claims:
                    lines.append(f"**Ungrounded claims:** {r.scores.ungrounded_claims}")
                    lines.append("")

            if r.root_cause:
                lines.append(f"**Root cause:** `{r.root_cause.value}`")
                lines.append("")

            if r.error:
                lines += ["**Error:**", f"```", r.error, "```", ""]

            lines += [
                f"**Answer:** {r.answer[:400]}{'...' if len(r.answer) > 400 else ''}",
                "",
                "---",
                "",
            ]

        # Footer
        lines += [
            "",
            "---",
            "_Generated automatically by the KnowledgeVault Ask Evaluation Framework._",
        ]

        output_path.write_text("\n".join(lines), encoding="utf-8")


class AskCSVReport:
    """Generates a flat CSV with one row per query."""

    FIELDNAMES = [
        "query_id", "question", "category", "difficulty", "status",
        "retrieval_only", "answer_preview",
        "correctness", "groundedness", "faithfulness",
        "hallucination", "completeness", "overall_weighted",
        "recall_at_expected", "context_utilisation",
        "retrieved_note_ids", "expected_note_ids",
        "retrieval_ms", "llm_ms", "total_ms",
        "estimated_prompt_tokens", "estimated_completion_tokens",
        "estimated_cost_usd", "root_cause", "error",
    ]

    @classmethod
    def generate(cls, report: AskEvalReport, output_path: str | Path) -> None:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with output_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=cls.FIELDNAMES)
            writer.writeheader()
            for r in report.results:
                writer.writerow(cls._to_row(r))

    @staticmethod
    def _to_row(r: AskEvalResult) -> dict:
        scores = r.scores
        return {
            "query_id": r.query_id,
            "question": r.question,
            "category": r.category,
            "difficulty": r.difficulty,
            "status": r.status,
            "retrieval_only": r.retrieval_only,
            "answer_preview": r.answer[:200].replace("\n", " "),
            "correctness":    f"{scores.correctness:.4f}"  if scores else "",
            "groundedness":   f"{scores.groundedness:.4f}" if scores else "",
            "faithfulness":   f"{scores.faithfulness:.4f}" if scores else "",
            "hallucination":  f"{scores.hallucination:.4f}" if scores else "",
            "completeness":   f"{scores.completeness:.4f}" if scores else "",
            "overall_weighted": f"{scores.weighted_overall:.4f}" if scores else "",
            "recall_at_expected": f"{r.recall_at_expected:.4f}",
            "context_utilisation": f"{r.context_utilisation:.4f}",
            "retrieved_note_ids": ",".join(str(n) for n in r.retrieved_note_ids),
            "expected_note_ids": ",".join(str(n) for n in r.expected_note_ids),
            "retrieval_ms": f"{r.retrieval_ms:.2f}",
            "llm_ms": f"{r.llm_ms:.2f}",
            "total_ms": f"{r.total_ms:.2f}",
            "estimated_prompt_tokens": r.estimated_prompt_tokens,
            "estimated_completion_tokens": r.estimated_completion_tokens,
            "estimated_cost_usd": f"{r.estimated_cost_usd:.8f}",
            "root_cause": r.root_cause.value if r.root_cause else "",
            "error": r.error or "",
        }
