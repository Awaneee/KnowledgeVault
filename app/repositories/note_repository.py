from sqlalchemy.orm import Session

from app.models.notes import Note


class NoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_note(
        self,
        title: str,
        content: str | None,
        user_id: int,
        category_id: int | None,
    ) -> Note:
        note = Note(
            title=title,
            content=content,
            user_id=user_id,
            category_id=category_id,
        )

        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)

        return note

    def get_notes_by_user(self, user_id: int) -> list[Note]:
        return (
            self.db.query(Note)
            .filter(Note.user_id == user_id)
            .all()
        )