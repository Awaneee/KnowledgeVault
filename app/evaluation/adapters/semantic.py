"""
Semantic retrieval adapter.

Wraps: EmbeddingService.search_notes(query, user_id, limit)

Production contract
-------------------
EmbeddingService.search_notes() returns a list of dicts:
    [{"id": int, "title": str, "content": str | None}, ...]
ranked by pgvector cosine similarity.

The adapter extracts the "id" field from each dict and preserves rank order.

Required production changes
---------------------------
None.  EmbeddingService.search_notes() already returns note IDs.
"""

from __future__ import annotations

from app.evaluation.adapters.base import BaseRetrievalAdapter
from app.evaluation.constants import DEFAULT_SEMANTIC_LIMIT
from app.evaluation.models import BenchmarkQuery, RetrievalResult, RetrievalStrategy

# Production import — never duplicated here.
from app.services.embedding_service import EmbeddingService


class SemanticAdapter(BaseRetrievalAdapter):
    strategy = RetrievalStrategy.SEMANTIC

    def __init__(self, db, user_id: int, limit: int = DEFAULT_SEMANTIC_LIMIT) -> None:
        super().__init__(db)
        self._service = EmbeddingService(db)
        self._user_id = user_id
        self._limit = limit

    def _retrieve(self, benchmark_query: BenchmarkQuery) -> RetrievalResult:
        raw = self._service.search_notes(
            query=benchmark_query.query,
            user_id=self._user_id,
            limit=self._limit,
        )

        # raw is list[dict] with key "id" — see EmbeddingService.search_notes()
        note_ids = [item["id"] for item in raw]

        return RetrievalResult(
            strategy=self.strategy,
            query=benchmark_query.query,
            retrieved_note_ids=note_ids,
            # Semantic path has no intent or category prediction.
            predicted_intent=None,
            predicted_category=None,
        )
