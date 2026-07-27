from sqlalchemy.orm import Session

from app.repositories.attachment_repository import AttachmentRepository
from app.schemas.attachment import AttachmentCreate, AttachmentResponse


class AttachmentService:
    def __init__(self, db: Session):
        self.repo = AttachmentRepository(db)

    def create_attachment(
        self,
        data: AttachmentCreate
    ) -> AttachmentResponse:

        attachment = self.repo.create_attachment(
            filename=data.filename,
            file_path=data.file_path,
            file_type=data.file_type,
            note_id=data.note_id,
        )

        return AttachmentResponse.model_validate(attachment)

    def get_attachments(self, user_id: int) -> list[AttachmentResponse]:

        attachments = self.repo.get_attachments_by_user(user_id)

        return [
            AttachmentResponse.model_validate(a)
            for a in attachments
        ]

    def get_note_attachments(
        self,
        note_id: int
    ) -> list[AttachmentResponse]:

        attachments = self.repo.get_attachments_by_note(note_id)

        return [
            AttachmentResponse.model_validate(a)
            for a in attachments
        ]