from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.note import NoteCreate, NoteResponse
from app.services.note_service import NoteService

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

# Temporary until JWT auth is implemented
TEMP_USER_ID = 1


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=201
)
def create_note(
    payload: NoteCreate,
    db: Session = Depends(get_db)
):
    service = NoteService(db)

    return service.create_note(
        payload,
        user_id=TEMP_USER_ID
    )


@router.get(
    "/",
    response_model=list[NoteResponse]
)
def get_notes(
    db: Session = Depends(get_db)
):
    service = NoteService(db)

    return service.get_notes(
        user_id=TEMP_USER_ID
    )