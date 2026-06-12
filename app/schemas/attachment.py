from pydantic import BaseModel
from datetime import datetime


class AttachmentCreate(BaseModel):
    filename: str
    file_path: str
    file_type: str
    note_id: int


class AttachmentResponse(BaseModel):
    id: int
    filename: str
    file_path: str
    file_type: str
    note_id: int
    created_at: datetime

    model_config = {"from_attributes": True}