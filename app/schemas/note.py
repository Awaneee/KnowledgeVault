from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NoteCreate(BaseModel):
    title: str
    content: Optional[str] = None
    category_id: Optional[int] = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    user_id: int
    category_id: Optional[int]
    created_at: datetime

    model_config = {"from_attributes": True}