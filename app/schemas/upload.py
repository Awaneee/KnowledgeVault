from pydantic import BaseModel


class PDFUploadResponse(BaseModel):
    message: str
    note_id: int