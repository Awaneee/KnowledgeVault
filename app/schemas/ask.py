from __future__ import annotations

from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class Citation(BaseModel):
    """A single inline citation reference resolved from the answer text."""
    ref: int            # The [N] number as it appears in the answer
    note_id: int        # Database ID of the source note — for navigation
    note_title: str     # Display title of the source note
    chunk_id: int | None = None  # DocumentChunk.id; None for note-level hybrid arm
    snippet: str        # First 200 chars of the cited passage for hover preview


class ChunkPreview(BaseModel):
    title: str
    preview: str
    score: float
    category: str | None = None


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]           # Kept unchanged for backward compatibility
    citations: list[Citation] = []  # Inline citation references; empty when none found
    retrieval_only: bool = False
    status: str = "ok"
    provider: str | None = None
    # Populated only when retrieval_only=True.
    chunks: list[ChunkPreview] = []