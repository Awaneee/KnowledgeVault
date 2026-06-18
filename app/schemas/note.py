from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.intent import IntentCategoryResponse
from app.schemas.intent import NoteIntentResponse


class NoteCreate(BaseModel):
    content: str


class NoteResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    user_id: int
    category_id: Optional[int]
    auto_title_source: Optional[str] = None
    organization_status: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class NoteCreateResponse(NoteResponse):
    intent: Optional[NoteIntentResponse] = None
    intent_category: Optional[IntentCategoryResponse] = None


class NoteSearchResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]

    model_config = {"from_attributes": True}
