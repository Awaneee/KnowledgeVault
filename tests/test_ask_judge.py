"""
Unit tests for app.evaluation.ask.judge.

Tests:
- JudgeScores model validation (field ranges, required fields)
- JSON repair path (_try_repair)
- Score clamping (_coerce_scores)
- Cost estimation
- Token estimation
- AskJudge.evaluate() with mocked Gemini responses

All tests are pure unit tests — no database, no network, no LLM calls.
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from app.evaluation.ask.judge import (
    AskJudge,
    JudgeError,
    _try_repair,
    estimate_cost_usd,
    estimate_tokens,
)
from app.evaluation.ask.models import JudgeScores


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

VALID_SCORES = {
    "correctness": 0.9,
    "groundedness": 0.85,
    "faithfulness": 1.0,
    "hallucination": 0.95,
    "completeness": 0.8,
    "overall": 0.88,
    "justification": "The answer is accurate and well-grounded in the retrieved context.",
    "hallucinated_claims": [],
    "ungrounded_claims": [],
}


# ---------------------------------------------------------------------------
# JudgeScores model
# ---------------------------------------------------------------------------

class TestJudgeScoresModel:
    def test_valid_scores_parse_correctly(self):
        scores = JudgeScores(**VALID_SCORES)
        assert scores.correctness == 0.9
        assert scores.groundedness == 0.85
        assert scores.faithfulness == 1.0
        assert scores.hallucination == 0.95
        assert scores.completeness == 0.8
        assert scores.overall == 0.88
        assert scores.justification != ""
        assert isinstance(scores.hallucinated_claims, list)
        assert isinstance(scores.ungrounded_claims, list)

    def test_minimum_boundary_values(self):
        data = {k: 0.0 for k in ["correctness", "groundedness", "faithfulness",
                                   "hallucination", "completeness", "overall"]}
        data["justification"] = "Low quality answer."
        scores = JudgeScores(**data)
        assert scores.correctness == 0.0

    def test_maximum_boundary_values(self):
        data = {k: 1.0 for k in ["correctness", "groundedness", "faithfulness",
                                   "hallucination", "completeness", "overall"]}
        data["justification"] = "Perfect answer."
        scores = JudgeScores(**data)
        assert scores.correctness == 1.0

    def test_score_below_range_fails_validation(self):
        data = dict(VALID_SCORES)
        data["correctness"] = -0.1
        with pytest.raises(Exception):
            JudgeScores(**data)

    def test_score_above_range_fails_validation(self):
        data = dict(VALID_SCORES)
        data["groundedness"] = 1.1
        with pytest.raises(Exception):
            JudgeScores(**data)

    def test_missing_required_field_fails(self):
        data = dict(VALID_SCORES)
        del data["correctness"]
        with pytest.raises(Exception):
            JudgeScores(**data)

    def test_weighted_overall_formula(self):
        """weighted_overall = 0.30*c + 0.25*g + 0.20*f + 0.15*comp + 0.10*h"""
        scores = JudgeScores(**VALID_SCORES)
        expected = (
            0.9 * 0.30
            + 0.85 * 0.25
            + 1.0 * 0.20
            + 0.8 * 0.15
            + 0.95 * 0.10
        )
        assert abs(scores.weighted_overall - expected) < 1e-9

    def test_default_empty_claims_lists(self):
        data = dict(VALID_SCORES)
        del data["hallucinated_claims"]
        del data["ungrounded_claims"]
        scores = JudgeScores(**data)
        assert scores.hallucinated_claims == []
        assert scores.ungrounded_claims == []


# ---------------------------------------------------------------------------
# JSON repair
# ---------------------------------------------------------------------------

class TestTryRepair:
    def test_valid_json_passes_through(self):
        raw = json.dumps(VALID_SCORES)
        result = _try_repair(raw)
        assert result is not None
        assert result["correctness"] == 0.9

    def test_json_in_markdown_fence_is_repaired(self):
        raw = f"```json\n{json.dumps(VALID_SCORES)}\n```"
        result = _try_repair(raw)
        assert result is not None
        assert result["overall"] == 0.88

    def test_json_with_preamble_is_repaired(self):
        raw = f"Here is the evaluation:\n{json.dumps(VALID_SCORES)}"
        result = _try_repair(raw)
        assert result is not None

    def test_garbage_returns_none(self):
        result = _try_repair("This is not JSON at all!!!")
        assert result is None

    def test_empty_string_returns_none(self):
        result = _try_repair("")
        assert result is None


# ---------------------------------------------------------------------------
# Score clamping
# ---------------------------------------------------------------------------

class TestCoerceScores:
    def test_out_of_range_high_is_clamped(self):
        data = dict(VALID_SCORES)
        data["correctness"] = 1.5
        coerced = AskJudge._coerce_scores(data)
        assert coerced["correctness"] == 1.0

    def test_out_of_range_low_is_clamped(self):
        data = dict(VALID_SCORES)
        data["groundedness"] = -0.2
        coerced = AskJudge._coerce_scores(data)
        assert coerced["groundedness"] == 0.0

    def test_missing_field_defaults_to_zero(self):
        data = {"justification": "ok"}
        coerced = AskJudge._coerce_scores(data)
        assert coerced["correctness"] == 0.0
        assert coerced["faithfulness"] == 0.0

    def test_non_numeric_field_defaults_to_zero(self):
        data = dict(VALID_SCORES)
        data["completeness"] = "high"
        coerced = AskJudge._coerce_scores(data)
        assert coerced["completeness"] == 0.0

    def test_default_lists_are_added(self):
        data = {"justification": "ok"}
        coerced = AskJudge._coerce_scores(data)
        assert coerced["hallucinated_claims"] == []
        assert coerced["ungrounded_claims"] == []


# ---------------------------------------------------------------------------
# Token and cost estimation
# ---------------------------------------------------------------------------

class TestCostEstimation:
    def test_token_estimate_is_positive(self):
        assert estimate_tokens("hello world") > 0

    def test_empty_string_returns_minimum(self):
        assert estimate_tokens("") == 1  # max(1, 0//4)

    def test_long_text_returns_proportional_estimate(self):
        text = "a" * 4000
        assert estimate_tokens(text) == 1000

    def test_zero_tokens_yields_zero_cost(self):
        cost = estimate_cost_usd(0, 0)
        assert cost == 0.0

    def test_cost_is_non_negative(self):
        cost = estimate_cost_usd(1000, 200)
        assert cost >= 0.0

    def test_cost_scales_with_tokens(self):
        cost_small = estimate_cost_usd(100, 50)
        cost_large = estimate_cost_usd(10000, 5000)
        assert cost_large > cost_small


# ---------------------------------------------------------------------------
# AskJudge.evaluate() — mocked Gemini
# ---------------------------------------------------------------------------

class TestAskJudgeEvaluate:
    """Tests that mock the Gemini HTTP call."""

    @staticmethod
    def _make_judge() -> AskJudge:
        """Build a judge, bypassing GEMINI_API_KEY check."""
        with patch("app.evaluation.ask.judge.settings") as mock_settings:
            mock_settings.GEMINI_API_KEY = "test-key"
            mock_settings.GEMINI_API_BASE = "https://example.com"
            mock_settings.GEMINI_ANSWER_MODEL = "gemini-2.0-flash"
            mock_settings.LLM_TIMEOUT_SECONDS = 30
            return AskJudge()

    def test_evaluate_returns_judge_scores_on_valid_response(self):
        judge = self._make_judge()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": json.dumps(VALID_SCORES)}]}}]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_response):
            scores = judge.evaluate(
                question="What is Redis?",
                context="Redis is an in-memory data structure store.",
                answer="Redis is an in-memory database.",
                reference_answer="Redis is an in-memory data structure store.",
            )

        assert isinstance(scores, JudgeScores)
        assert scores.correctness == 0.9
        assert scores.groundedness == 0.85

    def test_evaluate_raises_on_malformed_json_after_repair(self):
        judge = self._make_judge()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "not json at all!!!"}]}}]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_response):
            with pytest.raises(JudgeError):
                judge.evaluate(
                    question="Q",
                    context="C",
                    answer="A",
                )

    def test_evaluate_raises_on_timeout(self):
        import requests as req_lib

        judge = self._make_judge()

        with patch("requests.post", side_effect=req_lib.exceptions.Timeout):
            with pytest.raises(JudgeError, match="timed out"):
                judge.evaluate(question="Q", context="C", answer="A")

    def test_evaluate_clamps_out_of_range_scores(self):
        judge = self._make_judge()

        bad_scores = dict(VALID_SCORES)
        bad_scores["correctness"] = 2.0   # above range
        bad_scores["hallucination"] = -1.0  # below range

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": json.dumps(bad_scores)}]}}]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_response):
            scores = judge.evaluate(question="Q", context="C", answer="A")

        assert scores.correctness <= 1.0
        assert scores.hallucination >= 0.0

    def test_evaluate_missing_api_key_raises(self):
        with patch("app.evaluation.ask.judge.settings") as mock_settings:
            mock_settings.GEMINI_API_KEY = None
            with pytest.raises(JudgeError, match="GEMINI_API_KEY"):
                AskJudge()
