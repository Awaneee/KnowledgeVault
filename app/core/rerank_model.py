"""
Cross-encoder reranking model singleton.

Loaded once at module import when RERANKING_ENABLED=True.
Exposed as the module-level ``rerank_model`` variable, which is ``None``
when reranking is disabled or the model fails to load.  All callers must
treat ``None`` as "reranking unavailable" and fall back to the original
retrieval ordering.
"""

import logging

logger = logging.getLogger(__name__)

# Imported lazily to avoid resolving settings at import-graph construction time
# (circular-import guard).
from app.core.config import settings  # noqa: E402

rerank_model = None  # type: ignore[assignment]

if settings.RERANKING_ENABLED:
    try:
        from sentence_transformers import CrossEncoder  # type: ignore[import]

        logger.info("Loading reranking model: %s", settings.RERANK_MODEL)
        rerank_model = CrossEncoder(settings.RERANK_MODEL)
        logger.info("Reranking model loaded successfully")
    except Exception as exc:
        logger.error(
            "Failed to load reranking model %r — reranking disabled: %s",
            settings.RERANK_MODEL,
            exc,
        )
        rerank_model = None
