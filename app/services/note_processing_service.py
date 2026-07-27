"""
Note processing service.

Orchestrates the full indexing pipeline for a single note:
  1. Embedding generation
  2. Chunk creation + chunk embeddings
  3. Intent extraction + category assignment

Every stage is timed and logged.  Failures in any stage are caught,
the DB is rolled back, and the note is marked as "failed" so it can
be retried without leaving partial state.
"""

import logging
import time

from sqlalchemy.orm import Session

from app.repositories.note_repository import NoteRepository
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.intent_category_service import IntentCategoryService


logger = logging.getLogger(__name__)

# Maximum number of characters sent to downstream LLM services.
# Notes longer than this are truncated for intent extraction only;
# the full text is still stored, chunked, and embedded normally.
_LLM_TEXT_LIMIT = 4000


class NoteProcessingService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = NoteRepository(db)
        self.embedding_service = EmbeddingService(db)
        self.chunk_service = ChunkService(db)
        self.intent_category_service = IntentCategoryService(db)

    def process_note(self, note_id: int, user_id: int) -> None:
        note = self.repo.get_note_by_id(note_id)
        if not note:
            logger.error("NOTE NOT FOUND note_id=%d — skipping", note_id)
            return

        # Guard: normalise empty/whitespace titles.
        title = (note.title or "").strip() or "Untitled"
        content = (note.content or "").strip() or None

        logger.info(
            "\n%s\nNOTE PIPELINE START note_id=%d user_id=%d title=%.60s\n%s",
            "=" * 60,
            note_id,
            user_id,
            title,
            "=" * 60,
        )

        pipeline_start = time.monotonic()

        try:
            self.repo.update_organization_status(
                note_id=note_id, status="processing"
            )

            # Stage 1 — Note-level embedding.
            t = time.monotonic()
            text_for_embedding = f"{title}\n{content}" if content else title
            self.embedding_service.generate_and_store(
                note_id=note.id,
                text=text_for_embedding,
            )
            logger.info(
                "STAGE embedding note_id=%d elapsed=%.2fs",
                note_id,
                time.monotonic() - t,
            )

            # Stage 2 — Chunking + chunk embeddings.
            t = time.monotonic()
            chunk_text = content or title
            chunk_count = self.chunk_service.process_note(
                note_id=note.id,
                text=chunk_text,
            )
            logger.info(
                "STAGE chunking note_id=%d chunks=%d elapsed=%.2fs",
                note_id,
                chunk_count,
                time.monotonic() - t,
            )

            # Stage 3 — Intent extraction + category assignment.
            t = time.monotonic()
            result = self.intent_category_service.process_note(
                note_id=note.id,
                user_id=user_id,
                title=title,
                content=content,
            )
            category = result["category"]
            # category is None when the per-user cap is reached; the note is
            # still fully indexed (embedding + chunks) and retrievable via
            # semantic search.
            category_name = category.name if category is not None else "<uncategorized>"
            logger.info(
                "STAGE intent note_id=%d category=%r elapsed=%.2fs",
                note_id,
                category_name,
                time.monotonic() - t,
            )

            self.repo.update_organization_status(
                note_id=note.id, status="organized"
            )

            total = time.monotonic() - pipeline_start
            logger.info(
                "NOTE PIPELINE DONE note_id=%d category=%r total=%.2fs",
                note_id,
                category_name,
                total,
            )

        except Exception as exc:
            logger.exception(
                "NOTE PIPELINE FAILED note_id=%d error=%s", note_id, exc
            )
            try:
                self.db.rollback()
                self.repo.update_organization_status(
                    note_id=note.id, status="failed"
                )
            except Exception as rollback_exc:
                logger.error(
                    "ROLLBACK FAILED note_id=%d error=%s", note_id, rollback_exc
                )
            raise
