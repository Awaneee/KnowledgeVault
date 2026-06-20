import logging
import traceback

from sqlalchemy.orm import Session

from app.repositories.note_repository import NoteRepository
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.intent_category_service import IntentCategoryService

logger = logging.getLogger(__name__)


class NoteProcessingService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = NoteRepository(db)
        self.embedding_service = EmbeddingService(db)
        self.chunk_service = ChunkService(db)
        self.intent_category_service = IntentCategoryService(db)

    def process_note(
        self,
        note_id: int,
        user_id: int
    ):
        note = self.repo.get_note_by_id(note_id)
        if not note:
            logger.error(f"Note not found for processing: {note_id}")
            return

        try:
            # Transition to processing state
            self.repo.update_organization_status(
                note_id=note_id,
                status="processing"
            )

            # Generate and store embedding
            text_for_embedding = f"{note.title}\n{note.content or ''}"
            self.embedding_service.generate_and_store(
                note_id=note.id,
                text=text_for_embedding,
            )

            # Process chunks
            self.chunk_service.process_note(
                note_id=note.id,
                text=note.content or note.title
            )

            # Extract intent and category
            self.intent_category_service.process_note(
                note_id=note.id,
                user_id=user_id,
                title=note.title,
                content=note.content
            )

            # Transition to organized state
            self.repo.update_organization_status(
                note_id=note.id,
                status="organized"
            )

        except Exception as exc:
            logger.exception(
                "%s\nINTENT ORGANIZATION FAILED\n%s\n\nType: %s\nMessage: %s\n\n%s",
                "=" * 80,
                "=" * 80,
                type(exc).__name__,
                exc,
                traceback.format_exc()
            )
            self.db.rollback()
            self.repo.update_organization_status(
                note_id=note.id,
                status="failed"
            )
            raise exc
