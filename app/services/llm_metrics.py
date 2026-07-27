"""
LLM Metrics — thread-safe per-provider counters and latency tracking.

Usage::

    from app.services.llm_metrics import metrics

    with metrics.track("gemini", "answer"):
        result = provider.generate_answer(prompt)

    snapshot = metrics.snapshot()   # returns JSON-serialisable dict
"""

import threading
import time
from collections import defaultdict
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Generator


@dataclass
class _ProviderStats:
    attempts: int = 0
    successes: int = 0
    failures: int = 0
    total_latency_ms: float = 0.0
    fallback_count: int = 0


class LLMMetrics:
    """Thread-safe metrics store for LLM provider telemetry."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # provider → operation → stats
        self._stats: dict[str, dict[str, _ProviderStats]] = defaultdict(
            lambda: defaultdict(_ProviderStats)
        )
        self._cache_hits = 0
        self._cache_misses = 0
        self._retrieval_latency_ms_total = 0.0
        self._retrieval_calls = 0
        self._fallback_transitions: list[str] = []

    # ------------------------------------------------------------------
    # Context-manager helpers
    # ------------------------------------------------------------------

    @contextmanager
    def track(self, provider: str, operation: str) -> Generator[None, None, None]:
        """
        Time a single LLM call and record success / failure.

        Example::

            with metrics.track("gemini", "answer"):
                result = gemini.generate_answer(prompt)
        """
        start = time.monotonic()
        cell = self._get_cell(provider, operation)
        with self._lock:
            cell.attempts += 1
        try:
            yield
        except Exception:
            elapsed_ms = (time.monotonic() - start) * 1000
            with self._lock:
                cell.failures += 1
                cell.total_latency_ms += elapsed_ms
            raise
        else:
            elapsed_ms = (time.monotonic() - start) * 1000
            with self._lock:
                cell.successes += 1
                cell.total_latency_ms += elapsed_ms

    @contextmanager
    def track_retrieval(self) -> Generator[None, None, None]:
        start = time.monotonic()
        try:
            yield
        finally:
            elapsed_ms = (time.monotonic() - start) * 1000
            with self._lock:
                self._retrieval_latency_ms_total += elapsed_ms
                self._retrieval_calls += 1

    # ------------------------------------------------------------------
    # Manual recording helpers
    # ------------------------------------------------------------------

    def record_fallback(self, from_provider: str, to_provider: str, reason: str) -> None:
        with self._lock:
            self._stats[from_provider]["answer"].fallback_count += 1
            self._fallback_transitions.append(
                f"{from_provider}→{to_provider} ({reason})"
            )
            # Keep last 100 transitions to bound memory.
            if len(self._fallback_transitions) > 100:
                self._fallback_transitions = self._fallback_transitions[-100:]

    def record_cache_hit(self) -> None:
        with self._lock:
            self._cache_hits += 1

    def record_cache_miss(self) -> None:
        with self._lock:
            self._cache_misses += 1

    # ------------------------------------------------------------------
    # Snapshot
    # ------------------------------------------------------------------

    def snapshot(self) -> dict:
        """Return a JSON-serialisable metrics snapshot."""
        with self._lock:
            providers: dict = {}
            for provider, ops in self._stats.items():
                providers[provider] = {}
                for op, s in ops.items():
                    avg_ms = (
                        s.total_latency_ms / s.attempts if s.attempts else 0.0
                    )
                    providers[provider][op] = {
                        "attempts": s.attempts,
                        "successes": s.successes,
                        "failures": s.failures,
                        "avg_latency_ms": round(avg_ms, 1),
                        "fallback_count": s.fallback_count,
                    }

            avg_retrieval_ms = (
                self._retrieval_latency_ms_total / self._retrieval_calls
                if self._retrieval_calls
                else 0.0
            )

            return {
                "providers": providers,
                "cache": {
                    "hits": self._cache_hits,
                    "misses": self._cache_misses,
                    "hit_rate": round(
                        self._cache_hits
                        / max(1, self._cache_hits + self._cache_misses),
                        3,
                    ),
                },
                "retrieval": {
                    "calls": self._retrieval_calls,
                    "avg_latency_ms": round(avg_retrieval_ms, 1),
                },
                "recent_fallbacks": list(self._fallback_transitions[-20:]),
            }

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _get_cell(self, provider: str, operation: str) -> _ProviderStats:
        # Not locked here; caller locks around the result.
        return self._stats[provider][operation]


# Module-level singleton — import this everywhere.
metrics = LLMMetrics()
