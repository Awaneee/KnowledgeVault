from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.conversation import AgentAskRequest, AgentAskResponse
from app.services.agent_service import AgentService

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/ask", response_model=AgentAskResponse)
def agent_ask(
    data: AgentAskRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Agentic RAG endpoint.

    The agent autonomously decides which tools to use (search_notes,
    filter_by_category, get_note_content, list_categories) and chains
    multiple retrieval steps before synthesising a grounded answer.

    Optionally pass `session_id` to run within an existing conversation
    session — the agent will read prior turns as context and persist
    the new turn to the session history.
    """
    service = AgentService(db)
    return service.ask(
        question=data.question,
        user_id=current_user.id,
        session_id=data.session_id,
    )
