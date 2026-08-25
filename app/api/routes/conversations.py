from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.conversation import (
    ConversationAskRequest,
    ConversationAskResponse,
    ConversationSessionDetail,
    ConversationSessionOut,
)
from app.services.conversation_service import ConversationService

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/", response_model=ConversationSessionOut, status_code=status.HTTP_201_CREATED)
def create_session(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ConversationService(db)
    return service.create_session(user_id=current_user.id)


@router.get("/", response_model=list[ConversationSessionOut])
def list_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ConversationService(db)
    return service.list_sessions(user_id=current_user.id)


@router.get("/{session_id}", response_model=ConversationSessionDetail)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ConversationService(db)
    result = service.get_session(session_id=session_id, user_id=current_user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return result


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ConversationService(db)
    deleted = service.delete_session(session_id=session_id, user_id=current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Session not found")


@router.post("/{session_id}/ask", response_model=ConversationAskResponse)
def ask_in_session(
    session_id: int,
    data: ConversationAskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ConversationService(db)
    try:
        return service.ask(
            session_id=session_id,
            question=data.question,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
