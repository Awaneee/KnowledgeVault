"""
Hybrid retrieval adapter.

Wraps:
    ChunkService.retrieve_hybrid()

Production contract
-------------------
ChunkService.retrieve_hybrid() returns

[
    {
        "note_id": int,
        "note_title": str,
        "chunk_text": str,
        "chunk_index": int,
        "source": "intent" | "semantic",
        "intent_category": str | None
    }
]

The adapter deduplicates note_ids while preserving ranking.

Required production changes
---------------------------
ChunkService.retrieve_hybrid() must include "note_id".
"""

from __future__ import annotations

from app.evaluation.adapters.base import BaseRetrievalAdapter
from app.evaluation.constants import DEFAULT_HYBRID_LIMIT
from app.evaluation.models import (
    BenchmarkQuery,
    RetrievalResult,
    RetrievalStrategy,
)

from app.services.chunk_service import ChunkService
from app.services.intent_category_service import IntentCategoryService


class HybridAdapter(BaseRetrievalAdapter):

    strategy = RetrievalStrategy.HYBRID

    def __init__(
        self,
        db,
        user_id: int,
        limit: int = DEFAULT_HYBRID_LIMIT,
    ) -> None:

        super().__init__(db)

        self._chunk_service = ChunkService(db)
        self._intent_service = IntentCategoryService(db)

        self._user_id = user_id
        self._limit = limit

    def _retrieve(
        self,
        benchmark_query: BenchmarkQuery,
    ) -> RetrievalResult:

        chunks = self._chunk_service.retrieve_hybrid(
            query=benchmark_query.query,
            user_id=self._user_id,
            limit=self._limit,
        )

        note_ids = []
        seen = set()

        for chunk in chunks:

            note_id = chunk["note_id"]

            if note_id in seen:
                continue

            seen.add(note_id)
            note_ids.append(note_id)

        categories = self._intent_service.find_categories_for_query(
            query=benchmark_query.query,
            user_id=self._user_id,
            limit=1,
        )

        predicted_category = (
            categories[0].name
            if categories
            else None
        )

        return RetrievalResult(
            strategy=self.strategy,
            query=benchmark_query.query,
            retrieved_note_ids=note_ids,
            predicted_category=predicted_category,
        )