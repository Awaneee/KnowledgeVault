"""
Unit tests for RerankingService.

All tests are pure Python: no database, no network, no real cross-encoder.
The rerank model and CacheService are fully mocked.
"""
from __future__ import annotations

import hashlib
from unittest.mock import MagicMock, patch

import pytest

from app.services.reranking_service import RerankingService, RerankResult


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _candidates(n: int = 4, base_note_id: int = 1) -> list[dict]:
    """Return n minimal candidate dicts as produce by retrieve_hybrid()."""
    return [
        {
            "note_id": base_note_id + i,
            "note_title": f"Note {base_note_id + i}",
            "chunk_id": (base_note_id + i) * 10,
            "chunk_text": f"Content of note {base_note_id + i}. " * 5,
            "chunk_index": 0,
            "score": 0.9 - i * 0.1,
            "semantic_score": 0.9 - i * 0.1,
            "intent_score": 0.0,
            "source": "semantic",
            "intent_category": None,
        }
        for i in range(n)
    ]


# ---------------------------------------------------------------------------
# RERANKING_ENABLED=False branch
# ---------------------------------------------------------------------------

class TestRerankingDisabled:
    """When the feature flag is off the service must be a transparent pass-through."""

    @patch("app.services.reranking_service.settings")
    def test_disabled_returns_original_order(self, mock_settings):
        mock_settings.RERANKING_ENABLED = False
        mock_settings.RERANK_TOP_K = 8
        candidates = _candidates(4)

        result = RerankingService.rerank(
            query="test query",
            candidates=candidates,
            top_k=8,
            user_id=1,
        )

        assert result.reranked is False
        assert result.candidates == candidates  # identical objects, same order

    @patch("app.services.reranking_service.settings")
    def test_disabled_truncates_to_top_k(self, mock_settings):
        mock_settings.RERANKING_ENABLED = False
        candidates = _candidates(10)

        result = RerankingService.rerank(
            query="q",
            candidates=candidates,
            top_k=5,
            user_id=1,
        )

        assert result.reranked is False
        assert len(result.candidates) == 5
        # First 5 of original order retained
        assert result.candidates == candidates[:5]

    @patch("app.services.reranking_service.rerank_model", None)
    @patch("app.services.reranking_service.settings")
    def test_model_none_returns_original_order(self, mock_settings):
        mock_settings.RERANKING_ENABLED = True
        candidates = _candidates(3)

        result = RerankingService.rerank(
            query="q",
            candidates=candidates,
            top_k=8,
            user_id=1,
        )

        assert result.reranked is False
        assert result.candidates == candidates[:8]


# ---------------------------------------------------------------------------
# Empty candidates
# ---------------------------------------------------------------------------

class TestEmptyCandidates:
    @patch("app.services.reranking_service.settings")
    def test_empty_candidates_returns_empty(self, mock_settings):
        mock_settings.RERANKING_ENABLED = True

        # Even with a non-None model, empty candidates short-circuit before inference.
        with patch("app.services.reranking_service.rerank_model", MagicMock()):
            result = RerankingService.rerank(
                query="q",
                candidates=[],
                top_k=5,
                user_id=1,
            )

        assert result.candidates == []
        assert result.reranked is False


# ---------------------------------------------------------------------------
# Cache miss → inference path
# ---------------------------------------------------------------------------

