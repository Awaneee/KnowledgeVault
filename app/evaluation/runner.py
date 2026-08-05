"""
Evaluation Runner

Coordinates the complete evaluation pipeline.

Benchmark Loader
        ↓
Semantic Adapter
Intent Adapter
Hybrid Adapter
Rerank Adapter
        ↓
Retrieval Results
        ↓
Metrics (Precision@K, Recall@K, MRR, nDCG, MAP, R-Precision)
Bootstrap confidence intervals
Per-difficulty and per-intent breakdowns
Strategy comparisons with statistical significance
        ↓
Evaluation Report
"""

from __future__ import annotations

import subprocess
from collections import defaultdict
from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy.orm import Session

from app.evaluation.adapters.bm25 import BM25Adapter, HybridBM25Adapter
from app.evaluation.adapters.chunk_semantic import ChunkSemanticAdapter
from app.evaluation.adapters.hybrid import HybridAdapter
from app.evaluation.adapters.hybrid_no_intent import HybridNoIntentAdapter
from app.evaluation.adapters.intent import IntentAdapter
from app.evaluation.adapters.rerank import RerankAdapter
from app.evaluation.adapters.semantic import SemanticAdapter
from app.evaluation.benchmark.loader import BenchmarkLoader
from app.evaluation.constants import DEFAULT_K
from app.evaluation.models import (
    BenchmarkQuery,
    EvaluationReport,
    QueryEvaluation,
    RetrievalResult,
    RetrievalStrategy,
    StrategyComparison,
    StrategySummary,
)
from app.evaluation.metrics.classification import (
    canonicalize_category_name,
    category_accuracy,
    intent_accuracy,
)
from app.evaluation.metrics.latency import (
    average_latency,
    max_latency,
    median_latency,
    p95_latency,
)
from app.evaluation.metrics.retrieval import (
    average_precision_at_k,
    hit_rate,
    ndcg_at_k,
    precision_at_k,
    r_precision,
    recall_at_k,
    reciprocal_rank,
)
from app.evaluation.metrics.statistics import (
    bootstrap_delta_ci,
    bootstrap_mean_ci,
    wilcoxon_p_value,
)


def _git_commit() -> Optional[str]:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
        )
        return out.decode().strip()
    except Exception:
        return None


