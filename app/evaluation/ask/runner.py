"""
Ask evaluation runner.

Orchestrates the end-to-end evaluation pipeline:
  1. Load gold dataset
  2. For each query: call AskService.ask_with_context()
  3. Judge the answer
  4. Classify root cause
  5. Save per-query debug artifact to disk
  6. Aggregate into AskEvalReport

Root cause classification
--------------------------
The runner applies deterministic rules after receiving judge scores to assign
the most likely root cause of a failed evaluation. Rules are applied in order
of specificity:

  EVALUATOR_FAILURE    → judge raised an exception
  RETRIEVAL_FAILURE    → recall_at_expected < 0.5 AND correctness < 0.5
  INSUFFICIENT_CONTEXT → recall ok but context_utilisation or completeness low
  HALLUCINATION        → hallucination score < 0.4
  PROMPT_CONSTRUCTION  → answer looks malformed despite good retrieval & context
  UNKNOWN              → scores are low but no specific cause identified

A query is considered "failed" when overall weighted score < 0.6.
"""

from __future__ import annotations

import json
import logging
import statistics
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from sqlalchemy.orm import Session

from app.evaluation.ask.judge import AskJudge, JudgeError, estimate_cost_usd, estimate_tokens
from app.evaluation.ask.models import (
    AskEvalReport,
    AskEvalResult,
    CategorySummary,
    ChunkArtifact,
    FailureRootCause,
    GoldAskQuery,
    JudgeScores,
)
from app.services.ask_service import AskService


logger = logging.getLogger(__name__)

# Threshold below which a query is considered "failed" for root-cause analysis
_FAILURE_THRESHOLD = 0.60


# ---------------------------------------------------------------------------
# Gold dataset loader
# ---------------------------------------------------------------------------

class GoldDatasetLoader:
    @staticmethod
    def load(path: str | Path) -> list[GoldAskQuery]:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return [GoldAskQuery(**entry) for entry in data]


# ---------------------------------------------------------------------------
# Root-cause classifier
# ---------------------------------------------------------------------------

def classify_root_cause(
    result: AskEvalResult,
    judge_error: Optional[str],
) -> FailureRootCause:
    """
    Assign the most likely root cause for a failed evaluation.

    Only called when weighted_overall < _FAILURE_THRESHOLD.
    """
    if judge_error or result.scores is None:
        return FailureRootCause.EVALUATOR_FAILURE

    scores = result.scores

    # 1. Retrieval failure: correct notes not in top-8
    if result.recall_at_expected < 0.5 and scores.correctness < 0.5:
        return FailureRootCause.RETRIEVAL_FAILURE

    # 2. Hallucination: model invented facts
    if scores.hallucination < 0.4:
        return FailureRootCause.HALLUCINATION

    # 3. Insufficient context: notes retrieved but answer lacks info
    if result.recall_at_expected >= 0.5 and scores.completeness < 0.4:
        return FailureRootCause.INSUFFICIENT_CONTEXT

    # 4. Prompt construction: retrieval ok but answer malformed/off-topic
    if (
        result.recall_at_expected >= 0.5
        and scores.groundedness >= 0.5
        and scores.correctness < 0.5
    ):
        return FailureRootCause.PROMPT_CONSTRUCTION

    return FailureRootCause.UNKNOWN


# ---------------------------------------------------------------------------
# Context utilisation estimation
# ---------------------------------------------------------------------------

def estimate_context_utilisation(answer: str, chunks: list[dict]) -> float:
    """
    Estimate what fraction of retrieved chunks contributed to the answer.

    A chunk is considered "utilised" if at least 3 consecutive words from
    its text appear in the answer (case-insensitive). This is a lightweight
    heuristic — the judge performs deeper grounding analysis.
    """
    if not chunks or not answer:
        return 0.0

    answer_lower = answer.lower()
    utilised = 0

    for chunk in chunks:
        text = chunk.get("chunk_text", "")
        words = text.lower().split()
        if len(words) < 3:
            # Short chunks: check if any word appears in the answer
            if any(w in answer_lower for w in words if len(w) > 4):
                utilised += 1
            continue
        # Check for any 3-gram overlap
        found = False
        for i in range(len(words) - 2):
            trigram = " ".join(words[i:i+3])
            if trigram in answer_lower:
                found = True
                break
        if found:
            utilised += 1

    return utilised / len(chunks)


# ---------------------------------------------------------------------------
# Recall at expected
# ---------------------------------------------------------------------------

