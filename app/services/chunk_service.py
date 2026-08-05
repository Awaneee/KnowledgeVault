"""
Chunk service.

Handles chunk creation, embedding storage, and retrieval.

Retrieval modes
---------------
retrieve()              — Pure semantic (vector similarity only).
retrieve_hybrid()       — Weighted fusion of semantic + intent/category evidence.
retrieve_bm25_hybrid()  — Semantic + BM25 sparse retrieval fused via RRF
                          (gated by BM25_ENABLED; falls back to retrieve_hybrid()).

Hybrid scoring (retrieve_hybrid)
---------------------------------
  final_score = (semantic_score × 0.65) + (intent_score × 0.35)

Weights are biased slightly more toward semantic than intent (0.65/0.35)
because intent categories are per-user and can be noisy — a wrong category
should not drown out a strong vector match.

Tie-breaking is deterministic:
  1. final_score  (higher wins)
  2. semantic_score (higher wins — pure content relevance)
  3. intent_score (higher wins — purpose-level evidence)
  4. note_id (lower wins — older notes ranked above newer on a tie)
  5. chunk_index (lower wins — earlier chunks first within same note)

RRF fusion (retrieve_bm25_hybrid)
----------------------------------
  rrf_score = Σ  1 / (k + rank_i)
  where k = BM25_RRF_K (default 60, from Cormack et al. 2009) and rank_i is
  the 1-based position of the note in each arm (semantic, BM25).
  Deduplication is note-level; the best-ranked chunk per note is returned.

Score filtering
---------------
Chunks below RETRIEVAL_MIN_SCORE (configurable) are excluded before the
results are returned. This prevents low-confidence noise from polluting
the context window.
"""

import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.embedding_model import embedding_model
from app.models.document_chunk import DocumentChunk
from app.repositories.bm25_repository import BM25Repository
from app.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.embedding_repository import EmbeddingRepository
from app.services.chunking_service import ChunkingService
from app.services.intent_category_service import IntentCategoryService


logger = logging.getLogger(__name__)


