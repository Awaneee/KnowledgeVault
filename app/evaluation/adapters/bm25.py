"""
BM25 evaluation adapters.

BM25Adapter       — pure sparse retrieval via PostgreSQL FTS (BM25Repository).
HybridBM25Adapter — dense semantic + sparse BM25 fused via RRF
                    (ChunkService._retrieve_rrf_hybrid).

Both adapters bypass BM25_ENABLED because evaluation is always deliberate:
the point of these adapters is to measure the BM25 arm regardless of the
production feature flag.  The flag exists to protect production; it should
not prevent the benchmark from testing the strategy.

Both adapters set predicted_intent / predicted_category to None: BM25 has no
intent extraction path.  The evaluation runner handles None gracefully.
"""

from __future__ import annotations

from app.core.config import settings
from app.evaluation.adapters.base import BaseRetrievalAdapter
from app.evaluation.constants import DEFAULT_HYBRID_LIMIT
from app.evaluation.models import (
    BenchmarkQuery,
    RetrievalResult,
    RetrievalStrategy,
)
from app.repositories.bm25_repository import BM25Repository
from app.services.chunk_service import ChunkService


class BM25Adapter(BaseRetrievalAdapter):
    """Pure sparse BM25 retrieval — no semantic embedding, no intent lookup."""

    strategy = RetrievalStrategy.BM25

    def __init__(self, db, user_id: int, limit: int = DEFAULT_HYBRID_LIMIT) -> None:
        super().__init__(db)
        self._bm25_repo = BM25Repository(db)
        self._user_id = user_id
        self._limit = limit

    def _retrieve(self, benchmark_query: BenchmarkQuery) -> RetrievalResult:
        rows = self._bm25_repo.search(
            query=benchmark_query.query,
            user_id=self._user_id,
            limit=self._limit,
        )

        # Deduplicate by note_id, preserving BM25 rank order.
        note_ids: list[int] = []
        seen: set[int] = set()
        for row in rows:
            nid = row["note_id"]
            if nid not in seen:
                seen.add(nid)
                note_ids.append(nid)

        return RetrievalResult(
            strategy=self.strategy,
            query=benchmark_query.query,
            retrieved_note_ids=note_ids,
            predicted_intent=None,
            predicted_category=None,
        )


class HybridBM25Adapter(BaseRetrievalAdapter):
    """
    Dense semantic + sparse BM25 retrieval fused via Reciprocal Rank Fusion.

    Calls ChunkService._retrieve_rrf_hybrid() directly so the BM25 arm is
    always exercised, independent of the BM25_ENABLED production flag.
    """

    strategy = RetrievalStrategy.HYBRID_BM25

    def __init__(self, db, user_id: int, limit: int = DEFAULT_HYBRID_LIMIT) -> None:
        super().__init__(db)
        self._chunk_service = ChunkService(db)
        self._user_id = user_id
        self._limit = limit

    def _retrieve(self, benchmark_query: BenchmarkQuery) -> RetrievalResult:
        # Bypass the BM25_ENABLED flag — the adapter exists to evaluate the
        # RRF strategy; the flag is a production gate, not an eval gate.
        chunks = self._chunk_service._retrieve_rrf_hybrid(
            query=benchmark_query.query,
            user_id=self._user_id,
            limit=self._limit,
            k=settings.BM25_RRF_K,
            pool=settings.BM25_CANDIDATE_POOL,
        )

        note_ids: list[int] = []
        seen: set[int] = set()
        for chunk in chunks:
            nid = chunk["note_id"]
            if nid not in seen:
                seen.add(nid)
                note_ids.append(nid)

        return RetrievalResult(
            strategy=self.strategy,
            query=benchmark_query.query,
            retrieved_note_ids=note_ids,
            predicted_intent=None,
            predicted_category=None,
        )
