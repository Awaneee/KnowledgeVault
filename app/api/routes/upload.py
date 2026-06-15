from pathlib import Path
import uuid

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.database.session import get_db
from app.models.user import User

from app.schemas.note import NoteCreate
from app.schemas.upload import PDFUploadResponse

from app.services.note_service import NoteService
from app.services.document_service import DocumentService


router = APIRouter(
    prefix="/uploads",
    tags=["uploads"]
)


@router.post(
    "/file",
    response_model=PDFUploadResponse
)
def upload_file(
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

    allowed_extensions = {
        ".pdf",
        ".txt",
        ".docx"
    }

    extension = (
        file_path.suffix.lower()
    )

    if extension not in allowed_extensions:
        file_path.unlink(
            missing_ok=True
        )

        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    extracted_text = (
        DocumentService.extract_text(
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
        message="File processed successfully",
        note_id=note.id
    )