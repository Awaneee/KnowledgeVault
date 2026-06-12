from sqlalchemy.orm import Session
from app.models.attachment import Attachment


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

    def get_attachments(self) -> list[Attachment]:
        return self.db.query(Attachment).all()

    def get_attachments_by_note(self, note_id: int) -> list[Attachment]:
        return self.db.query(Attachment).filter(Attachment.note_id == note_id).all()

    def get_by_id(self, attachment_id: int) -> Attachment | None:
        return self.db.query(Attachment).filter(Attachment.id == attachment_id).first()