"""
Unit tests for app.evaluation.ask.models.

Tests:
- GoldAskQuery schema validation
- JudgeScores boundary conditions
- AskEvalResult construction
- ChunkArtifact construction
- FailureRootCause enum values
- CategorySummary aggregation
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.evaluation.ask.models import (
    AskEvalResult,
    CategorySummary,
    ChunkArtifact,
    FailureRootCause,
    GoldAskQuery,
    JudgeScores,
)


# ---------------------------------------------------------------------------
# GoldAskQuery
# ---------------------------------------------------------------------------

class TestGoldAskQuery:
    def test_valid_query_parses_correctly(self):
        q = GoldAskQuery(
            id="fq_01",
            question="What is Redis?",
            expected_note_ids=[73],
            reference_answer="Redis is an in-memory data store.",
            category="factual_lookup",
            difficulty="easy",
        )
        assert q.id == "fq_01"
        assert q.expected_note_ids == [73]
        assert q.eval_notes == ""

    def test_missing_required_field_raises(self):
        with pytest.raises(ValidationError):
            GoldAskQuery(
                id="test",
                # question missing
                expected_note_ids=[1],
                reference_answer="ref",
                category="factual_lookup",
            )

    def test_empty_note_ids_is_valid(self):
        q = GoldAskQuery(
            id="q1",
            question="test?",
            expected_note_ids=[],
            reference_answer="ref",
            category="factual_lookup",
        )
        assert q.expected_note_ids == []

    def test_default_difficulty_is_medium(self):
        q = GoldAskQuery(
            id="q1",
            question="test?",
            reference_answer="ref",
            category="factual_lookup",
        )
        assert q.difficulty == "medium"

    def test_default_eval_notes_is_empty_string(self):
        q = GoldAskQuery(
            id="q1",
            question="test?",
            reference_answer="ref",
            category="factual_lookup",
        )
        assert q.eval_notes == ""


# ---------------------------------------------------------------------------
# ChunkArtifact
# ---------------------------------------------------------------------------

class TestChunkArtifact:
    def test_valid_chunk_artifact(self):
        c = ChunkArtifact(
            note_id=73,
            note_title="Redis Notes",
            chunk_text="Redis is fast.",
            chunk_index=0,
            score=0.85,
            semantic_score=0.82,
            intent_score=0.03,
            intent_category="Study - Redis",
        )
        assert c.note_id == 73
        assert c.intent_category == "Study - Redis"

    def test_none_intent_category_is_valid(self):
        c = ChunkArtifact(
            note_id=73,
            note_title="Redis Notes",
            chunk_text="Redis is fast.",
            chunk_index=0,
            score=0.85,
            semantic_score=0.82,
            intent_score=0.0,
            intent_category=None,
        )
        assert c.intent_category is None


# ---------------------------------------------------------------------------
# FailureRootCause
# ---------------------------------------------------------------------------

class TestFailureRootCause:
    def test_all_values_are_strings(self):
        for cause in FailureRootCause:
            assert isinstance(cause.value, str)

    def test_expected_causes_exist(self):
        values = {c.value for c in FailureRootCause}
        assert "retrieval_failure" in values
        assert "hallucination" in values
        assert "insufficient_context" in values
        assert "prompt_construction" in values
        assert "evaluator_failure" in values
        assert "unknown" in values


# ---------------------------------------------------------------------------
# AskEvalResult
# ---------------------------------------------------------------------------

def _make_eval_result(**overrides) -> AskEvalResult:
    base = dict(
        query_id="fq_01",
        question="What is Redis?",
        category="factual_lookup",
        difficulty="easy",
        answer="Redis is an in-memory data store.",
        reference_answer="Redis is an in-memory data store.",
        status="ok",
        retrieval_only=False,
        retrieved_note_ids=[73, 74],
        expected_note_ids=[73],
        retrieved_chunks=[],
        filtered_chunk_count=2,
        prompt="...",
        scores=None,
        root_cause=None,
        recall_at_expected=1.0,
        context_utilisation=0.5,
        retrieval_ms=120.0,
        llm_ms=800.0,
        total_ms=940.0,
        estimated_prompt_tokens=250,
        estimated_completion_tokens=80,
        estimated_cost_usd=0.0000425,
        error=None,
    )
    base.update(overrides)
    return AskEvalResult(**base)


class TestAskEvalResult:
    def test_basic_construction(self):
        r = _make_eval_result()
        assert r.query_id == "fq_01"
        assert r.status == "ok"
        assert r.retrieval_only is False
        assert r.scores is None
        assert r.root_cause is None

    def test_with_judge_scores(self):
        scores = JudgeScores(
            correctness=0.9,
            groundedness=0.85,
            faithfulness=1.0,
            hallucination=0.95,
            completeness=0.8,
            overall=0.88,
            justification="Good answer.",
        )
        r = _make_eval_result(scores=scores)
        assert r.scores is not None
        assert r.scores.correctness == 0.9
        assert r.scores.weighted_overall > 0.0

    def test_with_root_cause(self):
        r = _make_eval_result(root_cause=FailureRootCause.RETRIEVAL_FAILURE)
        assert r.root_cause == FailureRootCause.RETRIEVAL_FAILURE

    def test_error_field_accepts_string(self):
        r = _make_eval_result(error="Judge timed out")
        assert r.error == "Judge timed out"

    def test_estimated_cost_is_non_negative(self):
        r = _make_eval_result()
        assert r.estimated_cost_usd >= 0.0

    def test_recall_at_expected_range(self):
        r = _make_eval_result(recall_at_expected=0.5)
        assert 0.0 <= r.recall_at_expected <= 1.0

    def test_model_copy_update_works(self):
        r = _make_eval_result()
        r2 = r.model_copy(update={"root_cause": FailureRootCause.HALLUCINATION})
        assert r2.root_cause == FailureRootCause.HALLUCINATION
        assert r.root_cause is None  # original unchanged


# ---------------------------------------------------------------------------
# CategorySummary
# ---------------------------------------------------------------------------

class TestCategorySummary:
    def test_valid_category_summary(self):
        cs = CategorySummary(
            category="factual_lookup",
            query_count=8,
            avg_correctness=0.85,
            avg_groundedness=0.90,
            avg_faithfulness=0.95,
            avg_hallucination=0.92,
            avg_completeness=0.80,
            avg_overall=0.87,
            avg_total_ms=1200.5,
        )
        assert cs.category == "factual_lookup"
        assert cs.query_count == 8
        assert cs.avg_overall == 0.87
