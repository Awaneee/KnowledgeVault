"""
Chunk service.

Handles chunk creation, embedding storage, and retrieval.

Retrieval modes
---------------
retrieve()         — Pure semantic (vector similarity only).
retrieve_hybrid()  — Weighted fusion of semantic + intent/category evidence.

Hybrid scoring
--------------
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
        self, query: str, user_id: int, limit: int = 5
    ) -> list[dict]:
        """
        Hybrid retrieval: semantic + intent/category evidence.
        Both arms always run. Results are merged, deduplicated, and ranked
        using weighted score fusion.
        """
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
            boost = (self._MAX_INTENT_BOOST * intent_score) if is_boosted else 0.0
            
            current = fused.get(note_id)
            if current is None:
                semantic_score = self._text_overlap_score(
                    query, f"{note.title} {chunk.chunk_text}"
                )
                current = {
                    "note_id": note.id,
                    "note_title": note.title,
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
