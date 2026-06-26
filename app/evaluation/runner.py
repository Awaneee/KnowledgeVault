"""
Evaluation Runner

Coordinates the complete evaluation pipeline.

Benchmark Loader
        ↓
Semantic Adapter
Intent Adapter
Hybrid Adapter
        ↓
Retrieval Results
        ↓
Metrics
        ↓
Evaluation Report
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from app.evaluation.adapters.semantic import SemanticAdapter
from app.evaluation.adapters.intent import IntentAdapter
from app.evaluation.adapters.hybrid import HybridAdapter

from app.evaluation.benchmark.loader import BenchmarkLoader

from app.evaluation.constants import DEFAULT_K

from app.evaluation.models import (
    BenchmarkQuery,
    EvaluationReport,
    QueryEvaluation,
    RetrievalResult,
    RetrievalStrategy,
    StrategySummary,
)

from app.evaluation.metrics.retrieval import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
    hit_rate,
)

from app.evaluation.metrics.classification import (
    intent_accuracy,
    category_accuracy,
)

from app.evaluation.metrics.latency import (
    average_latency,
    median_latency,
    p95_latency,
    max_latency,
)


class EvaluationRunner:

    def __init__(
        self,
        db: Session,
        user_id: int,
        benchmark_path: str,
        k: int = DEFAULT_K,
    ):

        self.db = db
        self.user_id = user_id
        self.k = k

        self.benchmark: list[
            BenchmarkQuery
        ] = BenchmarkLoader.load(
            benchmark_path
        )

        self.adapters = [

            SemanticAdapter(
                db=db,
                user_id=user_id,
            ),

            IntentAdapter(
                db=db,
                user_id=user_id,
            ),

            HybridAdapter(
                db=db,
                user_id=user_id,
            ),
        ]

    ####################################################################
    # Public API
    ####################################################################

    def run(self) -> EvaluationReport:

        summaries = []
        evaluations = []

        for adapter in self.adapters:

            adapter_results = []

            for benchmark in self.benchmark:

                retrieval_result = adapter.run(
                    benchmark
                )

                evaluation = self._evaluate_query(
                    benchmark,
                    retrieval_result,
                )

                adapter_results.append(
                    evaluation
                )

            summaries.append(

                self._summarize(

                    strategy=adapter.strategy,

                    evaluations=adapter_results,

                )

            )

            evaluations.extend(
                adapter_results
            )

        return EvaluationReport(

            run_id=str(uuid4()),

            created_at=datetime.utcnow().isoformat(),

            k=self.k,

            total_queries=len(self.benchmark),

            summaries=summaries,

            evaluations=evaluations,

        )

    ####################################################################
    # Query Evaluation
    ####################################################################

    def _evaluate_query(

        self,

        benchmark: BenchmarkQuery,

        retrieval: RetrievalResult,

    ) -> QueryEvaluation:

        precision = precision_at_k(

            retrieval.retrieved_note_ids,

            benchmark.relevant_note_ids,

            self.k,

        )

        recall = recall_at_k(

            retrieval.retrieved_note_ids,

            benchmark.relevant_note_ids,

            self.k,

        )

        rr = reciprocal_rank(

            retrieval.retrieved_note_ids,

            benchmark.relevant_note_ids,

        )

        hit = hit_rate(

            retrieval.retrieved_note_ids,

            benchmark.relevant_note_ids,

            self.k,

        )

        intent_correct = None

        if retrieval.predicted_intent is not None:

            intent_correct = (

                retrieval.predicted_intent.strip().lower()

                == benchmark.expected_intent.strip().lower()

            )

        category_correct = None

        if retrieval.predicted_category is not None:

            category_correct = (

                retrieval.predicted_category.strip().lower()

                == benchmark.expected_category.strip().lower()

            )

        return QueryEvaluation(

            benchmark_id=benchmark.id,

            strategy=retrieval.strategy,

            query=benchmark.query,

            difficulty=benchmark.difficulty,

            precision_at_k=precision,

            recall_at_k=recall,

            hit=hit,

            reciprocal_rank=rr,

            intent_correct=intent_correct,

            category_correct=category_correct,

            latency_ms=retrieval.latency_ms,

            relevant_note_ids=benchmark.relevant_note_ids,

            retrieved_note_ids=retrieval.retrieved_note_ids,

            predicted_intent=retrieval.predicted_intent,

            predicted_category=retrieval.predicted_category,

            expected_intent=benchmark.expected_intent,

            expected_category=benchmark.expected_category,

            error=retrieval.error,

        )

    ####################################################################
    # Strategy Summary
    ####################################################################
    def _summarize(
        self,
        strategy: RetrievalStrategy,
        evaluations: list[QueryEvaluation],
    ) -> StrategySummary:

        if not evaluations:

            return StrategySummary(
                strategy=strategy,
                query_count=0,
                mean_precision_at_k=0.0,
                mean_recall_at_k=0.0,
                hit_rate=0.0,
                mrr=0.0,
                intent_accuracy=None,
                category_accuracy=None,
                avg_latency_ms=0.0,
                median_latency_ms=0.0,
                p95_latency_ms=0.0,
                max_latency_ms=0.0,
                error_count=0,
            )

        precisions = [
            e.precision_at_k
            for e in evaluations
        ]

        recalls = [
            e.recall_at_k
            for e in evaluations
        ]

        hit_values = [
            1.0 if e.hit else 0.0
            for e in evaluations
        ]

        reciprocal_ranks = [
            e.reciprocal_rank
            for e in evaluations
        ]

        latencies = [
            e.latency_ms
            for e in evaluations
        ]

        predicted_intents = []
        expected_intents = []

        predicted_categories = []
        expected_categories = []

        for e in evaluations:

            if e.intent_correct is not None:

                predicted_intents.append(
                    e.predicted_intent
                )

                expected_intents.append(
                    e.expected_intent
                )

            if e.category_correct is not None:

                predicted_categories.append(
                    e.predicted_category
                )

                expected_categories.append(
                    e.expected_category
                )

        intent_acc = None

        if predicted_intents:

            intent_acc = intent_accuracy(
                predicted_intents,
                expected_intents,
            )

        category_acc = None

        if predicted_categories:

            category_acc = category_accuracy(
                predicted_categories,
                expected_categories,
            )

        return StrategySummary(

            strategy=strategy,

            query_count=len(evaluations),

            mean_precision_at_k=
                sum(precisions) / len(precisions),

            mean_recall_at_k=
                sum(recalls) / len(recalls),

            hit_rate=
                sum(hit_values) / len(hit_values),

            mrr=
                sum(reciprocal_ranks)
                / len(reciprocal_ranks),

            intent_accuracy=intent_acc,

            category_accuracy=category_acc,

            avg_latency_ms=
                average_latency(latencies),

            median_latency_ms=
                median_latency(latencies),

            p95_latency_ms=
                p95_latency(latencies),

            max_latency_ms=
                max_latency(latencies),

            error_count=sum(
                1
                for e in evaluations
                if e.error is not None
            ),
        )


####################################################################
# CLI
####################################################################


def main():

    from app.database.session import SessionLocal

    db = SessionLocal()

    try:

        runner = EvaluationRunner(

            db=db,

            user_id=1,

            benchmark_path="app/evaluation/benchmark/benchmark.json",

        )

        report = runner.run()

        print()

        print("=" * 70)

        print("KnowledgeVault Evaluation Report")

        print("=" * 70)

        print()

        for summary in report.summaries:

            print(summary.strategy.value.upper())

            print("-" * 40)

            print(
                f"Queries             : {summary.query_count}"
            )

            print(
                f"Precision@{report.k:<2}      : {summary.mean_precision_at_k:.3f}"
            )

            print(
                f"Recall@{report.k:<2}         : {summary.mean_recall_at_k:.3f}"
            )

            print(
                f"Hit Rate            : {summary.hit_rate:.3f}"
            )

            print(
                f"MRR                 : {summary.mrr:.3f}"
            )

            if summary.intent_accuracy is not None:

                print(
                    f"Intent Accuracy     : {summary.intent_accuracy:.3f}"
                )

            if summary.category_accuracy is not None:

                print(
                    f"Category Accuracy   : {summary.category_accuracy:.3f}"
                )

            print(
                f"Average Latency(ms) : {summary.avg_latency_ms:.2f}"
            )

            print(
                f"Median Latency(ms)  : {summary.median_latency_ms:.2f}"
            )

            print(
                f"P95 Latency(ms)     : {summary.p95_latency_ms:.2f}"
            )

            print(
                f"Max Latency(ms)     : {summary.max_latency_ms:.2f}"
            )

            print(
                f"Errors              : {summary.error_count}"
            )

            print()

        print("=" * 70)

    finally:

        db.close()


if __name__ == "__main__":
    main()