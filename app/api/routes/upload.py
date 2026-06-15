from pathlib import Path
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.note import NoteCreate
from app.schemas.upload import PDFUploadResponse
from app.services.note_service import NoteService
from app.services.pdf_services import PDFService


router = APIRouter(
    prefix="/uploads",
    tags=["uploads"]
)


@router.post(
    "/pdf",
    response_model=PDFUploadResponse
)
def upload_pdf(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    uploads_dir = Path("uploads")

    uploads_dir.mkdir(
        exist_ok=True
    )

    file_path = (
        uploads_dir
        / f"{uuid.uuid4()}_{file.filename}"
    )

    with open(
        file_path,
        "wb"
    ) as buffer:
        buffer.write(
            file.file.read()
        )

    extracted_text = (
        PDFService.extract_text(
            str(file_path)
        )
    )

    note_service = NoteService(db)

    note = note_service.create_note(
        NoteCreate(
            title=file.filename,
            content=extracted_text,
            category_id=None
        ),
        user_id=current_user.id
    )

    return PDFUploadResponse(
        message="PDF processed successfully",
        note_id=note.id
    )