class TestInferencePath:

    @patch("app.services.reranking_service.CacheService")
    @patch("app.services.reranking_service.rerank_model")
    @patch("app.services.reranking_service.settings")
    def test_inference_reorders_by_score(self, mock_settings, mock_model, mock_cache):
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CACHE_TTL_SECONDS = 900
        mock_cache.get.return_value = None  # cache miss

        candidates = _candidates(3)
        # Reranker assigns high score to the last candidate (note_id 3)
        mock_model.predict.return_value = [0.1, 0.5, 0.9]

        result = RerankingService.rerank(
            query="what is note 3?",
            candidates=candidates,
            top_k=3,
            user_id=42,
        )

        assert result.reranked is True
        assert result.candidates[0]["note_id"] == 3  # highest score wins
        assert result.candidates[1]["note_id"] == 2
        assert result.candidates[2]["note_id"] == 1

    @patch("app.services.reranking_service.CacheService")
    @patch("app.services.reranking_service.rerank_model")
    @patch("app.services.reranking_service.settings")
    def test_inference_truncates_to_top_k(self, mock_settings, mock_model, mock_cache):
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CACHE_TTL_SECONDS = 900
        mock_cache.get.return_value = None
        candidates = _candidates(6)
        mock_model.predict.return_value = [0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

        result = RerankingService.rerank(
            query="q",
            candidates=candidates,
            top_k=3,
            user_id=1,
        )

        assert result.reranked is True
        assert len(result.candidates) == 3

    @patch("app.services.reranking_service.CacheService")
    @patch("app.services.reranking_service.rerank_model")
    @patch("app.services.reranking_service.settings")
    def test_inference_writes_score_map_to_cache(
        self, mock_settings, mock_model, mock_cache
    ):
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CACHE_TTL_SECONDS = 900
        mock_cache.get.return_value = None
        candidates = _candidates(2)
        mock_model.predict.return_value = [0.7, 0.3]

        RerankingService.rerank(
            query="q",
            candidates=candidates,
            top_k=2,
            user_id=7,
        )

        mock_cache.set.assert_called_once()
        call_args = mock_cache.set.call_args
        score_map = call_args[0][1]  # positional arg 1 is value
        assert len(score_map) == 2
        assert all("note_id" in entry and "score" in entry for entry in score_map)

    @patch("app.services.reranking_service.CacheService")
    @patch("app.services.reranking_service.rerank_model")
    @patch("app.services.reranking_service.settings")
    def test_inference_pairs_contain_query_and_chunk_text(
        self, mock_settings, mock_model, mock_cache
    ):
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CACHE_TTL_SECONDS = 900
        mock_cache.get.return_value = None
        candidates = _candidates(2)
        mock_model.predict.return_value = [0.8, 0.2]

        RerankingService.rerank(
            query="my query",
            candidates=candidates,
            top_k=2,
            user_id=1,
        )

        call_pairs = mock_model.predict.call_args[0][0]
        assert len(call_pairs) == 2
        for query_text, chunk_text in call_pairs:
            assert query_text == "my query"
            assert "Content of note" in chunk_text


# ---------------------------------------------------------------------------
# Cache hit path
# ---------------------------------------------------------------------------

class TestCacheHitPath:

    @patch("app.services.reranking_service.CacheService")
    @patch("app.services.reranking_service.rerank_model")
    @patch("app.services.reranking_service.settings")
    def test_cache_hit_skips_inference(self, mock_settings, mock_model, mock_cache):
        mock_settings.RERANKING_ENABLED = True
        # Return a cached score map: note 3 ranks highest
        mock_cache.get.return_value = [
            {"note_id": 1, "score": 0.1},
            {"note_id": 2, "score": 0.5},
            {"note_id": 3, "score": 0.9},
        ]
        candidates = _candidates(3)

        result = RerankingService.rerank(
            query="q",
            candidates=candidates,
            top_k=3,
            user_id=1,
        )

        mock_model.predict.assert_not_called()
        assert result.reranked is True
        assert result.candidates[0]["note_id"] == 3

    @patch("app.services.reranking_service.CacheService")
    @patch("app.services.reranking_service.rerank_model")
    @patch("app.services.reranking_service.settings")
    def test_cache_hit_truncates_to_top_k(self, mock_settings, mock_model, mock_cache):
        mock_settings.RERANKING_ENABLED = True
        mock_cache.get.return_value = [
            {"note_id": i + 1, "score": float(i)} for i in range(5)
        ]
        candidates = _candidates(5)

        result = RerankingService.rerank(
            query="q",
            candidates=candidates,
            top_k=3,
            user_id=1,
        )

        assert len(result.candidates) == 3

    @patch("app.services.reranking_service.CacheService")
    @patch("app.services.reranking_service.rerank_model")
    @patch("app.services.reranking_service.settings")
    def test_cache_hit_does_not_write_cache(self, mock_settings, mock_model, mock_cache):
        mock_settings.RERANKING_ENABLED = True
        mock_cache.get.return_value = [{"note_id": 1, "score": 0.9}]
        candidates = _candidates(1)

        RerankingService.rerank(
            query="q",
            candidates=candidates,
            top_k=1,
            user_id=1,
        )

        mock_cache.set.assert_not_called()


# ---------------------------------------------------------------------------
# Graceful fallback on inference failure
# ---------------------------------------------------------------------------

class TestInferenceFailureFallback:

    @patch("app.services.reranking_service.CacheService")
    @patch("app.services.reranking_service.rerank_model")
    @patch("app.services.reranking_service.settings")
    def test_predict_exception_returns_original_order(
        self, mock_settings, mock_model, mock_cache
    ):
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CACHE_TTL_SECONDS = 900
        mock_cache.get.return_value = None
        mock_model.predict.side_effect = RuntimeError("CUDA OOM")
        candidates = _candidates(3)

        result = RerankingService.rerank(
            query="q",
            candidates=candidates,
            top_k=3,
            user_id=1,
        )

        assert result.reranked is False
        assert result.candidates == candidates  # original order preserved

    @patch("app.services.reranking_service.CacheService")
    @patch("app.services.reranking_service.rerank_model")
    @patch("app.services.reranking_service.settings")
    def test_predict_exception_does_not_write_cache(
        self, mock_settings, mock_model, mock_cache
    ):
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CACHE_TTL_SECONDS = 900
        mock_cache.get.return_value = None
        mock_model.predict.side_effect = ValueError("bad input")

        RerankingService.rerank(
            query="q",
            candidates=_candidates(2),
            top_k=2,
            user_id=1,
        )

        mock_cache.set.assert_not_called()


# ---------------------------------------------------------------------------
# Cache key stability
# ---------------------------------------------------------------------------

class TestCacheKey:

    def test_key_is_stable_regardless_of_candidate_insertion_order(self):
        candidates_a = _candidates(3, base_note_id=10)
        candidates_b = list(reversed(candidates_a))

        key_a = RerankingService._cache_key(1, "query", candidates_a)
        key_b = RerankingService._cache_key(1, "query", candidates_b)

        assert key_a == key_b, "Cache key must be independent of candidate order"

    def test_different_note_sets_produce_different_keys(self):
        candidates_a = _candidates(3, base_note_id=1)
        candidates_b = _candidates(3, base_note_id=100)

        key_a = RerankingService._cache_key(1, "query", candidates_a)
        key_b = RerankingService._cache_key(1, "query", candidates_b)

        assert key_a != key_b

    def test_different_queries_produce_different_keys(self):
        candidates = _candidates(2)
        key_a = RerankingService._cache_key(1, "query alpha", candidates)
        key_b = RerankingService._cache_key(1, "query beta", candidates)

        assert key_a != key_b

    def test_different_user_ids_produce_different_keys(self):
        candidates = _candidates(2)
        key_a = RerankingService._cache_key(1, "q", candidates)
        key_b = RerankingService._cache_key(2, "q", candidates)

        assert key_a != key_b

    def test_key_has_expected_prefix(self):
        candidates = _candidates(1)
        key = RerankingService._cache_key(5, "q", candidates)
        assert key.startswith("rerank:5:")

    def test_query_normalised_before_hashing(self):
        """Leading/trailing whitespace and case should not affect the key."""
        candidates = _candidates(2)
        key_a = RerankingService._cache_key(1, "  My Query  ", candidates)
        key_b = RerankingService._cache_key(1, "my query", candidates)

        assert key_a == key_b


# ---------------------------------------------------------------------------
# _apply_cached_scores
# ---------------------------------------------------------------------------

class TestApplyCachedScores:

    def test_reorders_by_cached_score(self):
        candidates = _candidates(3)
        score_map = [
            {"note_id": 1, "score": 0.1},
            {"note_id": 2, "score": 0.9},
            {"note_id": 3, "score": 0.5},
        ]
        result = RerankingService._apply_cached_scores(score_map, candidates, top_k=3)
        assert result[0]["note_id"] == 2
        assert result[1]["note_id"] == 3
        assert result[2]["note_id"] == 1

    def test_truncates_to_top_k(self):
        candidates = _candidates(4)
        score_map = [{"note_id": i + 1, "score": float(i)} for i in range(4)]
        result = RerankingService._apply_cached_scores(score_map, candidates, top_k=2)
        assert len(result) == 2

    def test_missing_score_treated_as_zero(self):
        candidates = _candidates(2)
        # Only note_id=1 has a cached score; note_id=2 is missing → score 0.0
        score_map = [{"note_id": 1, "score": 0.8}]
        result = RerankingService._apply_cached_scores(score_map, candidates, top_k=2)
        assert result[0]["note_id"] == 1  # 0.8 > 0.0
