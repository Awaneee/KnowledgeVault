"""
CSV report generator.

Exports every evaluated query into a CSV file for later analysis
(Excel, pandas, Power BI, etc.).

No metrics are calculated here.
"""

from __future__ import annotations

import csv
from pathlib import Path

from app.evaluation.models import EvaluationReport


class CSVReport:

    @staticmethod
    def generate(
        report: EvaluationReport,
        output_path: str | Path,
    ) -> None:

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_path,
            "w",
            newline="",
            encoding="utf-8",
        ) as csvfile:

            writer = csv.writer(csvfile)

            # =====================================================
            # Header
            # =====================================================

            writer.writerow(
                [
                    "benchmark_id",
                    "strategy",
                    "query",
                    "difficulty",
                    "precision_at_k",
                    "recall_at_k",
                    "hit",
                    "reciprocal_rank",
                    "latency_ms",
                    "predicted_intent",
                    "expected_intent",
                    "intent_correct",
                    "predicted_category",
                    "expected_category",
                    "category_correct",
                    "relevant_note_ids",
                    "retrieved_note_ids",
                    "error",
                ]
            )

            # =====================================================
            # Rows
            # =====================================================

            for evaluation in report.evaluations:

                writer.writerow(
                    [
                        evaluation.benchmark_id,
                        evaluation.strategy.value,
                        evaluation.query,
                        evaluation.difficulty,
                        round(
                            evaluation.precision_at_k,
                            4,
                        ),
                        round(
                            evaluation.recall_at_k,
                            4,
                        ),
                        evaluation.hit,
                        round(
                            evaluation.reciprocal_rank,
                            4,
                        ),
                        round(
                            evaluation.latency_ms,
                            2,
                        ),
                        evaluation.predicted_intent,
                        evaluation.expected_intent,
                        evaluation.intent_correct,
                        evaluation.predicted_category,
                        evaluation.expected_category,
                        evaluation.category_correct,
                        ",".join(
                            map(
                                str,
                                evaluation.relevant_note_ids,
                            )
                        ),
                        ",".join(
                            map(
                                str,
                                evaluation.retrieved_note_ids,
                            )
                        ),
                        evaluation.error,
                    ]
                )