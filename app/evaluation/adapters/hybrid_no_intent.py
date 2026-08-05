"""
Hybrid retrieval adapter with intent boost disabled.

Wraps: ChunkService.retrieve_hybrid(max_intent_boost=0.0)

Why this adapter exists
-----------------------
The standard HybridAdapter calls retrieve_hybrid() with the default
max_intent_boost (0.12).  This adapter passes 0.0 instead, which has
the following effect inside retrieve_hybrid():

  - The intent arm STILL RUNS:
      • find_category_matches_for_query() executes.
      • Intent-only candidates (notes not in the semantic ANN pool but
        matched by category) are still added to the fusion dict via
        _text_overlap_score() as their semantic score.
  - The additive score boost is suppressed:
      • boost = (effective_boost_cap * intent_score) if is_boosted else 0.0
        becomes boost = 0.0 for every candidate.
  - Final ranking is therefore pure semantic_score for every note.

This isolates the intent boost contribution: the difference between
HYBRID_NO_INTENT and HYBRID is exactly the effect of the 0–0.12 additive
boost on final ranking, with no other variable changed.

The difference between CHUNK_SEMANTIC and HYBRID_NO_INTENT isolates the
retrieval-granularity effect (chunk-level ANN vs. note-level ANN).
"""

from __future__ import annotations

from app.evaluation.adapters.base import BaseRetrievalAdapter
from app.evaluation.constants import DEFAULT_HYBRID_LIMIT
from app.evaluation.models import BenchmarkQuery, RetrievalResult, RetrievalStrategy
from app.services.chunk_service import ChunkService
from app.services.intent_category_service import IntentCategoryService


class HybridNoIntentAdapter(BaseRetrievalAdapter):
    """
    Hybrid pipeline with intent boost = 0.0.

    Identical call stack to HybridAdapter except max_intent_boost=0.0 is
    passed explicitly.  No production call site is affected.
    """

    strategy = RetrievalStrategy.HYBRID_NO_INTENT

    def __init__(self, db, user_id: int, limit: int = DEFAULT_HYBRID_LIMIT) -> None:
        super().__init__(db)
        self._chunk_service = ChunkService(db)
        self._intent_service = IntentCategoryService(db)
        self._user_id = user_id
        self._limit = limit

    def _retrieve(self, benchmark_query: BenchmarkQuery) -> RetrievalResult:
        chunks = self._chunk_service.retrieve_hybrid(
            query=benchmark_query.query,
            user_id=self._user_id,
            limit=self._limit,
            max_intent_boost=0.0,  # disable boost; intent arm still runs for recovery
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
