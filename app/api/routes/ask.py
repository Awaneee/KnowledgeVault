from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import StreamingResponse
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


@router.post("/stream")
def ask_question_stream(
    data: AskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    """
    Same retrieval+generation as POST /ask/, but streams the answer
    token-by-token as it's generated instead of waiting ~50s+ for the
    full response. Sources aren't included in this response since a
    plain text/event-stream body can't carry structured data
    alongside the token stream - if the client needs sources too,
    call POST /ask/ instead, or have the client track which notes
    were already shown via a separate call to /retrieve/hybrid.
    """
    service = AskService(db)

    return StreamingResponse(
        service.stream_ask(
            question=data.question,
            user_id=current_user.id
        ),
        media_type="text/event-stream"
    )