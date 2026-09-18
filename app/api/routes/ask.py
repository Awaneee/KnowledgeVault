import logging

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.api.dependencies.auth import get_current_user
from app.models.user import User

from app.schemas.ask import (
    AskRequest,
    AskResponse
)

from app.api.sse import sse_stream
from app.core.config import settings
from app.core.limiter import limiter, user_or_ip_key
from app.services.ask_service import AskService


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ask",
    tags=["ask"]
)


@router.post(
    "/",
    response_model=AskResponse
)
@limiter.shared_limit(settings.ASK_RATE_LIMIT, scope="ask", key_func=user_or_ip_key)
def ask_question(
    request: Request,
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
@limiter.shared_limit(settings.ASK_RATE_LIMIT, scope="ask", key_func=user_or_ip_key)
def ask_question_stream(
    request: Request,
    data: AskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    """
    Same retrieval+generation as POST /ask/, but streams the answer
    token-by-token as it's generated instead of waiting ~50s+ for the
    full response.

    Wire format is Server-Sent Events. Each frame carries one
    JSON-encoded string token:

        data: "Based"
        data: " on your notes"
        data: ":\n\n1. [1]"

    After the last token, if the answer cited any notes, one
    `citations` frame carries the resolved citation objects (same shape
    as `citations` in POST /ask/), then the stream ends:

        event: citations
        data: [{"ref": 1, "note_id": 7, "note_title": "...", "chunk_id": null, "snippet": "..."}]

        data: [DONE]

    Tokens are already on the wire when citations are resolved, so
    unlike POST /ask/ an out-of-range [N] marker cannot be removed from
    the text; clients should only link refs that appear in `citations`.
    """
    service = AskService(db)

    return StreamingResponse(
        sse_stream(
            service.stream_ask(
                question=data.question,
                user_id=current_user.id
            )
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            # Tell nginx-style proxies not to buffer the response, which
            # would otherwise defeat streaming entirely.
            "X-Accel-Buffering": "no",
        },
    )