def compute_recall_at_expected(
    retrieved_chunks: list[dict],
    expected_note_ids: list[int],
) -> float:
    """Fraction of expected note IDs present in the retrieved chunk set."""
    if not expected_note_ids:
        return 1.0  # vacuously satisfied
    retrieved_ids = {c["note_id"] for c in retrieved_chunks}
    hits = sum(1 for nid in expected_note_ids if nid in retrieved_ids)
    return hits / len(expected_note_ids)


# ---------------------------------------------------------------------------
# Debug artifact persistence
# ---------------------------------------------------------------------------

def save_debug_artifact(
    artifact_dir: Path,
    query_id: str,
    gold: GoldAskQuery,
    result_dict: dict,
    scores: Optional[JudgeScores],
    root_cause: Optional[FailureRootCause],
    judge_error: Optional[str],
) -> None:
    """
    Persist all evaluation artifacts for a single query to disk as JSON.

    Files are written to: {artifact_dir}/{query_id}_debug.json
    The artifact contains everything needed to reproduce and debug
    the evaluation result without re-running the pipeline.
    """
    artifact_dir.mkdir(parents=True, exist_ok=True)
    eval_meta = result_dict.get("_eval", {})

    artifact = {
        "query_id": query_id,
        "question": gold.question,
        "category": gold.category,
        "difficulty": gold.difficulty,
        "expected_note_ids": gold.expected_note_ids,
        "reference_answer": gold.reference_answer,
        "eval_notes": gold.eval_notes,
        "pipeline": {
            "status": result_dict.get("status"),
            "retrieval_only": result_dict.get("retrieval_only"),
            "answer": result_dict.get("answer", ""),
            "sources": result_dict.get("sources", []),
            "retrieval_ms": eval_meta.get("retrieval_ms"),
            "llm_ms": eval_meta.get("llm_ms"),
            "total_ms": eval_meta.get("total_ms"),
        },
        "context": {
            "prompt": eval_meta.get("prompt", ""),
            "retrieved_chunks": [
                {
                    "note_id": c.get("note_id"),
                    "note_title": c.get("note_title"),
                    "chunk_text": c.get("chunk_text", "")[:500],  # truncate for storage
                    "chunk_index": c.get("chunk_index"),
                    "score": c.get("score"),
                    "semantic_score": c.get("semantic_score"),
                    "intent_score": c.get("intent_score"),
                    "intent_category": c.get("intent_category"),
                }
                for c in eval_meta.get("filtered_chunks", [])
            ],
            "raw_chunk_count": len(eval_meta.get("retrieved_chunks", [])),
            "filtered_chunk_count": len(eval_meta.get("filtered_chunks", [])),
        },
        "judge": {
            "scores": scores.model_dump() if scores else None,
            "error": judge_error,
            "root_cause": root_cause.value if root_cause else None,
        },
    }

    out_path = artifact_dir / f"{query_id}_debug.json"
    out_path.write_text(json.dumps(artifact, indent=2, ensure_ascii=False), encoding="utf-8")
    logger.debug("Debug artifact saved: %s", out_path)


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

