from sqlalchemy.orm import Session
from app.models.attachment import Attachment
from app.models.notes import Note


class AttachmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_attachment(
        self,
        filename: str,
        file_path: str,
        file_type: str,
        note_id: int,
    ) -> Attachment:
        attachment = Attachment(
            filename=filename,
            file_path=file_path,
            file_type=file_type,
            note_id=note_id,
        )
        self.db.add(attachment)
        self.db.commit()
        self.db.refresh(attachment)
        return attachment

    def get_attachments_by_user(self, user_id: int) -> list[Attachment]:
        return (
            self.db.query(Attachment)
            .join(Note, Note.id == Attachment.note_id)
            .filter(Note.user_id == user_id)
            .all()
        )

    def get_attachments_by_note(self, note_id: int) -> list[Attachment]:
        return self.db.query(Attachment).filter(Attachment.note_id == note_id).all()

    def get_by_id(self, attachment_id: int) -> Attachment | None:
        return self.db.query(Attachment).filter(Attachment.id == attachment_id).first()