import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.services.attachment_service import AttachmentService
from app.repositories.note_repository import NoteRepository
from app.schemas.attachment import AttachmentCreate, AttachmentResponse

router = APIRouter(prefix="/attachments", tags=["attachments"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/", response_model=AttachmentResponse, status_code=201)
def upload_attachment(
    note_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note_repo = NoteRepository(db)
    matched_note = note_repo.get_note_by_id(note_id)
    if not matched_note:
        raise HTTPException(status_code=404, detail="Note not found")
    if matched_note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    service = AttachmentService(db)
    data = AttachmentCreate(
        filename=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        note_id=note_id
    )
    return service.create_attachment(data)


@router.get("/", response_model=list[AttachmentResponse])
def list_attachments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = AttachmentService(db)
    return service.get_attachments(current_user.id)


@router.get("/{attachment_id}", response_model=AttachmentResponse)
def get_attachment(
    attachment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = AttachmentService(db)
    attachment = service.repo.get_by_id(attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    if attachment.note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return attachment