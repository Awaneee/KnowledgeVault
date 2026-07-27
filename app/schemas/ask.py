from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class ChunkPreview(BaseModel):
    title: str
    preview: str
    score: float
    category: str | None = None


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]
    retrieval_only: bool = False
    status: str = "ok"
    provider: str | None = None
    # Populated only when retrieval_only=True.
    chunks: list[ChunkPreview] = []