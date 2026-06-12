from sqlalchemy.orm import Session

from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate
from app.schemas.note import NoteResponse
from app.services.embedding_service import EmbeddingService


class NoteService:
    def __init__(self, db: Session):
        self.repo = NoteRepository(db)
        self.embedding_service = EmbeddingService(db)

    def create_note(
        self,
        data: NoteCreate,
        user_id: int
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
          text=text_for_embedding
)

        print("NOTE CREATED")
        print("ID:", note.id)
        print("CREATED_AT:", note.created_at)

        return NoteResponse.model_validate(note)

    def get_notes(
        self,
        user_id: int
    ) -> list[NoteResponse]:

        notes = self.repo.get_notes_by_user(user_id)

        return [
            NoteResponse.model_validate(note)
            for note in notes
        ]