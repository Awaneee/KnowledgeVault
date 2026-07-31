"""
Tests for AskService with cross-encoder reranking integrated.

All tests are pure Python: no database, no network, no LLM call.
ChunkService, LLMService, RerankingService, and CacheService are mocked.

Covers:
  - reranked=False when RERANKING_ENABLED=False
  - reranked=True when reranker succeeds
  - reranked=False when reranker fails (graceful fallback)
  - pool_limit is RERANK_CANDIDATE_POOL when RERANKING_ENABLED=True
  - pool_limit is 8 when RERANKING_ENABLED=False
  - reranked flag is present in cached response
  - AskResponse schema accepts reranked field
  - stream_ask applies reranking
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch, call

import pytest

from app.schemas.ask import AskResponse
from app.services.ask_service import AskService
from app.services.reranking_service import RerankResult


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _chunk(note_id: int = 1, score: float = 0.8) -> dict:
    return {
        "note_id": note_id,
        "note_title": f"Note {note_id}",
        "chunk_id": note_id * 10,
        "chunk_text": f"Content of note {note_id}. " * 6,
        "chunk_index": 0,
        "score": score,
        "semantic_score": score,
        "intent_score": 0.0,
        "source": "semantic",
        "intent_category": None,
    }


def _make_service() -> AskService:
    """Create AskService with a mocked ChunkService (no DB needed)."""
    svc = AskService.__new__(AskService)
    svc.chunk_service = MagicMock()
    svc.chunk_service.retrieve_hybrid.return_value = [_chunk(1), _chunk(2)]
    return svc


# ---------------------------------------------------------------------------
# AskResponse schema — reranked field
# ---------------------------------------------------------------------------

class TestAskResponseRerankField:
    def test_defaults_to_false(self):
        r = AskResponse(question="q", answer="a", sources=[])
        assert r.reranked is False

    def test_can_be_set_true(self):
        r = AskResponse(question="q", answer="a", sources=[], reranked=True)
        assert r.reranked is True

    def test_backward_compat_without_field(self):
        """Existing response dicts without 'reranked' still deserialise."""
        data = {"question": "q", "answer": "a", "sources": [], "status": "ok"}
        r = AskResponse(**data)
        assert r.reranked is False


# ---------------------------------------------------------------------------
# ask() — reranked flag in response
# ---------------------------------------------------------------------------

class TestAskRerankedFlag:

    @patch("app.services.ask_service.CacheService")
    @patch("app.services.ask_service.LLMService")
    @patch("app.services.ask_service.RerankingService")
    @patch("app.services.ask_service.settings")
    def test_reranked_false_when_disabled(
        self, mock_settings, mock_reranker, mock_llm, mock_cache
    ):
        mock_settings.RERANKING_ENABLED = False
        mock_settings.RERANK_CANDIDATE_POOL = 20
        mock_settings.RERANK_TOP_K = 8
        mock_settings.RETRIEVAL_MIN_SCORE = 0.0
        mock_settings.ASK_CACHE_TTL_SECONDS = 0
        mock_settings.LLM_PROVIDER_PRIORITY = "gemini"
        mock_settings.LLM_PROVIDER = "gemini"
        mock_cache.get.return_value = None
        mock_reranker.rerank.return_value = RerankResult(
            candidates=[_chunk(1), _chunk(2)], reranked=False
        )
        mock_llm.generate.return_value = "The answer is here and quite detailed."

        svc = _make_service()
        result = svc.ask("what is note 1?", user_id=1)

        assert result["reranked"] is False

    @patch("app.services.ask_service.CacheService")
    @patch("app.services.ask_service.LLMService")
    @patch("app.services.ask_service.RerankingService")
    @patch("app.services.ask_service.settings")
    def test_reranked_true_when_enabled_and_succeeds(
        self, mock_settings, mock_reranker, mock_llm, mock_cache
    ):
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CANDIDATE_POOL = 20
        mock_settings.RERANK_TOP_K = 8
        mock_settings.RETRIEVAL_MIN_SCORE = 0.0
        mock_settings.ASK_CACHE_TTL_SECONDS = 0
        mock_settings.LLM_PROVIDER_PRIORITY = "gemini"
        mock_settings.LLM_PROVIDER = "gemini"
        mock_cache.get.return_value = None
        mock_reranker.rerank.return_value = RerankResult(
            candidates=[_chunk(2), _chunk(1)],  # reranker flipped the order
            reranked=True,
        )
        mock_llm.generate.return_value = "Reranked answer with full details."

        svc = _make_service()
        result = svc.ask("what is note 2?", user_id=1)

        assert result["reranked"] is True

    @patch("app.services.ask_service.CacheService")
    @patch("app.services.ask_service.LLMService")
    @patch("app.services.ask_service.RerankingService")
    @patch("app.services.ask_service.settings")
    def test_reranked_false_on_reranker_fallback(
        self, mock_settings, mock_reranker, mock_llm, mock_cache
    ):
        """When the reranker returns reranked=False (fallback), the response carries False."""
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CANDIDATE_POOL = 20
        mock_settings.RERANK_TOP_K = 8
        mock_settings.RETRIEVAL_MIN_SCORE = 0.0
        mock_settings.ASK_CACHE_TTL_SECONDS = 0
        mock_settings.LLM_PROVIDER_PRIORITY = "gemini"
        mock_settings.LLM_PROVIDER = "gemini"
        mock_cache.get.return_value = None
        # Reranker gracefully fell back (inference failed internally)
        mock_reranker.rerank.return_value = RerankResult(
            candidates=[_chunk(1), _chunk(2)],
            reranked=False,
        )
        mock_llm.generate.return_value = "Fallback answer with enough detail here."

        svc = _make_service()
        result = svc.ask("q", user_id=1)

        assert result["reranked"] is False


# ---------------------------------------------------------------------------
# ask() — pool_limit wiring
# ---------------------------------------------------------------------------

class TestAskPoolLimit:

    @patch("app.services.ask_service.CacheService")
    @patch("app.services.ask_service.LLMService")
    @patch("app.services.ask_service.RerankingService")
    @patch("app.services.ask_service.settings")
    def test_pool_limit_is_candidate_pool_when_enabled(
        self, mock_settings, mock_reranker, mock_llm, mock_cache
    ):
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CANDIDATE_POOL = 20
        mock_settings.RERANK_TOP_K = 8
        mock_settings.RETRIEVAL_MIN_SCORE = 0.0
        mock_settings.ASK_CACHE_TTL_SECONDS = 0
        mock_settings.LLM_PROVIDER_PRIORITY = "gemini"
        mock_settings.LLM_PROVIDER = "gemini"
        mock_cache.get.return_value = None
        mock_reranker.rerank.return_value = RerankResult(
            candidates=[_chunk(1)], reranked=True
        )
        mock_llm.generate.return_value = "Answer with sufficient detail present."

        svc = _make_service()
        svc.ask("q", user_id=1)

        svc.chunk_service.retrieve_hybrid.assert_called_once()
        _, kwargs = svc.chunk_service.retrieve_hybrid.call_args
        assert kwargs["limit"] == 20

    @patch("app.services.ask_service.CacheService")
    @patch("app.services.ask_service.LLMService")
    @patch("app.services.ask_service.RerankingService")
    @patch("app.services.ask_service.settings")
    def test_pool_limit_is_8_when_disabled(
        self, mock_settings, mock_reranker, mock_llm, mock_cache
    ):
        mock_settings.RERANKING_ENABLED = False
        mock_settings.RERANK_CANDIDATE_POOL = 20
        mock_settings.RERANK_TOP_K = 8
        mock_settings.RETRIEVAL_MIN_SCORE = 0.0
        mock_settings.ASK_CACHE_TTL_SECONDS = 0
        mock_settings.LLM_PROVIDER_PRIORITY = "gemini"
        mock_settings.LLM_PROVIDER = "gemini"
        mock_cache.get.return_value = None
        mock_reranker.rerank.return_value = RerankResult(
            candidates=[_chunk(1)], reranked=False
        )
        mock_llm.generate.return_value = "Answer with sufficient detail present."

        svc = _make_service()
        svc.ask("q", user_id=1)

        _, kwargs = svc.chunk_service.retrieve_hybrid.call_args
        assert kwargs["limit"] == 8


# ---------------------------------------------------------------------------
# ask() — reranker receives the raw pool, not the filtered set
# ---------------------------------------------------------------------------

class TestRerankCalledBeforeFilter:

    @patch("app.services.ask_service.CacheService")
    @patch("app.services.ask_service.LLMService")
    @patch("app.services.ask_service.RerankingService")
    @patch("app.services.ask_service.settings")
    def test_reranker_receives_unfiltered_pool(
        self, mock_settings, mock_reranker, mock_llm, mock_cache
    ):
        """RerankingService.rerank must be called with the raw retrieve output."""
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CANDIDATE_POOL = 20
        mock_settings.RERANK_TOP_K = 8
        mock_settings.RETRIEVAL_MIN_SCORE = 0.5  # high threshold so some chunks get filtered
        mock_settings.ASK_CACHE_TTL_SECONDS = 0
        mock_settings.LLM_PROVIDER_PRIORITY = "gemini"
        mock_settings.LLM_PROVIDER = "gemini"
        mock_cache.get.return_value = None

        raw_pool = [_chunk(1, score=0.9), _chunk(2, score=0.1)]  # chunk 2 below threshold
        mock_reranker.rerank.return_value = RerankResult(
            candidates=raw_pool[:], reranked=True
        )
        mock_llm.generate.return_value = "Detailed answer with full content here."

        svc = _make_service()
        svc.chunk_service.retrieve_hybrid.return_value = raw_pool
        svc.ask("q", user_id=1)

        # The full pool (both chunks) must reach the reranker
        call_kwargs = mock_reranker.rerank.call_args[1]
        assert len(call_kwargs["candidates"]) == 2


# ---------------------------------------------------------------------------
# ask() — cache stores reranked flag
# ---------------------------------------------------------------------------

class TestCacheWithRerankFlag:

    @patch("app.services.ask_service.CacheService")
    @patch("app.services.ask_service.LLMService")
    @patch("app.services.ask_service.RerankingService")
    @patch("app.services.ask_service.settings")
    def test_cache_set_includes_reranked_true(
        self, mock_settings, mock_reranker, mock_llm, mock_cache
    ):
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CANDIDATE_POOL = 20
        mock_settings.RERANK_TOP_K = 8
        mock_settings.RETRIEVAL_MIN_SCORE = 0.0
        mock_settings.ASK_CACHE_TTL_SECONDS = 3600
        mock_settings.LLM_PROVIDER_PRIORITY = "gemini"
        mock_settings.LLM_PROVIDER = "gemini"
        mock_cache.get.return_value = None
        mock_reranker.rerank.return_value = RerankResult(
            candidates=[_chunk(1)], reranked=True
        )
        mock_llm.generate.return_value = "Synthesised answer with complete details."

        svc = _make_service()
        svc.ask("q", user_id=1)

        mock_cache.set.assert_called_once()
        cached_value = mock_cache.set.call_args[0][1]
        assert cached_value["reranked"] is True


# ---------------------------------------------------------------------------
# stream_ask() — reranking is applied
# ---------------------------------------------------------------------------

class TestStreamAskReranking:

    @patch("app.services.ask_service.LLMService")
    @patch("app.services.ask_service.RerankingService")
    @patch("app.services.ask_service.settings")
    def test_stream_applies_reranking(
        self, mock_settings, mock_reranker, mock_llm
    ):
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CANDIDATE_POOL = 20
        mock_settings.RERANK_TOP_K = 8
        mock_settings.RETRIEVAL_MIN_SCORE = 0.0
        mock_reranker.rerank.return_value = RerankResult(
            candidates=[_chunk(2), _chunk(1)], reranked=True
        )
        mock_llm.generate_stream.return_value = iter(["token"])

        svc = _make_service()
        tokens = list(svc.stream_ask("q", user_id=1))

        mock_reranker.rerank.assert_called_once()
        assert tokens == ["token"]

    @patch("app.services.ask_service.LLMService")
    @patch("app.services.ask_service.RerankingService")
    @patch("app.services.ask_service.settings")
    def test_stream_pool_limit_is_20_when_enabled(
        self, mock_settings, mock_reranker, mock_llm
    ):
        mock_settings.RERANKING_ENABLED = True
        mock_settings.RERANK_CANDIDATE_POOL = 20
        mock_settings.RERANK_TOP_K = 8
        mock_settings.RETRIEVAL_MIN_SCORE = 0.0
        mock_reranker.rerank.return_value = RerankResult(
            candidates=[_chunk(1)], reranked=True
        )
        mock_llm.generate_stream.return_value = iter([])

        svc = _make_service()
        list(svc.stream_ask("q", user_id=1))

        _, kwargs = svc.chunk_service.retrieve_hybrid.call_args
        assert kwargs["limit"] == 20
