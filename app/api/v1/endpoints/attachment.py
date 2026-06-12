import os
import uuid

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.attachment import (
    AttachmentCreate,
    AttachmentResponse,
)
from app.services.attachment_service import (
    AttachmentService,
)

router = APIRouter(tags=["Attachments"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post(
    "/attachments",
    response_model=AttachmentResponse,
    status_code=201,
)
def upload_attachment(
    note_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not note_id:
        raise HTTPException(
            status_code=400,
            detail="note_id is required"
        )

    ext = os.path.splitext(file.filename)[-1]
    unique_filename = f"{uuid.uuid4().hex}{ext}"

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    contents = file.file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    data = AttachmentCreate(
        filename=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        note_id=note_id,
    )

    service = AttachmentService(db)

    return service.create_attachment(data)


@router.get(
    "/attachments",
    response_model=list[AttachmentResponse]
)
def get_all_attachments(
    db: Session = Depends(get_db)
):
    service = AttachmentService(db)

    return service.get_attachments()


@router.get(
    "/notes/{note_id}/attachments",
    response_model=list[AttachmentResponse]
)
def get_note_attachments(
    note_id: int,
    db: Session = Depends(get_db)
):
    service = AttachmentService(db)

    return service.get_note_attachments(note_id)