from datetime import date
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class NoteIntentResponse(BaseModel):
    id: int
    note_id: int
    intent_type: str
    action: Optional[str]
    actor: Optional[str]
    object: Optional[str]
    due_date: Optional[date]
    temporal_text: Optional[str]
    urgency: Optional[str]
    confidence: float
    model_name: str

    model_config = {"from_attributes": True}


class IntentCategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    intent_type: str
    actor: Optional[str]
    action: Optional[str]
    time_scope: Optional[str]
    confidence: float
    note_count: int
    last_used_at: Optional[datetime]

    model_config = {"from_attributes": True}


class IntentNoteResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    created_at: datetime

    model_config = {"from_attributes": True}


class IntentBackfillResponse(BaseModel):
    processed: int
    failed: int
    remaining_hint: int
