import json
import logging

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


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/ask",
    tags=["ask"]
)


def _sse_frame(payload: str, event: str | None = None) -> str:
    """
    Build a single SSE frame.

    The payload is JSON-encoded so that a token's own newlines and leading
    spaces survive the transport - SSE is a line-oriented protocol, so a raw
    token containing "\n" would otherwise be split across frames (or silently
    reassembled without its whitespace by the client).
    """
    prefix = f"event: {event}\n" if event else ""
    return f"{prefix}data: {payload}\n\n"


def _sse_stream(tokens):
    """Wrap a token generator in SSE frames, always terminating with [DONE]."""
    try:
        for token in tokens:
            if token:
                yield _sse_frame(json.dumps(token, ensure_ascii=False))
    except Exception as exc:
        logger.exception("STREAM failed mid-generation: %s", exc)
        yield _sse_frame(
            json.dumps("The answer stream was interrupted. Please try again."),
            event="error",
        )
    finally:
        yield _sse_frame("[DONE]")


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

    Wire format is Server-Sent Events. Each frame carries one
    JSON-encoded string token:

        data: "Based"
        data: " on your notes"
        data: ":\n\n1. "
        data: [DONE]
    """
    service = AskService(db)

    return StreamingResponse(
        _sse_stream(
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
