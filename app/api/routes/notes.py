from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.services.note_service import NoteService
from app.services.related_notes_service import RelatedNotesService
from app.schemas.attachment import AttachmentResponse
from app.schemas.note import (
    NoteCreate,
    BulkNoteCreate,
    NoteCreateResponse,
    NoteResponse,
    NoteSearchResponse,
    RelatedNoteResponse,
)

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)


@router.post(
    "/",
    response_model=NoteCreateResponse,
    status_code=201
)
def create_note(
    data: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = NoteService(db)

    return service.create_note(
        data,
        user_id=current_user.id
    )
@router.post(
    "/bulk",
    response_model=list[NoteCreateResponse]
)
def create_notes_bulk(
    data: BulkNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = NoteService(db)

    return service.create_notes_bulk(
        notes=data.notes,
        user_id=current_user.id
    )


@router.get(
    "/",
    response_model=list[NoteResponse]
)
def list_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = NoteService(db)

    return service.get_notes(
        user_id=current_user.id
    )


@router.get(
    "/search",
    response_model=list[NoteSearchResponse]
)
def search_notes(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = NoteService(db)

    return service.search_notes(
        query=q,
        user_id=current_user.id
    )


@router.get("/{note_id}/related", response_model=list[RelatedNoteResponse])
def get_related_notes(
    note_id: int,
    limit: int = Query(default=5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return the top-N semantically similar notes using pgvector cosine distance."""
    service = RelatedNotesService(db)
    return service.get_related(note_id=note_id, user_id=current_user.id, limit=limit)


@router.get(
    "/{note_id}",
    response_model=NoteResponse
)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = NoteService(db)

    note = service.repo.get_note_by_id(note_id)

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden"
        )

    return note


@router.delete("/{note_id}", status_code=204)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = NoteService(db)
    note = service.repo.get_note_by_id(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    if note.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")
    service.delete_note(note_id=note_id, user_id=current_user.id)


@router.get("/{note_id}/attachments", response_model=list[AttachmentResponse])
def get_note_attachments(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = NoteService(db)

    note = service.repo.get_note_by_id(note_id)

    if not note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    if note.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access forbidden"
        )

    return note.attachments

