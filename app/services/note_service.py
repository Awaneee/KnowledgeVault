import logging
import os
import traceback

from sqlalchemy.orm import Session

from app.schemas.note import NoteCreate
from app.schemas.note import NoteCreateResponse
from app.schemas.note import NoteResponse
from app.schemas.note import NoteSearchResponse

from app.repositories.note_repository import NoteRepository
from app.schemas.intent import IntentCategoryResponse
from app.schemas.intent import NoteIntentResponse
from app.services.cache_service import CacheService
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.intent_category_service import IntentCategoryService


logger = logging.getLogger(__name__)


class NoteService:
    def __init__(self, db: Session):
        self.repo = NoteRepository(db)
        self.embedding_service = EmbeddingService(db)
        self.chunk_service = ChunkService(db)
        self.intent_category_service = IntentCategoryService(db)

    def create_notes_bulk(
        self,
        notes: list[str],
        user_id: int
    ) -> list[NoteCreateResponse]:
        # create_notes_bulk was previously defined BEFORE __init__,
        # which means self.repo/embedding_service etc. would not exist
        # when it ran. Also replaced silent print() with logger.exception
        # so bulk failures are actually visible in logs with tracebacks.
        results = []

        for content in notes:
            try:
                result = self.create_note(
                    NoteCreate(content=content),
                    user_id=user_id
                )
                results.append(result)

            except Exception:
                logger.exception(
                    f"Failed to create note for user {user_id}: {content[:80]!r}"
                )

        return results

    def create_note(
        self,
        data: NoteCreate,
        user_id: int,
    ) -> NoteCreateResponse:
        title = (data.content or "").strip()
        if len(title) > 120:
            title = title[:120]
        title_source = "content"

        note = self.repo.create_note(
            title=title,
            content=data.content,
            user_id=user_id,
            category_id=None,
            auto_title_source=title_source,
            organization_status="pending"
        )

        from app.services.queue_service import QueueService
        QueueService.enqueue_note_processing(
            note_id=note.id,
            user_id=user_id
        )

        return NoteCreateResponse.model_validate(note)

    def get_notes(
        self,
        user_id: int,
    ) -> list[NoteResponse]:

        notes = self.repo.get_notes_by_user(user_id)

        return [
            NoteResponse.model_validate(note)
            for note in notes
        ]

    def search_notes(
        self,
        query: str,
        user_id: int
    ) -> list[NoteSearchResponse]:

        notes = self.embedding_service.search_notes(
            query=query,
            user_id=user_id
        )

        return [
            NoteSearchResponse.model_validate(note)
            for note in notes
        ]

    def delete_note(self, note_id: int, user_id: int) -> bool:
        """Delete a note owned by user_id. Returns False if not found or not owned."""
        note = self.repo.get_note_by_id(note_id)
        if not note or note.user_id != user_id:
            return False
        # Collect file paths before the DB cascade removes Attachment records.
        attachment_paths = [a.file_path for a in note.attachments]
        deleted = self.repo.delete_note_by_id(note_id)
        if deleted:
            for path in attachment_paths:
                try:
                    os.remove(path)
                except OSError as exc:
                    logger.warning("Could not remove attachment file %s: %s", path, exc)
            CacheService.delete_pattern(f"ask:{user_id}:*")
            CacheService.delete_pattern(f"semantic_search:{user_id}:*")
        return deleted

    def get_related_notes(
        self,
        note_id: int,
        user_id: int
    ) -> list[NoteSearchResponse]:

        # Ownership check happens here, before the note_id ever reaches
        # the embedding repository. Without this, get_related_notes
        # would use *any* note's embedding as the similarity anchor
        # regardless of who owns it - meaning a caller could pass
        # another user's note_id and learn which of their own notes
        # are semantically close to that private note's content, even
        # though the private note itself is never returned directly.
        source_note = self.repo.get_note_by_id(note_id)

        if not source_note or source_note.user_id != user_id:
            return []

        notes = self.embedding_service.get_related_notes(
            note_id=note_id,
            user_id=user_id
        )

        return [
            NoteSearchResponse.model_validate(note)
            for note in notes
        ]