class EvaluationRunner:

    def __init__(
        self,
        db: Session,
        user_id: int,
        benchmark_path: str,
        k: int = DEFAULT_K,
        total_note_count: Optional[int] = None,
    ):
        self.db = db
        self.user_id = user_id
        self.k = k
        self.total_note_count = total_note_count  # for corpus coverage; None = unknown

        self.benchmark: list[BenchmarkQuery] = BenchmarkLoader.load(benchmark_path)
        self.benchmark_manifest: dict = BenchmarkLoader.load_manifest(benchmark_path)

        self.adapters = [
            SemanticAdapter(db=db, user_id=user_id),
            IntentAdapter(db=db, user_id=user_id),
            HybridAdapter(db=db, user_id=user_id),
            RerankAdapter(db=db, user_id=user_id),
            BM25Adapter(db=db, user_id=user_id),
            HybridBM25Adapter(db=db, user_id=user_id),
            # Intent-arm ablation adapters (Session 1 — 2026-08-04)
            ChunkSemanticAdapter(db=db, user_id=user_id),
            HybridNoIntentAdapter(db=db, user_id=user_id),
        ]

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    def run(self) -> EvaluationReport:
        summaries: list[StrategySummary] = []
        evaluations: list[QueryEvaluation] = []

        # Track all retrieved note IDs across all strategies for corpus coverage.
        all_retrieved_ids: set[int] = set()

        per_strategy_rr: dict[RetrievalStrategy, list[float]] = {}
        per_strategy_hit: dict[RetrievalStrategy, list[float]] = {}
        per_strategy_recall: dict[RetrievalStrategy, list[float]] = {}
        per_strategy_ndcg: dict[RetrievalStrategy, list[float]] = {}

        for adapter in self.adapters:
            adapter_results: list[QueryEvaluation] = []

            for benchmark in self.benchmark:
                retrieval_result = adapter.run(benchmark)
                evaluation = self._evaluate_query(benchmark, retrieval_result)
                adapter_results.append(evaluation)
                all_retrieved_ids.update(retrieval_result.retrieved_note_ids)

            summary = self._summarize(
                strategy=adapter.strategy,
                evaluations=adapter_results,
            )
            summaries.append(summary)
            evaluations.extend(adapter_results)

            per_strategy_rr[adapter.strategy] = [e.reciprocal_rank for e in adapter_results]
            per_strategy_hit[adapter.strategy] = [1.0 if e.hit else 0.0 for e in adapter_results]
            per_strategy_recall[adapter.strategy] = [e.recall_at_k for e in adapter_results]
            per_strategy_ndcg[adapter.strategy] = [e.ndcg_at_k for e in adapter_results]

        # Corpus coverage
        corpus_coverage = 0.0
        if self.total_note_count and self.total_note_count > 0:
            corpus_coverage = len(all_retrieved_ids) / self.total_note_count

        # Strategy comparisons
        comparisons = self._compute_comparisons(
            per_strategy_rr,
            per_strategy_hit,
            per_strategy_recall,
            per_strategy_ndcg,
        )

        return EvaluationReport(
            run_id=str(uuid4()),
            created_at=datetime.utcnow().isoformat(),
            k=self.k,
            total_queries=len(self.benchmark),
            summaries=summaries,
            evaluations=evaluations,
            benchmark_version=self.benchmark_manifest.get("version", "unknown"),
            corpus_coverage=round(corpus_coverage, 4),
            git_commit=_git_commit(),
            strategy_comparisons=comparisons,
        )

    # ------------------------------------------------------------------ #
    # Query Evaluation
    # ------------------------------------------------------------------ #

    def _evaluate_query(
        self,
        benchmark: BenchmarkQuery,
        retrieval: RetrievalResult,
    ) -> QueryEvaluation:

        grade_map = benchmark.graded_relevance  # None for binary relevance

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
        ndcg = ndcg_at_k(
            retrieved=retrieval.retrieved_note_ids,
            relevant=benchmark.relevant_note_ids,
            k=self.k,
        )
        ndcg_graded: Optional[float] = None
        if grade_map:
            ndcg_graded = ndcg_at_k(
                retrieved=retrieval.retrieved_note_ids,
                relevant=benchmark.relevant_note_ids,
                k=self.k,
                grade_map=grade_map,
            )

        map_k = average_precision_at_k(
            retrieval.retrieved_note_ids,
            benchmark.relevant_note_ids,
            self.k,
        )
        rprec = r_precision(
            retrieval.retrieved_note_ids,
            benchmark.relevant_note_ids,
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
                canonicalize_category_name(retrieval.predicted_category)
                == canonicalize_category_name(benchmark.expected_category)
            )

        return QueryEvaluation(
            benchmark_id=benchmark.id,
            strategy=retrieval.strategy,
            query=benchmark.query,
            difficulty=benchmark.difficulty,
            precision_at_k=precision,
            recall_at_k=recall,
            ndcg_at_k=ndcg,
            hit=hit,
            reciprocal_rank=rr,
            map_at_k=map_k,
            r_precision=rprec,
            ndcg_at_k_graded=ndcg_graded,
            retrieval_challenge=benchmark.retrieval_challenge,
            intent_correct=intent_correct,
            category_correct=category_correct,
            latency_ms=retrieval.latency_ms,
            end_to_end_latency_ms=retrieval.end_to_end_latency_ms,
            relevant_note_ids=benchmark.relevant_note_ids,
            retrieved_note_ids=retrieval.retrieved_note_ids,
            predicted_intent=retrieval.predicted_intent,
            predicted_category=retrieval.predicted_category,
            expected_intent=benchmark.expected_intent,
            expected_category=benchmark.expected_category,
            error=retrieval.error,
        )

    # ------------------------------------------------------------------ #
    # Strategy Summary
    # ------------------------------------------------------------------ #

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
                mean_ndcg_at_k=0.0,
                hit_rate=0.0,
                mrr=0.0,
                avg_latency_ms=0.0,
                median_latency_ms=0.0,
                p95_latency_ms=0.0,
                max_latency_ms=0.0,
                error_count=0,
            )

        precisions = [e.precision_at_k for e in evaluations]
        recalls = [e.recall_at_k for e in evaluations]
        hit_values = [1.0 if e.hit else 0.0 for e in evaluations]
        reciprocal_ranks = [e.reciprocal_rank for e in evaluations]
        latencies = [e.latency_ms for e in evaluations]
        ndcgs = [e.ndcg_at_k for e in evaluations]
        maps = [e.map_at_k for e in evaluations]
        rprecs = [e.r_precision for e in evaluations]
        e2e_latencies = [
            e.end_to_end_latency_ms
            for e in evaluations
            if e.end_to_end_latency_ms is not None
        ]
        graded_ndcgs = [
            e.ndcg_at_k_graded
            for e in evaluations
            if e.ndcg_at_k_graded is not None
        ]

        predicted_intents: list[str] = []
        expected_intents: list[str] = []
        predicted_categories: list[str] = []
        expected_categories: list[str] = []

        for e in evaluations:
            if e.intent_correct is not None:
                predicted_intents.append(e.predicted_intent or "")
                expected_intents.append(e.expected_intent)
            if e.category_correct is not None:
                predicted_categories.append(e.predicted_category or "")
                expected_categories.append(e.expected_category)

        intent_acc = (
            intent_accuracy(predicted_intents, expected_intents)
            if predicted_intents else None
        )
        category_acc = (
            category_accuracy(predicted_categories, expected_categories)
            if predicted_categories else None
        )

        mrr_val = sum(reciprocal_ranks) / len(reciprocal_ranks)
        hit_val = sum(hit_values) / len(hit_values)
        prec_val = sum(precisions) / len(precisions)
        rec_val = sum(recalls) / len(recalls) if recalls else 0.0

        # Bootstrap CIs (only meaningful with ≥ 5 samples)
        mrr_ci = bootstrap_mean_ci(reciprocal_ranks) if len(reciprocal_ranks) >= 5 else None
        hit_ci = bootstrap_mean_ci(hit_values) if len(hit_values) >= 5 else None
        prec_ci = bootstrap_mean_ci(precisions) if len(precisions) >= 5 else None
        rec_ci = bootstrap_mean_ci(recalls) if len(recalls) >= 5 else None

        # Per-difficulty breakdown
        difficulty_breakdown = self._breakdown_by(evaluations, key="difficulty")
        # Per-intent breakdown
        intent_breakdown = self._breakdown_by(evaluations, key="expected_intent")

        return StrategySummary(
            strategy=strategy,
            query_count=len(evaluations),
            mean_precision_at_k=prec_val,
            mean_recall_at_k=rec_val,
            mean_ndcg_at_k=sum(ndcgs) / len(ndcgs) if ndcgs else 0.0,
            hit_rate=hit_val,
            mrr=mrr_val,
            intent_accuracy=intent_acc,
            category_accuracy=category_acc,
            avg_latency_ms=average_latency(latencies),
            avg_end_to_end_latency_ms=(
                sum(e2e_latencies) / len(e2e_latencies) if e2e_latencies else None
            ),
            median_latency_ms=median_latency(latencies),
            p95_latency_ms=p95_latency(latencies),
            max_latency_ms=max_latency(latencies),
            error_count=sum(1 for e in evaluations if e.error is not None),
            mean_map_at_k=sum(maps) / len(maps) if maps else 0.0,
            mean_r_precision=sum(rprecs) / len(rprecs) if rprecs else 0.0,
            mean_ndcg_at_k_graded=(
                sum(graded_ndcgs) / len(graded_ndcgs) if graded_ndcgs else None
            ),
            mrr_ci=mrr_ci,
            hit_rate_ci=hit_ci,
            precision_ci=prec_ci,
            recall_ci=rec_ci,
            difficulty_breakdown=difficulty_breakdown,
            intent_breakdown=intent_breakdown,
        )

    @staticmethod
    def _breakdown_by(
        evaluations: list[QueryEvaluation],
        key: str,  # "difficulty" or "expected_intent"
    ) -> dict[str, dict[str, float]]:
        """
        Return per-group metric means.

        Returns dict keyed by group name, each value a dict with
        {mrr, hit_rate, precision, recall} means for that group.
        """
        groups: dict[str, list[QueryEvaluation]] = defaultdict(list)
        for e in evaluations:
            group_val = getattr(e, key, None) or "unknown"
            groups[group_val].append(e)

        result: dict[str, dict[str, float]] = {}
        for group, group_evals in sorted(groups.items()):
            n = len(group_evals)
            result[group] = {
                "count": n,
                "mrr": sum(e.reciprocal_rank for e in group_evals) / n,
                "hit_rate": sum(1.0 if e.hit else 0.0 for e in group_evals) / n,
                "precision": sum(e.precision_at_k for e in group_evals) / n,
                "recall": sum(e.recall_at_k for e in group_evals) / n,
            }
        return result

    # ------------------------------------------------------------------ #
    # Strategy comparisons
    # ------------------------------------------------------------------ #

    def _compute_comparisons(
        self,
        per_strategy_rr: dict[RetrievalStrategy, list[float]],
        per_strategy_hit: dict[RetrievalStrategy, list[float]],
        per_strategy_recall: dict[RetrievalStrategy, list[float]] | None = None,
        per_strategy_ndcg: dict[RetrievalStrategy, list[float]] | None = None,
    ) -> list[StrategyComparison]:
        """
        Compute pairwise comparisons for all registered strategy pairs.

        MRR and hit-rate are always computed (they drive the recommendation).
        Recall@K and nDCG@K CIs are also computed when per-query arrays are
        provided — both use the same bootstrap_delta_ci / wilcoxon_p_value
        functions; no new statistics code is introduced.
        """
        pairs = [
            (RetrievalStrategy.SEMANTIC, RetrievalStrategy.HYBRID),
            (RetrievalStrategy.HYBRID, RetrievalStrategy.RERANK),
            # BM25 ablation: sparse alone vs. dense baseline
            (RetrievalStrategy.SEMANTIC, RetrievalStrategy.BM25),
            # BM25 RRF vs. production baseline
            (RetrievalStrategy.HYBRID, RetrievalStrategy.HYBRID_BM25),
            # Intent-arm ablation (Session 1 — 2026-08-04):
            #   full delta: chunk-level ANN vs. full hybrid pipeline
            (RetrievalStrategy.CHUNK_SEMANTIC, RetrievalStrategy.HYBRID),
            #   granularity-only: chunk-level ANN vs. note-level ANN (no boost in either)
            (RetrievalStrategy.CHUNK_SEMANTIC, RetrievalStrategy.HYBRID_NO_INTENT),
            #   boost-only: note-level hybrid with and without the 0–0.12 additive boost
            (RetrievalStrategy.HYBRID_NO_INTENT, RetrievalStrategy.HYBRID),
        ]
        comparisons: list[StrategyComparison] = []

        for baseline_strat, candidate_strat in pairs:
            rr_base = per_strategy_rr.get(baseline_strat)
            rr_cand = per_strategy_rr.get(candidate_strat)
            hit_base = per_strategy_hit.get(baseline_strat)
            hit_cand = per_strategy_hit.get(candidate_strat)

            if not rr_base or not rr_cand:
                continue

            mrr_lo, mrr_hi, mrr_sig = bootstrap_delta_ci(rr_cand, rr_base)
            hit_lo, hit_hi, hit_sig = bootstrap_delta_ci(hit_cand, hit_base)
            delta_mrr = sum(rr_cand) / len(rr_cand) - sum(rr_base) / len(rr_base)
            delta_hit = sum(hit_cand) / len(hit_cand) - sum(hit_base) / len(hit_base)

            p_mrr = wilcoxon_p_value(rr_cand, rr_base)
            p_hit = wilcoxon_p_value(hit_cand, hit_base)

            if mrr_sig and delta_mrr > 0:
                recommendation = "approve_candidate"
            elif mrr_sig and delta_mrr < 0:
                recommendation = "keep_baseline"
            else:
                recommendation = "insufficient_evidence"

            # --- Optional recall and nDCG CIs (no new stats code) -----------
            rec_base = (per_strategy_recall or {}).get(baseline_strat)
            rec_cand = (per_strategy_recall or {}).get(candidate_strat)
            ndcg_base = (per_strategy_ndcg or {}).get(baseline_strat)
            ndcg_cand = (per_strategy_ndcg or {}).get(candidate_strat)

            delta_recall = recall_lo = recall_hi = None
            recall_sig = p_recall = None
            if rec_base and rec_cand:
                recall_lo, recall_hi, recall_sig = bootstrap_delta_ci(rec_cand, rec_base)
                delta_recall = sum(rec_cand) / len(rec_cand) - sum(rec_base) / len(rec_base)
                p_recall = wilcoxon_p_value(rec_cand, rec_base)

            delta_ndcg = ndcg_lo = ndcg_hi = None
            ndcg_sig = p_ndcg = None
            if ndcg_base and ndcg_cand:
                ndcg_lo, ndcg_hi, ndcg_sig = bootstrap_delta_ci(ndcg_cand, ndcg_base)
                delta_ndcg = sum(ndcg_cand) / len(ndcg_cand) - sum(ndcg_base) / len(ndcg_base)
                p_ndcg = wilcoxon_p_value(ndcg_cand, ndcg_base)

            comparisons.append(StrategyComparison(
                baseline=baseline_strat,
                candidate=candidate_strat,
                delta_mrr=round(delta_mrr, 4),
                mrr_ci_lower=round(mrr_lo, 4),
                mrr_ci_upper=round(mrr_hi, 4),
                mrr_significant=mrr_sig,
                delta_hit_rate=round(delta_hit, 4),
                hit_rate_ci_lower=round(hit_lo, 4),
                hit_rate_ci_upper=round(hit_hi, 4),
                hit_rate_significant=hit_sig,
                p_value_mrr=round(p_mrr, 4) if p_mrr is not None else None,
                p_value_hit_rate=round(p_hit, 4) if p_hit is not None else None,
                delta_recall_at_k=round(delta_recall, 4) if delta_recall is not None else None,
                recall_ci_lower=round(recall_lo, 4) if recall_lo is not None else None,
                recall_ci_upper=round(recall_hi, 4) if recall_hi is not None else None,
                recall_significant=recall_sig,
                p_value_recall=round(p_recall, 4) if p_recall is not None else None,
                delta_ndcg_at_k=round(delta_ndcg, 4) if delta_ndcg is not None else None,
                ndcg_ci_lower=round(ndcg_lo, 4) if ndcg_lo is not None else None,
                ndcg_ci_upper=round(ndcg_hi, 4) if ndcg_hi is not None else None,
                ndcg_significant=ndcg_sig,
                p_value_ndcg=round(p_ndcg, 4) if p_ndcg is not None else None,
                recommendation=recommendation,
            ))

        return comparisons


