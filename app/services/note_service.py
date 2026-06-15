from sqlalchemy.orm import Session

from app.schemas.note import NoteCreate
from app.schemas.note import NoteResponse
from app.schemas.note import NoteSearchResponse

from app.repositories.note_repository import NoteRepository
from app.services.embedding_service import EmbeddingService


class NoteService:
    def __init__(self, db: Session):
        self.repo = NoteRepository(db)
        self.embedding_service = EmbeddingService(db)

    def create_note(
        self,
        data: NoteCreate,
        user_id: int,
    ) -> NoteResponse:

        note = self.repo.create_note(
            title=data.title,
            content=data.content,
            user_id=user_id,
            category_id=data.category_id,
        )

        text_for_embedding = (
            f"{note.title}\n{note.content or ''}"
        )

        self.embedding_service.generate_and_store(
            note_id=note.id,
            text=text_for_embedding,
        )

        return NoteResponse.model_validate(note)

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