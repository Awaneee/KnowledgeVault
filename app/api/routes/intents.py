from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.database.session import get_db
from app.models.intent_category import IntentCategory
from app.models.user import User
from app.repositories.intent_repository import IntentRepository
from app.schemas.intent import IntentCategoryResponse
from app.schemas.intent import IntentBackfillResponse
from app.schemas.intent import IntentNoteResponse
from app.schemas.intent import NoteIntentResponse
from app.services.intent_category_service import IntentCategoryService


router = APIRouter(
    prefix="/intents",
    tags=["intents"]
)


@router.get(
    "/categories",
    response_model=list[IntentCategoryResponse]
)
def list_intent_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = IntentCategoryService(db)

    return service.get_categories(
        user_id=current_user.id
    )


@router.get(
    "/categories/{intent_category_id}/notes",
    response_model=list[IntentNoteResponse]
)
def list_notes_for_intent_category(
    intent_category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(IntentCategory).filter(
        IntentCategory.id == intent_category_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Intent category not found")
    if category.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access forbidden")

    service = IntentCategoryService(db)
    return service.get_notes_for_category(
        intent_category_id=intent_category_id,
        user_id=current_user.id
    )


@router.get(
    "/notes/{note_id}",
    response_model=NoteIntentResponse
)
def get_note_intent(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = IntentRepository(db)
    intent = repo.get_note_intent(
        note_id=note_id,
        user_id=current_user.id
    )

    if not intent:
        raise HTTPException(
            status_code=404,
            detail="Intent not found for note"
        )

    return intent


@router.post(
    "/backfill",
    response_model=IntentBackfillResponse
)
def backfill_intents(
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = IntentCategoryService(db)

    # Capped at 50: each call is a synchronous LLM round-trip (~1-2 s each).
    # 500 sequential calls would take ~10 min and risk Gemini quota exhaustion.
    return service.backfill_user_notes(
        user_id=current_user.id,
        limit=min(max(limit, 1), 50)
    )
