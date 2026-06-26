"""
Base adapter interface.

Every adapter wraps exactly one production retrieval path and translates
its output into a RetrievalResult.  No retrieval logic is implemented here.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.evaluation.models import BenchmarkQuery, RetrievalResult, RetrievalStrategy


class BaseRetrievalAdapter(ABC):
    """
    Contract that all concrete adapters must satisfy.

    The constructor receives a SQLAlchemy Session so the adapter can
    instantiate production services exactly as FastAPI route handlers do
    (via Depends(get_db)).  The session is never used for evaluation
    data storage — it exists solely to satisfy the production service
    constructors.
    """

    strategy: RetrievalStrategy  # must be set by each subclass

    def __init__(self, db: Session) -> None:
        self.db = db

    def run(self, benchmark_query: BenchmarkQuery) -> RetrievalResult:
        """
        Execute the retrieval, measure wall-clock time, return a
        RetrievalResult.  Exceptions are caught and stored in .error so
        that a single failing query does not abort the whole evaluation run.
        """
        start = time.perf_counter()
        try:
            result = self._retrieve(benchmark_query)
        except Exception as exc:  # noqa: BLE001
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            return RetrievalResult(
                strategy=self.strategy,
                query=benchmark_query.query,
                latency_ms=elapsed_ms,
                error=str(exc),
            )

        elapsed_ms = (time.perf_counter() - start) * 1000.0
        result.latency_ms = elapsed_ms
        return result

    @abstractmethod
    def _retrieve(self, benchmark_query: BenchmarkQuery) -> RetrievalResult:
        """
        Subclasses implement this method.

        Must call the production service and convert its output into a
        RetrievalResult.  Must NOT set latency_ms — the base class
        measures wall-clock time around the call.
        """
