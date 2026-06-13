from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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


class NoteSearchResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]

    model_config = {"from_attributes": True}