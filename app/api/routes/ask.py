from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.ask import (
    AskRequest,
    AskResponse
)

from app.services.ask_service import AskService


router = APIRouter(
    prefix="/ask",
    tags=["ask"]
)


@router.post(
    "/",
    response_model=AskResponse
)
def ask_question(
    data: AskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    service = AskService(db)

    return service.ask(
        question=data.question,
        user_id=current_user.id
    )