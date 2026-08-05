"""
Chunk-level semantic retrieval adapter.

Wraps: ChunkService.retrieve(query, user_id, limit)

Why this adapter exists
-----------------------
The existing SemanticAdapter calls EmbeddingService.search_notes(), which
searches the *note-level* embedding table (one vector per note).

ChunkService.retrieve() searches the *chunk-level* embedding table
(one vector per chunk, typically 3-6 per note).  These are different ANN
corpora with different granularity:

  SemanticAdapter       → note_embeddings   (note-level ANN)
  HybridAdapter         → note_embeddings   (note-level ANN) + intent arm
  ChunkSemanticAdapter  → chunk_embeddings  (chunk-level ANN)

ChunkSemanticAdapter is also the only evaluation coverage for the live
production endpoint POST /retrieve, which calls ChunkService.retrieve()
directly and was previously unrepresented in the benchmark.

Output contract
---------------
retrieve() returns list[dict] with keys including "note_id".  Multiple
chunks from the same note may appear in the ranked list.  The adapter
deduplicates by note_id while preserving chunk-rank order — the first
(highest-similarity) chunk seen for each note determines that note's rank.

Limit
-----
Uses DEFAULT_HYBRID_LIMIT (20) to match the retrieval budget of HybridAdapter,
making per-query metric comparisons directly interpretable.  At chunk level
this still evaluates @K=5.
"""

from __future__ import annotations

from app.evaluation.adapters.base import BaseRetrievalAdapter
from app.evaluation.constants import DEFAULT_HYBRID_LIMIT
from app.evaluation.models import BenchmarkQuery, RetrievalResult, RetrievalStrategy
from app.services.chunk_service import ChunkService


class ChunkSemanticAdapter(BaseRetrievalAdapter):
    """Chunk-level semantic ANN with no intent arm — wraps ChunkService.retrieve()."""

    strategy = RetrievalStrategy.CHUNK_SEMANTIC

    def __init__(self, db, user_id: int, limit: int = DEFAULT_HYBRID_LIMIT) -> None:
        super().__init__(db)
        self._chunk_service = ChunkService(db)
        self._user_id = user_id
        self._limit = limit

    def _retrieve(self, benchmark_query: BenchmarkQuery) -> RetrievalResult:
        chunks = self._chunk_service.retrieve(
            query=benchmark_query.query,
            user_id=self._user_id,
            limit=self._limit,
        )

        # Deduplicate to note-level, preserving chunk-rank order.
        # The first occurrence of each note_id has the highest chunk similarity.
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
