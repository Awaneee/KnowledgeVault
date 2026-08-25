from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ConversationMessageOut(BaseModel):
    id: int
    role: str
    content: str
    citations: list[Any] | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationSessionOut(BaseModel):
    id: int
    title: str | None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    model_config = {"from_attributes": True}


class ConversationSessionDetail(ConversationSessionOut):
    messages: list[ConversationMessageOut] = []


class ConversationAskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)


class ConversationAskResponse(BaseModel):
    session_id: int
    question: str
    answer: str
    sources: list[str] = []
    citations: list[Any] = []
    retrieval_only: bool = False
    reranked: bool = False
    provider: str | None = None
    status: str = "ok"


class AgentAskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    session_id: int | None = None


class AgentAskResponse(BaseModel):
    session_id: int
    question: str
    answer: str
    sources: list[str] = []
    citations: list[Any] = []
    tools_used: list[str] = []
    iterations: int = 0
    status: str = "ok"
