from sqlalchemy.orm import Session

from app.schemas.note import NoteCreate
from app.schemas.note import NoteCreateResponse
from app.schemas.note import NoteResponse
from app.schemas.note import NoteSearchResponse

from app.repositories.note_repository import NoteRepository
from app.schemas.intent import IntentCategoryResponse
from app.schemas.intent import NoteIntentResponse
from app.services.chunk_service import ChunkService
from app.services.embedding_service import EmbeddingService
from app.services.intent_category_service import IntentCategoryService
from app.services.title_generation_service import TitleGenerationService


class NoteService:
    def __init__(self, db: Session):
        self.repo = NoteRepository(db)
        self.embedding_service = EmbeddingService(db)
        self.chunk_service = ChunkService(db)
        self.intent_category_service = IntentCategoryService(db)
        self.title_generation_service = TitleGenerationService()

    def create_note(
        self,
        data: NoteCreate,
        user_id: int,
    ) -> NoteCreateResponse:
        title, title_source = self.title_generation_service.generate(
            data.content
        )

        note = self.repo.create_note(
            title=title,
            content=data.content,
            user_id=user_id,
            category_id=None,
            auto_title_source=title_source,
            organization_status="pending"
        )

        text_for_embedding = (
            f"{note.title}\n{note.content or ''}"
        )

        self.embedding_service.generate_and_store(
            note_id=note.id,
            text=text_for_embedding,
        )

        self.chunk_service.process_note(
            note_id=note.id,
            text=note.content or note.title
        )

        intent_result = None

        try:
            intent_result = self.intent_category_service.process_note(
                note_id=note.id,
                user_id=user_id,
                title=note.title,
                content=note.content
            )
            note = self.repo.update_organization_status(
                note_id=note.id,
                status="organized"
            ) or note
        except Exception:
            self.repo.db.rollback()
            note = self.repo.update_organization_status(
                note_id=note.id,
                status="failed"
            ) or note

        response = NoteCreateResponse.model_validate(note)

        if intent_result:
            response.intent = NoteIntentResponse.model_validate(
                intent_result["intent"]
            )
            response.intent_category = IntentCategoryResponse.model_validate(
                intent_result["category"]
            )

        return response

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

    def get_related_notes(
        self,
        note_id: int,
        user_id: int
    ) -> list[NoteSearchResponse]:

        notes = self.embedding_service.get_related_notes(
            note_id=note_id,
            user_id=user_id
        )

        return [
            NoteSearchResponse.model_validate(note)
            for note in notes
        ]
