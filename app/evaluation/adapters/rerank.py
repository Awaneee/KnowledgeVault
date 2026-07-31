"""
Rerank retrieval adapter.

Wraps ChunkService.retrieve_hybrid() followed by RerankingService.rerank().
This adapter measures the full retrieve-then-rerank latency so that the
benchmark can compare HYBRID vs RERANK on both quality and speed.

The adapter respects RERANKING_ENABLED: if the feature flag is off or the
model failed to load, RerankingService.rerank() returns the hybrid ordering
unchanged, so RERANK results degrade gracefully to HYBRID results.
"""

from __future__ import annotations

from app.core.config import settings
from app.evaluation.adapters.base import BaseRetrievalAdapter
from app.evaluation.models import BenchmarkQuery, RetrievalResult, RetrievalStrategy
from app.services.chunk_service import ChunkService
from app.services.intent_category_service import IntentCategoryService
from app.services.reranking_service import RerankingService


class RerankAdapter(BaseRetrievalAdapter):

    strategy = RetrievalStrategy.RERANK

    def __init__(
        self,
        db,
        user_id: int,
        pool: int | None = None,
        top_k: int | None = None,
    ) -> None:
        super().__init__(db)
        self._chunk_service = ChunkService(db)
        self._intent_service = IntentCategoryService(db)
        self._user_id = user_id
        self._pool = pool or settings.RERANK_CANDIDATE_POOL
        self._top_k = top_k or settings.RERANK_TOP_K

    def _retrieve(self, benchmark_query: BenchmarkQuery) -> RetrievalResult:
        # Stage 1 — hybrid retrieval with expanded candidate pool
        chunks = self._chunk_service.retrieve_hybrid(
            query=benchmark_query.query,
            user_id=self._user_id,
            limit=self._pool,
        )

        # Stage 2 — cross-encoder reranking
        rerank_result = RerankingService.rerank(
            query=benchmark_query.query,
            candidates=chunks,
            top_k=self._top_k,
            user_id=self._user_id,
        )

        # Deduplicate note IDs while preserving reranked order.
        note_ids: list[int] = []
        seen: set[int] = set()
        for chunk in rerank_result.candidates:
            note_id = chunk["note_id"]
            if note_id not in seen:
                seen.add(note_id)
                note_ids.append(note_id)

        predicted_intent = self._intent_service.extractor.extract_query_intent_fast(
            benchmark_query.query
        )["intent_type"]

        categories = self._intent_service.find_categories_for_query(
            query=benchmark_query.query,
            user_id=self._user_id,
            limit=1,
        )
        predicted_category = categories[0].name if categories else None

        return RetrievalResult(
            strategy=self.strategy,
            query=benchmark_query.query,
            retrieved_note_ids=note_ids,
            predicted_intent=predicted_intent,
            predicted_category=predicted_category,
        )