class AskEvaluationRunner:
    """
    Orchestrates the full Ask endpoint evaluation.

    Usage
    -----
    runner = AskEvaluationRunner(db_session)
    report = runner.run(user_id=1, dataset_path="...", artifact_dir="...")
    """

    def __init__(self, db: Session) -> None:
        self.db = db
        self.ask_service = AskService(db)
        self.judge = AskJudge()

    def run(
        self,
        user_id: int,
        dataset_path: str | Path,
        artifact_dir: str | Path | None = None,
        limit: int | None = None,
    ) -> AskEvalReport:
        """
        Run evaluation over the gold dataset.

        Parameters
        ----------
        user_id       DB user whose notes are searched.
        dataset_path  Path to gold_dataset.json.
        artifact_dir  If provided, per-query debug JSONs are written here.
        limit         Optional maximum number of queries to evaluate.
        """
        run_id = str(uuid.uuid4())
        created_at = datetime.now(timezone.utc).isoformat()

        gold_queries = GoldDatasetLoader.load(dataset_path)
        if limit is not None:
            gold_queries = gold_queries[:limit]
            
        artifact_path = Path(artifact_dir) if artifact_dir else None

        results: list[AskEvalResult] = []

        for i, gold in enumerate(gold_queries):
            logger.info(
                "ASK EVAL [%d/%d] query_id=%s question=%.60s",
                i + 1,
                len(gold_queries),
                gold.id,
                gold.question,
            )
            result = self._evaluate_one(gold, user_id, artifact_path)
            results.append(result)
            
            # Sleep to respect rate limits (Gemini free tier has 15 RPM limit)
            import time
            if i < len(gold_queries) - 1:
                time.sleep(8.0)

        report = self._aggregate(run_id, created_at, results)
        return report

    # ------------------------------------------------------------------
    # Per-query evaluation
    # ------------------------------------------------------------------

    def _evaluate_one(
        self,
        gold: GoldAskQuery,
        user_id: int,
        artifact_dir: Optional[Path],
    ) -> AskEvalResult:
        """Run the full pipeline + judge for a single gold query."""
        judge_error: Optional[str] = None
        scores: Optional[JudgeScores] = None
        root_cause: Optional[FailureRootCause] = None
        result_dict: dict = {}

        # Step 1 — Run Ask pipeline
        try:
            result_dict = self.ask_service.ask_with_context(gold.question, user_id)
        except Exception as exc:
            logger.exception("Pipeline error for query %s: %s", gold.id, exc)
            result_dict = {
                "status": "error",
                "answer": "",
                "sources": [],
                "retrieval_only": True,
                "_eval": {
                    "retrieved_chunks": [],
                    "filtered_chunks": [],
                    "prompt": "",
                    "retrieval_ms": 0.0,
                    "llm_ms": 0.0,
                    "total_ms": 0.0,
                },
            }
            judge_error = f"Pipeline error: {exc}"

        eval_meta = result_dict.get("_eval", {})
        raw_chunks: list[dict] = eval_meta.get("retrieved_chunks", [])
        filtered_chunks: list[dict] = eval_meta.get("filtered_chunks", [])
        prompt: str = eval_meta.get("prompt", "")
        answer: str = result_dict.get("answer", "")
        status: str = result_dict.get("status", "error")

        # Step 2 — Compute local metrics (no LLM)
        recall = compute_recall_at_expected(raw_chunks, gold.expected_note_ids)
        ctx_util = estimate_context_utilisation(answer, filtered_chunks)

        retrieved_note_ids = list(dict.fromkeys(c["note_id"] for c in raw_chunks))
        chunk_artifacts = [
            ChunkArtifact(
                note_id=c.get("note_id", 0),
                note_title=c.get("note_title", ""),
                chunk_text=c.get("chunk_text", ""),
                chunk_index=c.get("chunk_index", 0),
                score=round(c.get("score", 0.0), 4),
                semantic_score=round(c.get("semantic_score", 0.0), 4),
                intent_score=round(c.get("intent_score", 0.0), 4),
                intent_category=c.get("intent_category"),
            )
            for c in raw_chunks
        ]

        # Step 3 — Build context string for judge (same format as prompt)
        context_for_judge = self._extract_context_from_prompt(prompt)

        # Step 4 — Run judge (only if pipeline produced an answer)
        if not judge_error and answer:
            try:
                scores = self.judge.evaluate(
                    question=gold.question,
                    context=context_for_judge,
                    answer=answer,
                    reference_answer=gold.reference_answer,
                )
            except JudgeError as exc:
                logger.warning("Judge failed for query %s: %s", gold.id, exc)
                judge_error = str(exc)
        elif not judge_error and not answer:
            judge_error = "Pipeline returned empty answer"

        # Step 5 — Cost estimation
        prompt_tokens = estimate_tokens(prompt)
        completion_tokens = estimate_tokens(answer)
        cost_usd = estimate_cost_usd(prompt_tokens, completion_tokens)

        # Step 6 — Root cause classification
        eval_result = AskEvalResult(
            query_id=gold.id,
            question=gold.question,
            category=gold.category,
            difficulty=gold.difficulty,
            answer=answer,
            reference_answer=gold.reference_answer,
            status=status,
            retrieval_only=result_dict.get("retrieval_only", False),
            retrieved_note_ids=retrieved_note_ids,
            expected_note_ids=gold.expected_note_ids,
            retrieved_chunks=chunk_artifacts,
            filtered_chunk_count=len(filtered_chunks),
            prompt=prompt,
            scores=scores,
            root_cause=None,
            recall_at_expected=recall,
            context_utilisation=ctx_util,
            retrieval_ms=eval_meta.get("retrieval_ms", 0.0),
            llm_ms=eval_meta.get("llm_ms", 0.0),
            total_ms=eval_meta.get("total_ms", 0.0),
            estimated_prompt_tokens=prompt_tokens,
            estimated_completion_tokens=completion_tokens,
            estimated_cost_usd=cost_usd,
            error=judge_error,
        )

        weighted = scores.weighted_overall if scores else 0.0
        if weighted < _FAILURE_THRESHOLD or judge_error:
            root_cause = classify_root_cause(eval_result, judge_error)
            eval_result = eval_result.model_copy(update={"root_cause": root_cause})

        # Step 7 — Persist debug artifact
        if artifact_dir:
            save_debug_artifact(
                artifact_dir=artifact_dir,
                query_id=gold.id,
                gold=gold,
                result_dict=result_dict,
                scores=scores,
                root_cause=root_cause,
                judge_error=judge_error,
            )

        return eval_result

    # ------------------------------------------------------------------
    # Aggregation
    # ------------------------------------------------------------------

    def _aggregate(
        self,
        run_id: str,
        created_at: str,
        results: list[AskEvalResult],
    ) -> AskEvalReport:
        """Build the aggregate report from per-query results."""

        def _safe_mean(vals: list[float]) -> float:
            return statistics.mean(vals) if vals else 0.0

        scored = [r for r in results if r.scores is not None]

        avg_correctness    = _safe_mean([r.scores.correctness    for r in scored])
        avg_groundedness   = _safe_mean([r.scores.groundedness   for r in scored])
        avg_faithfulness   = _safe_mean([r.scores.faithfulness   for r in scored])
        avg_hallucination  = _safe_mean([r.scores.hallucination  for r in scored])
        avg_completeness   = _safe_mean([r.scores.completeness   for r in scored])
        avg_overall        = _safe_mean([r.scores.weighted_overall for r in scored])

        avg_retrieval_ms   = _safe_mean([r.retrieval_ms for r in results])
        avg_llm_ms         = _safe_mean([r.llm_ms       for r in results])
        avg_total_ms       = _safe_mean([r.total_ms     for r in results])
        total_cost         = sum(r.estimated_cost_usd for r in results)

        # Per-category breakdown
        categories: dict[str, list[AskEvalResult]] = {}
        for r in scored:
            categories.setdefault(r.category, []).append(r)

        category_summaries = []
        for cat, cat_results in sorted(categories.items()):
            category_summaries.append(CategorySummary(
                category=cat,
                query_count=len(cat_results),
                avg_correctness=_safe_mean([r.scores.correctness   for r in cat_results]),
                avg_groundedness=_safe_mean([r.scores.groundedness  for r in cat_results]),
                avg_faithfulness=_safe_mean([r.scores.faithfulness  for r in cat_results]),
                avg_hallucination=_safe_mean([r.scores.hallucination for r in cat_results]),
                avg_completeness=_safe_mean([r.scores.completeness  for r in cat_results]),
                avg_overall=_safe_mean([r.scores.weighted_overall for r in cat_results]),
                avg_total_ms=_safe_mean([r.total_ms for r in cat_results]),
            ))

        # Rank by weighted overall
        sorted_scored = sorted(scored, key=lambda r: r.scores.weighted_overall)
        hardest = [r.query_id for r in sorted_scored[:5]]
        easiest = [r.query_id for r in sorted_scored[-5:]]

        # Root cause distribution
        root_cause_counts: dict[str, int] = {}
        for r in results:
            if r.root_cause:
                key = r.root_cause.value
                root_cause_counts[key] = root_cause_counts.get(key, 0) + 1

        return AskEvalReport(
            run_id=run_id,
            created_at=created_at,
            total_queries=len(results),
            avg_correctness=avg_correctness,
            avg_groundedness=avg_groundedness,
            avg_faithfulness=avg_faithfulness,
            avg_hallucination=avg_hallucination,
            avg_completeness=avg_completeness,
            avg_overall=avg_overall,
            avg_retrieval_ms=avg_retrieval_ms,
            avg_llm_ms=avg_llm_ms,
            avg_total_ms=avg_total_ms,
            total_estimated_cost_usd=total_cost,
            category_summaries=category_summaries,
            hardest_queries=hardest,
            easiest_queries=easiest,
            root_cause_counts=root_cause_counts,
            results=results,
        )

    @staticmethod
    def _extract_context_from_prompt(prompt: str) -> str:
        """Extract the <context>...</context> section from the built prompt."""
        start = prompt.find("<context>")
        end = prompt.find("</context>")
        if start != -1 and end != -1:
            return prompt[start + len("<context>"):end].strip()
        return prompt  # fallback: pass whole prompt
