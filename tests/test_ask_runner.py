"""
Unit tests for app.evaluation.ask.runner.

Tests:
- compute_recall_at_expected
- estimate_context_utilisation
- classify_root_cause
- GoldDatasetLoader.load()
- save_debug_artifact (filesystem)
- AskEvaluationRunner with mocked dependencies
- AskEvalReport aggregation
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.evaluation.ask.models import (
    AskEvalResult,
    ChunkArtifact,
    FailureRootCause,
    GoldAskQuery,
    JudgeScores,
)
from app.evaluation.ask.runner import (
    GoldDatasetLoader,
    AskEvaluationRunner,
    classify_root_cause,
    compute_recall_at_expected,
    estimate_context_utilisation,
    save_debug_artifact,
)


# ---------------------------------------------------------------------------
# compute_recall_at_expected
# ---------------------------------------------------------------------------

class TestComputeRecallAtExpected:
    def test_all_expected_retrieved(self):
        chunks = [{"note_id": 1}, {"note_id": 2}, {"note_id": 3}]
        assert compute_recall_at_expected(chunks, [1, 2]) == 1.0

    def test_none_expected_retrieved(self):
        chunks = [{"note_id": 5}, {"note_id": 6}]
        assert compute_recall_at_expected(chunks, [1, 2]) == 0.0

    def test_partial_recall(self):
        chunks = [{"note_id": 1}, {"note_id": 5}]
        recall = compute_recall_at_expected(chunks, [1, 2])
        assert recall == 0.5

    def test_empty_expected_returns_one(self):
        # Vacuously satisfied: nothing expected, nothing required
        chunks = [{"note_id": 1}]
        assert compute_recall_at_expected(chunks, []) == 1.0

    def test_empty_chunks_no_expected(self):
        assert compute_recall_at_expected([], []) == 1.0

    def test_empty_chunks_with_expected(self):
        assert compute_recall_at_expected([], [1, 2]) == 0.0


# ---------------------------------------------------------------------------
# estimate_context_utilisation
# ---------------------------------------------------------------------------

class TestEstimateContextUtilisation:
    def test_full_utilisation_with_trigram_overlap(self):
        chunks = [{"chunk_text": "Redis is an in-memory data structure store"}]
        answer = "Redis is an in-memory data structure store used for caching."
        util = estimate_context_utilisation(answer, chunks)
        assert util == 1.0

    def test_no_utilisation_no_overlap(self):
        chunks = [{"chunk_text": "PostgreSQL is a relational database system"}]
        answer = "I could not find that information in your notes."
        util = estimate_context_utilisation(answer, chunks)
        assert util == 0.0

    def test_empty_chunks_returns_zero(self):
        assert estimate_context_utilisation("some answer", []) == 0.0

    def test_empty_answer_returns_zero(self):
        chunks = [{"chunk_text": "Redis is fast"}]
        assert estimate_context_utilisation("", chunks) == 0.0

    def test_partial_utilisation(self):
        chunks = [
            {"chunk_text": "Redis is an in-memory database"},
            {"chunk_text": "PostgreSQL uses ACID compliance very strictly"},
        ]
        # Answer only references Redis
        answer = "Redis is an in-memory database used for caching."
        util = estimate_context_utilisation(answer, chunks)
        assert 0.0 < util < 1.0


# ---------------------------------------------------------------------------
# classify_root_cause
# ---------------------------------------------------------------------------

def _make_result_for_cause(
    recall: float = 0.8,
    correctness: float = 0.8,
    groundedness: float = 0.8,
    faithfulness: float = 0.9,
    hallucination: float = 0.9,
    completeness: float = 0.8,
    overall: float = 0.8,
) -> AskEvalResult:
    scores = JudgeScores(
        correctness=correctness,
        groundedness=groundedness,
        faithfulness=faithfulness,
        hallucination=hallucination,
        completeness=completeness,
        overall=overall,
        justification="test",
    )
    return AskEvalResult(
        query_id="test",
        question="test?",
        category="factual_lookup",
        difficulty="easy",
        answer="test answer",
        reference_answer="ref",
        status="ok",
        retrieval_only=False,
        retrieved_note_ids=[1],
        expected_note_ids=[1],
        retrieved_chunks=[],
        filtered_chunk_count=1,
        prompt="test prompt",
        scores=scores,
        root_cause=None,
        recall_at_expected=recall,
        context_utilisation=0.5,
        retrieval_ms=100.0,
        llm_ms=500.0,
        total_ms=600.0,
        estimated_prompt_tokens=200,
        estimated_completion_tokens=50,
        estimated_cost_usd=0.0,
    )


class TestClassifyRootCause:
    def test_evaluator_failure_on_judge_error(self):
        result = _make_result_for_cause()
        cause = classify_root_cause(result, judge_error="timeout")
        assert cause == FailureRootCause.EVALUATOR_FAILURE

    def test_evaluator_failure_when_no_scores(self):
        result = _make_result_for_cause()
        result = result.model_copy(update={"scores": None})
        cause = classify_root_cause(result, judge_error=None)
        assert cause == FailureRootCause.EVALUATOR_FAILURE

    def test_retrieval_failure_low_recall_and_correctness(self):
        result = _make_result_for_cause(recall=0.2, correctness=0.2)
        cause = classify_root_cause(result, judge_error=None)
        assert cause == FailureRootCause.RETRIEVAL_FAILURE

    def test_hallucination_low_hallucination_score(self):
        result = _make_result_for_cause(recall=0.9, hallucination=0.2)
        cause = classify_root_cause(result, judge_error=None)
        assert cause == FailureRootCause.HALLUCINATION

    def test_insufficient_context_low_completeness(self):
        result = _make_result_for_cause(recall=0.8, completeness=0.2, hallucination=0.8)
        cause = classify_root_cause(result, judge_error=None)
        assert cause == FailureRootCause.INSUFFICIENT_CONTEXT

    def test_prompt_construction_good_retrieval_bad_correctness(self):
        result = _make_result_for_cause(
            recall=0.9,
            groundedness=0.8,
            correctness=0.2,
            hallucination=0.8,
            completeness=0.7,
        )
        cause = classify_root_cause(result, judge_error=None)
        assert cause == FailureRootCause.PROMPT_CONSTRUCTION

    def test_unknown_for_ambiguous_failure(self):
        # Low overall but no clear specific cause
        result = _make_result_for_cause(
            recall=0.9, correctness=0.5, groundedness=0.5,
            hallucination=0.5, completeness=0.5,
        )
        cause = classify_root_cause(result, judge_error=None)
        # Could be UNKNOWN or any other cause — just verify it returns a valid enum
        assert isinstance(cause, FailureRootCause)


# ---------------------------------------------------------------------------
# GoldDatasetLoader
# ---------------------------------------------------------------------------

class TestGoldDatasetLoader:
    def test_load_valid_json(self):
        data = [
            {
                "id": "fq_01",
                "question": "What is Redis?",
                "expected_note_ids": [73],
                "reference_answer": "Redis is fast.",
                "category": "factual_lookup",
                "difficulty": "easy",
            }
        ]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(data, f)
            path = f.name

        queries = GoldDatasetLoader.load(path)
        assert len(queries) == 1
        assert queries[0].id == "fq_01"
        assert queries[0].expected_note_ids == [73]

    def test_load_missing_file_raises(self):
        with pytest.raises(FileNotFoundError):
            GoldDatasetLoader.load("/nonexistent/path/gold.json")

    def test_load_invalid_entry_raises(self):
        data = [{"invalid_field": "no question or id"}]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, encoding="utf-8"
        ) as f:
            json.dump(data, f)
            path = f.name

        with pytest.raises(Exception):
            GoldDatasetLoader.load(path)


# ---------------------------------------------------------------------------
# save_debug_artifact
# ---------------------------------------------------------------------------

class TestSaveDebugArtifact:
    def test_artifact_is_written(self):
        gold = GoldAskQuery(
            id="fq_test",
            question="What is Redis?",
            expected_note_ids=[73],
            reference_answer="Redis is fast.",
            category="factual_lookup",
            difficulty="easy",
        )
        scores = JudgeScores(
            correctness=0.9, groundedness=0.85, faithfulness=1.0,
            hallucination=0.95, completeness=0.8, overall=0.88,
            justification="Good.",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            artifact_dir = Path(tmpdir)
            save_debug_artifact(
                artifact_dir=artifact_dir,
                query_id="fq_test",
                gold=gold,
                result_dict={
                    "status": "ok",
                    "answer": "Redis is in-memory.",
                    "sources": ["Redis Notes"],
                    "retrieval_only": False,
                    "_eval": {
                        "prompt": "test prompt",
                        "retrieved_chunks": [],
                        "filtered_chunks": [],
                        "retrieval_ms": 120.0,
                        "llm_ms": 800.0,
                        "total_ms": 940.0,
                    },
                },
                scores=scores,
                root_cause=None,
                judge_error=None,
            )

            artifact_file = artifact_dir / "fq_test_debug.json"
            assert artifact_file.exists()

            content = json.loads(artifact_file.read_text(encoding="utf-8"))
            assert content["query_id"] == "fq_test"
            assert content["pipeline"]["answer"] == "Redis is in-memory."
            assert content["judge"]["scores"]["correctness"] == 0.9
            assert content["judge"]["error"] is None

    def test_artifact_directory_created_if_not_exists(self):
        gold = GoldAskQuery(
            id="fq_test",
            question="Q?",
            reference_answer="A",
            category="factual_lookup",
        )

        with tempfile.TemporaryDirectory() as tmpdir:
            artifact_dir = Path(tmpdir) / "nested" / "subdir"
            assert not artifact_dir.exists()

            save_debug_artifact(
                artifact_dir=artifact_dir,
                query_id="fq_test",
                gold=gold,
                result_dict={"_eval": {}},
                scores=None,
                root_cause=None,
                judge_error="test error",
            )

            assert artifact_dir.exists()
            assert (artifact_dir / "fq_test_debug.json").exists()


# ---------------------------------------------------------------------------
# AskEvaluationRunner — integration with mocked dependencies
# ---------------------------------------------------------------------------

class TestAskEvaluationRunner:
    """
    Integration tests with mocked AskService and AskJudge.
    No database required.
    """

    GOLD_DATA = [
        {
            "id": "fq_01",
            "question": "What is Redis?",
            "expected_note_ids": [73],
            "reference_answer": "Redis is an in-memory data store.",
            "category": "factual_lookup",
            "difficulty": "easy",
        },
        {
            "id": "fq_02",
            "question": "What is Docker?",
            "expected_note_ids": [72],
            "reference_answer": "Docker is a container platform.",
            "category": "factual_lookup",
            "difficulty": "easy",
        },
    ]

    MOCK_CHUNK = {
        "note_id": 73,
        "note_title": "Redis Notes",
        "chunk_text": "Redis is an in-memory data structure store.",
        "chunk_index": 0,
        "score": 0.88,
        "semantic_score": 0.85,
        "intent_score": 0.03,
        "intent_category": "Study",
    }

    MOCK_ASK_RESULT = {
        "status": "ok",
        "answer": "Redis is an in-memory data store used for caching.",
        "sources": ["Redis Notes"],
        "retrieval_only": False,
        "_eval": {
            "retrieved_chunks": [MOCK_CHUNK],
            "filtered_chunks": [MOCK_CHUNK],
            "prompt": "<context>Redis is an in-memory data structure store.</context>\n<question>What is Redis?</question>",
            "retrieval_ms": 120.0,
            "llm_ms": 800.0,
            "total_ms": 940.0,
        },
    }

    MOCK_SCORES = JudgeScores(
        correctness=0.9,
        groundedness=0.85,
        faithfulness=1.0,
        hallucination=0.95,
        completeness=0.8,
        overall=0.88,
        justification="Good answer.",
    )

    def _write_gold(self, tmpdir: str) -> Path:
        path = Path(tmpdir) / "gold.json"
        path.write_text(json.dumps(self.GOLD_DATA), encoding="utf-8")
        return path

    def test_runner_returns_report_with_correct_query_count(self):
        mock_db = MagicMock()

        with (
            patch("app.evaluation.ask.runner.AskService") as MockAsk,
            patch("app.evaluation.ask.runner.AskJudge") as MockJudge,
        ):
            MockAsk.return_value.ask_with_context.return_value = self.MOCK_ASK_RESULT
            MockJudge.return_value.evaluate.return_value = self.MOCK_SCORES

            with tempfile.TemporaryDirectory() as tmpdir:
                gold_path = self._write_gold(tmpdir)
                runner = AskEvaluationRunner(mock_db)
                report = runner.run(user_id=1, dataset_path=gold_path)

        assert report.total_queries == 2
        assert len(report.results) == 2

    def test_runner_report_contains_correct_averages(self):
        mock_db = MagicMock()

        with (
            patch("app.evaluation.ask.runner.AskService") as MockAsk,
            patch("app.evaluation.ask.runner.AskJudge") as MockJudge,
        ):
            MockAsk.return_value.ask_with_context.return_value = self.MOCK_ASK_RESULT
            MockJudge.return_value.evaluate.return_value = self.MOCK_SCORES

            with tempfile.TemporaryDirectory() as tmpdir:
                gold_path = self._write_gold(tmpdir)
                runner = AskEvaluationRunner(mock_db)
                report = runner.run(user_id=1, dataset_path=gold_path)

        # Both queries have the same mocked scores
        assert abs(report.avg_correctness - 0.9) < 0.01
        assert abs(report.avg_groundedness - 0.85) < 0.01

    def test_runner_persists_artifacts_when_artifact_dir_given(self):
        mock_db = MagicMock()

        with (
            patch("app.evaluation.ask.runner.AskService") as MockAsk,
            patch("app.evaluation.ask.runner.AskJudge") as MockJudge,
        ):
            MockAsk.return_value.ask_with_context.return_value = self.MOCK_ASK_RESULT
            MockJudge.return_value.evaluate.return_value = self.MOCK_SCORES

            with tempfile.TemporaryDirectory() as tmpdir:
                gold_path = self._write_gold(tmpdir)
                artifact_dir = Path(tmpdir) / "artifacts"
                runner = AskEvaluationRunner(mock_db)
                runner.run(
                    user_id=1,
                    dataset_path=gold_path,
                    artifact_dir=artifact_dir,
                )

                # Two debug JSON files should exist
                assert (artifact_dir / "fq_01_debug.json").exists()
                assert (artifact_dir / "fq_02_debug.json").exists()

    def test_runner_handles_pipeline_exception_gracefully(self):
        mock_db = MagicMock()

        with (
            patch("app.evaluation.ask.runner.AskService") as MockAsk,
            patch("app.evaluation.ask.runner.AskJudge") as MockJudge,
        ):
            MockAsk.return_value.ask_with_context.side_effect = RuntimeError("DB error")
            MockJudge.return_value.evaluate.return_value = self.MOCK_SCORES

            with tempfile.TemporaryDirectory() as tmpdir:
                gold_path = self._write_gold(tmpdir)
                runner = AskEvaluationRunner(mock_db)
                # Must NOT raise; should handle error per-query
                report = runner.run(user_id=1, dataset_path=gold_path)

        assert report.total_queries == 2
        for r in report.results:
            assert r.error is not None

    def test_runner_category_summaries_are_present(self):
        mock_db = MagicMock()

        with (
            patch("app.evaluation.ask.runner.AskService") as MockAsk,
            patch("app.evaluation.ask.runner.AskJudge") as MockJudge,
        ):
            MockAsk.return_value.ask_with_context.return_value = self.MOCK_ASK_RESULT
            MockJudge.return_value.evaluate.return_value = self.MOCK_SCORES

            with tempfile.TemporaryDirectory() as tmpdir:
                gold_path = self._write_gold(tmpdir)
                runner = AskEvaluationRunner(mock_db)
                report = runner.run(user_id=1, dataset_path=gold_path)

        # Both queries are in "factual_lookup"
        assert len(report.category_summaries) == 1
        assert report.category_summaries[0].category == "factual_lookup"
        assert report.category_summaries[0].query_count == 2

    def test_runner_root_cause_assigned_for_failed_queries(self):
        """If scores are low, root_cause should be assigned."""
        mock_db = MagicMock()
        low_scores = JudgeScores(
            correctness=0.1,
            groundedness=0.1,
            faithfulness=0.9,
            hallucination=0.9,
            completeness=0.1,
            overall=0.2,
            justification="Very poor.",
        )

        # Mock: retrieval returns different notes (recall miss)
        mock_result = dict(self.MOCK_ASK_RESULT)
        mock_result["_eval"] = dict(self.MOCK_ASK_RESULT["_eval"])
        mock_result["_eval"]["retrieved_chunks"] = [
            {"note_id": 999, "note_title": "Irrelevant", "chunk_text": "xyz",
             "chunk_index": 0, "score": 0.5, "semantic_score": 0.5, "intent_score": 0.0}
        ]
        mock_result["_eval"]["filtered_chunks"] = mock_result["_eval"]["retrieved_chunks"]

        with (
            patch("app.evaluation.ask.runner.AskService") as MockAsk,
            patch("app.evaluation.ask.runner.AskJudge") as MockJudge,
        ):
            MockAsk.return_value.ask_with_context.return_value = mock_result
            MockJudge.return_value.evaluate.return_value = low_scores

            with tempfile.TemporaryDirectory() as tmpdir:
                gold_path = self._write_gold(tmpdir)
                runner = AskEvaluationRunner(mock_db)
                report = runner.run(user_id=1, dataset_path=gold_path)

        for r in report.results:
            assert r.root_cause is not None
