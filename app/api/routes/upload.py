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

    allowed_extensions = {
        ".pdf",
        ".txt",
        ".docx"
    }

    # Validate the extension BEFORE writing anything to disk, and take
    # only the extension from the client-supplied filename - never the
    # filename itself. file.filename is attacker-controlled; building a
    # path directly from it (e.g. "../../something") risks writing
    # outside uploads_dir. The actual on-disk name is always a fresh
    # uuid4, so the original filename can't influence the path at all.
    original_extension = Path(file.filename or "").suffix.lower()

    if original_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    file_path = (
        uploads_dir
        / f"{uuid.uuid4()}{original_extension}"
    )

    with open(
        file_path,
        "wb"
    ) as buffer:
        buffer.write(
            file.file.read()
        )

    try:
        extracted_text = (
            DocumentService.extract_text(
                str(file_path)
            )
        )
    except Exception:
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=400,
            detail="Could not read file - it may be corrupted or not a valid file of its declared type"
        )

    note_service = NoteService(db)

    note = note_service.create_note(
        NoteCreate(
            content=extracted_text
        ),
        user_id=current_user.id
    )

    return PDFUploadResponse(
        message="File processed successfully",
        note_id=note.id
    )

