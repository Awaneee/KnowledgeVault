from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer

_model: "SentenceTransformer | None" = None


def get_embedding_model() -> "SentenceTransformer":
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


# Legacy alias — existing code that does `from app.core.embedding_model import embedding_model`
# will get a lazy proxy object. We replace usages below with get_embedding_model() calls.
# For backwards compat, provide a module-level name that doesn't load on import.
embedding_model = None  # will be set on first use via get_embedding_model()
