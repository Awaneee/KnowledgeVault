from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.services.chunk_service import ChunkService


router = APIRouter(
    prefix="/retrieve",
    tags=["retrieval"]
)


# ── Request / Response schemas (local; move to app/schemas/ if desired) ──

class RetrieveRequest(BaseModel):
    query: str


class ChunkResult(BaseModel):
    chunk_text: str
    note_title: str
    source: str | None = None
    intent_category: str | None = None

    model_config = {"from_attributes": True}


# ── Endpoint ──

@router.post(
    "",
    response_model=list[ChunkResult]
)
def retrieve_chunks(
    body: RetrieveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Semantic chunk retrieval.

    Accepts a natural-language query, embeds it, and returns
    the top-5 most relevant document chunks from the current
    user's notes.  No LLM answering is performed here.
    """
    chunk_service = ChunkService(db)

    results = chunk_service.retrieve(
        query=body.query,
        user_id=current_user.id,
        limit=5
    )

    return [
        ChunkResult(
            chunk_text=r["chunk_text"],
            note_title=r["note_title"]
        )
        for r in results
    ]


@router.post(
    "/hybrid",
    response_model=list[ChunkResult]
)
def retrieve_hybrid_chunks(
    body: RetrieveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Intent-aware chunk retrieval.

    Useful for queries like "what should I tell Sid?" where
    purpose matters more than topic similarity.
    """
    chunk_service = ChunkService(db)

    results = chunk_service.retrieve_hybrid(
        query=body.query,
        user_id=current_user.id,
        limit=5
    )

    return [
        ChunkResult(
            chunk_text=r["chunk_text"],
            note_title=r["note_title"],
            source=r.get("source"),
            intent_category=r.get("intent_category")
        )
        for r in results
    ]