class ChunkService:
    MODEL_NAME = "all-MiniLM-L6-v2"

    # Semantic retrieval pool: fetch this many candidates before fusion.
    # Larger than the public `limit` so intent results have something to merge with.
    _SEMANTIC_POOL_FACTOR = 4
    _SEMANTIC_POOL_MIN = 20

    # Intent is an additive, confidence-gated ranking signal.  It cannot
    # reduce a semantic candidate's score or replace the semantic corpus.
    _MAX_INTENT_BOOST = 0.12
    _MIN_CONFIDENT_INTENT = 0.55

    def __init__(self, db: Session) -> None:
        self.db = db
        self.chunk_repo = ChunkRepository(db)
        self.embedding_repo = ChunkEmbeddingRepository(db)
        self.note_embedding_repo = EmbeddingRepository(db)
        self.intent_category_service = IntentCategoryService(db)
        self.bm25_repo = BM25Repository(db)

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    def process_note(self, note_id: int, text: str) -> int:
        if not text or not text.strip():
            logger.warning("CHUNK SKIPPED note_id=%d — empty text", note_id)
            return 0

        chunk_texts = ChunkingService.split(text)
        if not chunk_texts:
            return 0

        # Clear existing chunks for this note to maintain idempotency.
        self.db.query(DocumentChunk).filter(DocumentChunk.note_id == note_id).delete()
        self.db.commit()

        chunks = self.chunk_repo.create_chunks(
            note_id=note_id,
            texts=chunk_texts,
        )

        vectors = embedding_model.encode(chunk_texts).tolist()

        records = [
            {
                "chunk_id": chunk.id,
                "embedding_model": self.MODEL_NAME,
                "embedding_vector": vector,
            }
            for chunk, vector in zip(chunks, vectors)
        ]

        self.embedding_repo.bulk_create_embeddings(records)
        return len(chunks)

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def retrieve(self, query: str, user_id: int, limit: int = 5) -> list[dict]:
        """Pure semantic retrieval (vector similarity only)."""
        query_vector = embedding_model.encode(query).tolist()
        rows = self.embedding_repo.search_similar_chunks_with_distance(
            query_vector=query_vector,
            user_id=user_id,
            limit=limit,
        )
        results = [
            {
                "note_id": note.id,
                "note_title": note.title,
                "chunk_id": chunk.id,
                "chunk_text": chunk.chunk_text,
                "chunk_index": chunk.chunk_index,
                "semantic_score": self._distance_to_score(distance),
                "intent_score": 0.0,
                "score": self._distance_to_score(distance),
                "source": "semantic",
                "intent_category": None,
            }
            for chunk, note, distance in rows
        ]
        return self._apply_score_filter(results)

    def retrieve_hybrid(
        self,
        query: str,
        user_id: int,
        limit: int = 5,
        max_intent_boost: float | None = None,
    ) -> list[dict]:
        """
        Hybrid retrieval: semantic + intent/category evidence.
        Both arms always run. Results are merged, deduplicated, and ranked
        using weighted score fusion.

        Parameters
        ----------
        max_intent_boost
            Override for the maximum additive score boost applied to intent-
            matched candidates.  When None (default) the class constant
            _MAX_INTENT_BOOST (0.12) is used — identical to the previous
            behaviour.  Pass 0.0 to disable the boost while keeping the intent
            arm active as a candidate-recovery mechanism; this is the correct
            parameter for ablation studies that isolate the semantic-only
            ranking within the hybrid pipeline.
        """
        effective_boost_cap = (
            self._MAX_INTENT_BOOST if max_intent_boost is None else max_intent_boost
        )
        pool_size = max(limit * self._SEMANTIC_POOL_FACTOR, self._SEMANTIC_POOL_MIN)
        query_vector = embedding_model.encode(query).tolist()

        # --- Semantic arm -------------------------------------------------
        # Use the same note embeddings as the standalone semantic path.  The
        # previous implementation used a different chunk corpus, then
        # truncated chunks before note de-duplication; the two strategies were
        # therefore not comparable and repeated chunks consumed the top-K.
        semantic_rows = self.note_embedding_repo.search_similar_notes_with_distance(
            query_vector=query_vector,
            user_id=user_id,
            limit=pool_size,
        )

        # --- Intent arm ---
        category_matches = self.intent_category_service.find_category_matches_for_query(
            query=query,
            user_id=user_id,
            limit=5,
        )

        query_intent = self.intent_category_service.extractor.extract_query_intent_fast(query)
        query_confidence = float(query_intent.get("confidence") or 0.0)

        logger.info(
            "HYBRID RETRIEVAL query=%.60s semantic_pool=%d intent_categories=%d",
            query,
            len(semantic_rows),
            len(category_matches),
        )

        # Gather one representative chunk per note.  Ranking is intentionally
        # note-level: callers and evaluation both consume notes, and returning
        # several chunks of one note reduces diversity without adding recall.
        semantic_note_ids = [note.id for note, _ in semantic_rows]
        intent_note_by_id = {}
        for match in category_matches:
            for note in self.intent_category_service.get_notes_for_category(
                intent_category_id=match.category.id, user_id=user_id
            ):
                intent_note_by_id.setdefault(note.id, (note, match))

        candidate_ids = list(dict.fromkeys(semantic_note_ids + list(intent_note_by_id)))
        chunks_by_note: dict[int, list[DocumentChunk]] = {}
        for chunk in self.chunk_repo.get_chunks_by_note_ids(candidate_ids):
            chunks_by_note.setdefault(chunk.note_id, []).append(chunk)

        # --- Fused result dict keyed by note_id ---
        fused: dict[int, dict] = {}

        # Seed with semantic hits.
        for note, distance in semantic_rows:
            sem_score = self._distance_to_score(distance)
            chunk = self._best_chunk(query, chunks_by_note.get(note.id, []))
            if chunk is None:
                continue
            fused[note.id] = {
                "note_id": note.id,
                "note_title": note.title,
                "chunk_id": chunk.id,
                "chunk_text": chunk.chunk_text,
                "chunk_index": chunk.chunk_index,
                "source": "semantic",
                "intent_category": None,
                "semantic_score": sem_score,
                "intent_score": 0.0,
                "score": sem_score,
            }

        # Merge intent arm.  Confidence is deliberately gated: the fast
        # classifier is heuristic, so below its neutral confidence it has no
        # influence.  A category can recover a lexically supported note, but
        # cannot demote an existing semantic candidate.
        confidence_factor = max(
            0.0,
            (query_confidence - self._MIN_CONFIDENT_INTENT)
            / (1.0 - self._MIN_CONFIDENT_INTENT),
        )
        for note_id, (note, match) in intent_note_by_id.items():
            # Allow all matches to act as candidates to recover lexical hits,
            # but only canonical and actor-specific rule matches earn a score boost.
            is_boosted = (match.method == "canonical_name") or (
                match.method == "exact_rule" and match.category.actor is not None
            )
            
            chunk = self._best_chunk(query, chunks_by_note.get(note_id, []))
            if chunk is None:
                continue
                
            intent_score = max(0.0, min(1.0, match.score * confidence_factor))
            boost = (effective_boost_cap * intent_score) if is_boosted else 0.0
            
            current = fused.get(note_id)
            if current is None:
                semantic_score = self._text_overlap_score(
                    query, f"{note.title} {chunk.chunk_text}"
                )
                current = {
                    "note_id": note.id,
                    "note_title": note.title,
                    "chunk_id": chunk.id,
                    "chunk_text": chunk.chunk_text,
                    "chunk_index": chunk.chunk_index,
                    "source": "intent",
                    "intent_category": match.category.name,
                    "semantic_score": semantic_score,
                    "intent_score": intent_score,
                    "score": semantic_score + boost,
                }
                fused[note_id] = current
            else:
                current["source"] = "hybrid"
                current["intent_category"] = match.category.name
                current["intent_score"] = max(current["intent_score"], intent_score)
                current["score"] = current["semantic_score"] + boost

        # --- Deterministic ranking ---
        # Primary: score desc, semantic_score desc, intent_score desc.
        # Tie-break: older notes (lower note_id) and earlier chunks first.
        ranked = sorted(
            fused.values(),
            key=lambda item: (
                item["score"],
                item["semantic_score"],
                item["intent_score"],
                -item["note_id"],     # lower note_id → higher priority on tie
                -item["chunk_index"],  # lower chunk_index → earlier in note
            ),
            reverse=True,
        )

        # Thresholding belongs to AskService's prompt construction. Applying
        # it here made hybrid return fewer than K notes while semantic always
        # returned K, silently lowering recall in the retrieval API.
        result = ranked[:limit]

        logger.info(
            "HYBRID RESULT limit=%d returned=%d top_score=%.3f filtered_out=%d",
            limit,
            len(result),
            result[0]["score"] if result else 0.0,
            len(ranked) - len(result) if len(ranked) > limit else 0,
        )

        return result

    def retrieve_bm25_hybrid(
        self, query: str, user_id: int, limit: int = 5
    ) -> list[dict]:
        """
        Hybrid retrieval: dense semantic + sparse BM25 fused via Reciprocal Rank Fusion.

        When BM25_ENABLED is False this method is a transparent alias for
        retrieve_hybrid() so the call site never needs to branch.  The
        RRF logic lives in _retrieve_rrf_hybrid() which is also callable
        directly (without the flag check) by the evaluation framework.
        """
        if not settings.BM25_ENABLED:
            return self.retrieve_hybrid(query=query, user_id=user_id, limit=limit)
        return self._retrieve_rrf_hybrid(
            query=query,
            user_id=user_id,
            limit=limit,
            k=settings.BM25_RRF_K,
            pool=settings.BM25_CANDIDATE_POOL,
        )

    def _retrieve_rrf_hybrid(
        self,
        query: str,
        user_id: int,
        limit: int = 5,
        k: int = 60,
        pool: int = 20,
    ) -> list[dict]:
        """
        Core RRF fusion — always runs both arms regardless of BM25_ENABLED.

        Called by retrieve_bm25_hybrid() (production, flag-gated) and
        directly by HybridBM25Adapter (evaluation, always-on).

        Algorithm
        ---------
        1. Fetch *pool* candidates from each arm independently.
        2. Deduplicate to note level.
        3. Compute RRF score:  rrf = Σ  1 / (k + rank_i)
           A note absent from an arm contributes 0 from that arm.
        4. Sort by rrf descending; return top *limit* results.
        """
        query_vector = embedding_model.encode(query).tolist()

        # --- Semantic arm (note-level) ---
        semantic_rows = self.note_embedding_repo.search_similar_notes_with_distance(
            query_vector=query_vector,
            user_id=user_id,
            limit=pool,
        )

        # --- BM25 arm (chunk-level; deduplicate to note-level) ---
        bm25_raw = self.bm25_repo.search(query=query, user_id=user_id, limit=pool)

        # First occurrence per note_id is the best-scoring BM25 chunk.
        bm25_note_map: dict[int, dict] = {}
        for row in bm25_raw:
            bm25_note_map.setdefault(row["note_id"], row)

        logger.info(
            "BM25 HYBRID query=%.60s semantic_pool=%d bm25_hits=%d unique_bm25_notes=%d",
            query,
            len(semantic_rows),
            len(bm25_raw),
            len(bm25_note_map),
        )

        # --- RRF fusion ---
        rrf_scores: dict[int, float] = {}

        for rank, (note, _distance) in enumerate(semantic_rows, start=1):
            rrf_scores[note.id] = rrf_scores.get(note.id, 0.0) + 1.0 / (k + rank)

        for rank, (note_id, _row) in enumerate(bm25_note_map.items(), start=1):
            rrf_scores[note_id] = rrf_scores.get(note_id, 0.0) + 1.0 / (k + rank)

        ranked_note_ids = sorted(rrf_scores, key=rrf_scores.__getitem__, reverse=True)

        candidate_ids = ranked_note_ids[: max(limit * 2, pool)]
        note_by_id = {note.id: note for note, _ in semantic_rows}

        chunks_by_note: dict[int, list[DocumentChunk]] = {}
        for chunk in self.chunk_repo.get_chunks_by_note_ids(candidate_ids):
            chunks_by_note.setdefault(chunk.note_id, []).append(chunk)

        semantic_ids = {n.id for n, _ in semantic_rows}
        results: list[dict] = []
        for note_id in ranked_note_ids[:limit]:
            rrf = rrf_scores[note_id]
            note = note_by_id.get(note_id)
            bm25_row = bm25_note_map.get(note_id)

            if note is not None:
                note_title = note.title
            elif bm25_row is not None:
                note_title = bm25_row["note_title"]
            else:
                continue

            chunk = self._best_chunk(query, chunks_by_note.get(note_id, []))
            if chunk is None:
                if bm25_row is None:
                    continue
                chunk_text  = bm25_row["chunk_text"]
                chunk_index = bm25_row["chunk_index"]
                chunk_id    = bm25_row["chunk_id"]
            else:
                chunk_text  = chunk.chunk_text
                chunk_index = chunk.chunk_index
                chunk_id    = chunk.id

            in_semantic = note_id in semantic_ids
            in_bm25     = note_id in bm25_note_map
            if in_semantic and in_bm25:
                source = "hybrid_bm25"
            elif in_bm25:
                source = "bm25"
            else:
                source = "semantic"

            results.append({
                "note_id":         note_id,
                "note_title":      note_title,
                "chunk_id":        chunk_id,
                "chunk_text":      chunk_text,
                "chunk_index":     chunk_index,
                "rrf_score":       rrf,
                "score":           rrf,
                "semantic_score":  rrf,
                "intent_score":    0.0,
                "source":          source,
                "intent_category": None,
            })

        logger.info(
            "BM25 HYBRID RESULT limit=%d returned=%d top_rrf=%.4f",
            limit,
            len(results),
            results[0]["rrf_score"] if results else 0.0,
        )
        return results

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _distance_to_score(distance: float) -> float:
        try:
            return max(0.0, min(1.0, 1.0 - float(distance)))
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _text_overlap_score(query: str, text: str) -> float:
        import re
        query_tokens = {
            t for t in re.findall(r"[a-z0-9]+", query.lower()) if len(t) > 2
        }
        text_tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
        if not query_tokens:
            return 0.0
        return len(query_tokens & text_tokens) / len(query_tokens)

    def _best_chunk(self, query: str, chunks: list[DocumentChunk]) -> DocumentChunk | None:
        """Pick a stable, query-relevant preview chunk for a ranked note."""
        if not chunks:
            return None
        return max(
            chunks,
            key=lambda chunk: (
                self._text_overlap_score(query, chunk.chunk_text),
                -chunk.chunk_index,
            ),
        )

    @staticmethod
    def _apply_score_filter(chunks: list[dict]) -> list[dict]:
        """Remove chunks below the configured minimum score threshold."""
        min_score = settings.RETRIEVAL_MIN_SCORE
        if min_score <= 0.0:
            return chunks
        return [c for c in chunks if c.get("score", 0.0) >= min_score]
