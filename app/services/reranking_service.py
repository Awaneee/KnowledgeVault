"""
Cross-encoder reranking service.

Takes a list of hybrid retrieval candidates (dicts as returned by
ChunkService.retrieve_hybrid) and re-scores each (query, chunk_text)
pair using a cross-encoder.  Returns candidates sorted by reranker score
and truncated to top_k.

Graceful degradation
--------------------
If reranking is disabled (RERANKING_ENABLED=False), the model failed to
load, or inference raises an exception, the service returns the original
candidate ordering unchanged with reranked=False.  The request is never
failed because of a reranker error.

Cache
-----
Reranker scores are deterministic for the same (query, candidate set).
Scores are cached in Redis under:

    rerank:{user_id}:{SHA-256(normalised_query + sorted_note_ids)}

TTL = RERANK_CACHE_TTL_SECONDS (default 900 s).
The cache key changes naturally when the note set changes (new ingestion
adds/removes note IDs), so no explicit invalidation is needed.
"""

from __future__ import annotations

import hashlib
import logging
import time
from typing import NamedTuple

from app.core.config import settings
from app.core.rerank_model import rerank_model
from app.services.cache_service import CacheService

logger = logging.getLogger(__name__)


class RerankResult(NamedTuple):
    """Returned by RerankingService.rerank()."""
    candidates: list[dict]
    reranked: bool


class RerankingService:
    """All methods are static — no per-instance state."""

    @staticmethod
    def rerank(
        query: str,
        candidates: list[dict],
        top_k: int,
        user_id: int,
    ) -> RerankResult:
        """
        Re-score candidates with the cross-encoder and return the top_k
        sorted by reranker score.

        Parameters
        ----------
        query      : The user's question (plain text).
        candidates : Output of ChunkService.retrieve_hybrid — each dict
                     must have ``note_id`` (int) and ``chunk_text`` (str).
        top_k      : Maximum number of candidates to return.
        user_id    : Used to namespace the Redis cache key.

        Returns
        -------
        RerankResult(candidates, reranked)
          candidates : Top-k list, ordered by reranker score (or original
                       order on fallback).
          reranked   : True iff the cross-encoder was actually applied.
        """
        if not settings.RERANKING_ENABLED or rerank_model is None:
            return RerankResult(candidates=candidates[:top_k], reranked=False)

        if not candidates:
            return RerankResult(candidates=[], reranked=False)

        # --- Cache lookup -------------------------------------------------
        cache_key = RerankingService._cache_key(user_id, query, candidates)
        cached = CacheService.get(cache_key)
        if cached is not None:
            logger.debug("RERANK CACHE HIT user_id=%d query=%.60s", user_id, query)
            reordered = RerankingService._apply_cached_scores(
                cached, candidates, top_k
            )
            return RerankResult(candidates=reordered, reranked=True)

        # --- Inference ----------------------------------------------------
        try:
            t0 = time.monotonic()
            pairs = [(query, c["chunk_text"]) for c in candidates]
            scores = rerank_model.predict(pairs)
            elapsed_ms = (time.monotonic() - t0) * 1000.0

            logger.info(
                "RERANK INFERENCE user_id=%d candidates=%d elapsed=%.1fms",
                user_id,
                len(candidates),
                elapsed_ms,
            )

            # Sort candidates by descending reranker score.
            scored_pairs = sorted(
                zip(scores, candidates),
                key=lambda x: x[0],
                reverse=True,
            )
            reranked_candidates = [c for _, c in scored_pairs]

            # Persist scores to Redis so repeated queries skip inference.
            score_map = [
                {"note_id": c["note_id"], "score": float(s)}
                for s, c in zip(scores, candidates)
            ]
            CacheService.set(
                cache_key,
                score_map,
                expire_seconds=settings.RERANK_CACHE_TTL_SECONDS,
            )

            return RerankResult(
                candidates=reranked_candidates[:top_k],
                reranked=True,
            )

        except Exception as exc:
            logger.error(
                "RERANK INFERENCE FAILED — falling back to original ordering: %s",
                exc,
            )
            return RerankResult(candidates=candidates[:top_k], reranked=False)

    # ------------------------------------------------------------------
    # Internals
    # ------------------------------------------------------------------

    @staticmethod
    def _cache_key(user_id: int, query: str, candidates: list[dict]) -> str:
        """
        Build a stable cache key from (user_id, query, note_id set).

        Sorting note_ids makes the key independent of upstream ANN ordering,
        so two runs that return the same candidate pool in different order
        share a cache entry.
        """
        sorted_ids = ",".join(
            str(nid)
            for nid in sorted(c["note_id"] for c in candidates)
        )
        normalised = query.strip().lower()
        digest = hashlib.sha256(
            f"{normalised}:{sorted_ids}".encode()
        ).hexdigest()
        return f"rerank:{user_id}:{digest}"

    @staticmethod
    def _apply_cached_scores(
        score_map: list[dict],
        candidates: list[dict],
        top_k: int,
    ) -> list[dict]:
        """Re-order candidates using note_id → score mapping from cache."""
        score_by_note_id = {
            entry["note_id"]: entry["score"] for entry in score_map
        }
        reordered = sorted(
            candidates,
            key=lambda c: score_by_note_id.get(c["note_id"], 0.0),
            reverse=True,
        )
        return reordered[:top_k]
