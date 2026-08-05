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
        auto_title_source: str = "heuristic",
        organization_status: str = "pending"
    ) -> Note:
        note = Note(
            title=title,
            content=content,
            user_id=user_id,
            category_id=category_id,
            auto_title_source=auto_title_source,
            organization_status=organization_status
        )

        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)

        return note

    def update_organization_status(
        self,
        note_id: int,
        status: str
    ) -> Note | None:
        note = (
            self.db.query(Note)
            .filter(Note.id == note_id)
            .first()
        )

        if not note:
            return None

        note.organization_status = status
        self.db.commit()
        self.db.refresh(note)
        return note

    def get_notes_by_user(self, user_id: int) -> list[Note]:
        return (
            self.db.query(Note)
            .filter(Note.user_id == user_id)
            .all()
        )

    def get_note_by_id(self, note_id: int) -> Note | None:
        return (
            self.db.query(Note)
            .filter(Note.id == note_id)
            .first()
        )

    def delete_note_by_id(self, note_id: int) -> bool:
        """Delete note and all cascaded children. Returns True if deleted."""
        note = self.get_note_by_id(note_id)
        if not note:
            return False
        self.db.delete(note)
        self.db.commit()
        return True
