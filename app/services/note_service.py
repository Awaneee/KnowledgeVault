from sqlalchemy.orm import Session

from app.repositories.note_repository import NoteRepository
from app.schemas.note import NoteCreate, NoteResponse


class NoteService:
    def __init__(self, db: Session):
        self.repo = NoteRepository(db)

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