# ------------------------------------------------------------------ #
# CLI
# ------------------------------------------------------------------ #

def main() -> None:

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
        print(f"Benchmark version : {report.benchmark_version}")
        print(f"Git commit        : {report.git_commit or 'unknown'}")
        print(f"Corpus coverage   : {report.corpus_coverage:.1%}")
        print()

        for summary in report.summaries:
            print(summary.strategy.value.upper())
            print("-" * 40)
            print(f"Queries    : {summary.query_count}")
            print(f"Precision@{report.k} : {summary.mean_precision_at_k:.3f}")
            print(f"Recall@{report.k}    : {summary.mean_recall_at_k:.3f}")
            print(f"Hit Rate   : {summary.hit_rate:.3f}")

            ci = summary.mrr_ci
            ci_str = f"  [{ci[0]:.3f}, {ci[1]:.3f}]" if ci else ""
            print(f"MRR        : {summary.mrr:.3f}{ci_str}")

            print(f"MAP@{report.k}      : {summary.mean_map_at_k:.3f}")
            print(f"R-Prec     : {summary.mean_r_precision:.3f}")
            print(f"nDCG@{report.k}     : {summary.mean_ndcg_at_k:.3f}")
            print(f"Avg Latency: {summary.avg_latency_ms:.2f} ms")
            print(f"Errors     : {summary.error_count}")
            print()

        if report.strategy_comparisons:
            print("Strategy Comparisons")
            print("-" * 40)
            for comp in report.strategy_comparisons:
                sig = "SIGNIFICANT" if comp.mrr_significant else "not significant"
                print(
                    f"  {comp.candidate.value.upper()} vs {comp.baseline.value.upper()}: "
                    f"ΔMRR={comp.delta_mrr:+.4f} "
                    f"[{comp.mrr_ci_lower:.4f},{comp.mrr_ci_upper:.4f}] "
                    f"{sig} → {comp.recommendation}"
                )
                if comp.delta_recall_at_k is not None:
                    rec_sig = "sig" if comp.recall_significant else "n.s."
                    ndcg_sig = "sig" if comp.ndcg_significant else "n.s."
                    print(
                        f"    ΔRecall={comp.delta_recall_at_k:+.4f} "
                        f"[{comp.recall_ci_lower:.4f},{comp.recall_ci_upper:.4f}] {rec_sig}  "
                        f"ΔnDCG={comp.delta_ndcg_at_k:+.4f} "
                        f"[{comp.ndcg_ci_lower:.4f},{comp.ndcg_ci_upper:.4f}] {ndcg_sig}"
                    )
            print()

        print("=" * 70)

        # Export
        import csv as _csv
        with open("app/evaluation/benchmark/results.csv", "w", newline="") as f:
            writer = _csv.writer(f)
            writer.writerow([
                "Strategy", "Queries", "Precision@K", "Recall@K", "nDCG@K",
                "Hit Rate", "MRR", "MRR_CI_Lower", "MRR_CI_Upper",
                "MAP@K", "R-Precision",
                "Intent Acc", "Category Acc",
                "Avg Latency(ms)", "Avg E2E Latency(ms)",
            ])
            for summary in report.summaries:
                ci = summary.mrr_ci
                writer.writerow([
                    summary.strategy.value,
                    summary.query_count,
                    f"{summary.mean_precision_at_k:.3f}",
                    f"{summary.mean_recall_at_k:.3f}",
                    f"{summary.mean_ndcg_at_k:.3f}",
                    f"{summary.hit_rate:.3f}",
                    f"{summary.mrr:.3f}",
                    f"{ci[0]:.3f}" if ci else "N/A",
                    f"{ci[1]:.3f}" if ci else "N/A",
                    f"{summary.mean_map_at_k:.3f}",
                    f"{summary.mean_r_precision:.3f}",
                    f"{summary.intent_accuracy:.3f}" if summary.intent_accuracy is not None else "N/A",
                    f"{summary.category_accuracy:.3f}" if summary.category_accuracy is not None else "N/A",
                    f"{summary.avg_latency_ms:.2f}",
                    f"{summary.avg_end_to_end_latency_ms:.2f}" if summary.avg_end_to_end_latency_ms is not None else "N/A",
                ])

        print("\nResults exported to app/evaluation/benchmark/results.csv")

    finally:
        db.close()


if __name__ == "__main__":
    main()
