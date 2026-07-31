"""
Ask service — retrieval-augmented question answering.

Retrieval (hybrid semantic + intent) runs first, unconditionally.
LLM answer generation runs second and has two outcomes:

  1. Success — synthesised answer returned with sources.
  2. All providers exhausted — retrieval-only response returned (no 500).

The retrieval-only response is a production-safe degradation: the user
still gets the most relevant notes, just without a synthesised sentence.

Caching
-------
Only the blocking ask() path is cached (stream_ask is not cacheable).
Cache key = SHA-256(user_id + normalised question).
TTL is configurable via ASK_CACHE_TTL_SECONDS in .env (default 3600).

Context construction
--------------------
- Chunks below RETRIEVAL_MIN_SCORE are dropped before prompt assembly.
- Duplicate content fingerprints are removed (keeps highest-scored copy).
- Context is truncated at MAX_CONTEXT_CHARS to stay within token budgets.
"""

import hashlib
import logging
import re
import time
from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.core.config import settings
from app.schemas.ask import Citation
from app.services.cache_service import CacheService
from app.services.chunk_service import ChunkService
from app.services.llm_metrics import metrics
from app.services.llm_service import AllProvidersExhausted
from app.services.llm_service import LLMService
from app.services.reranking_service import RerankingService


logger = logging.getLogger(__name__)

# Maximum total characters of context passed to the LLM.
# ~3 000 chars ≈ 750 tokens, leaving headroom for instructions + answer.
_MAX_CONTEXT_CHARS = 3_000

# Minimum content fingerprint length for dedup (very short chunks are kept as-is).
_MIN_DEDUP_LEN = 40


@dataclass(frozen=True)
class ContextEntry:
    """Bridges a context passage with its stable citation reference number."""
    ref: int                     # [N] as it appears in the prompt and answer
    note_id: int
    note_title: str
    chunk_id: int | None         # None for hybrid note-level arm
    chunk_index: int
    chunk_text: str              # full text used in the context string
    snippet: str                 # first 200 chars — for citation preview
    intent_category: str | None


class AskService:

    def __init__(self, db: Session) -> None:
        self.chunk_service = ChunkService(db)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ask(self, question: str, user_id: int) -> dict:
        """
        Blocking ask — retrieval + optional LLM synthesis.

        Returns a dict that is always safe to serialise:
          - On LLM success: {question, answer, sources, provider, retrieval_only: false}
          - On LLM failure: {question, answer (degraded), sources, retrieval_only: true}
        """
        cache_key = self._cache_key(user_id, question)
        cached = CacheService.get(cache_key)
        if cached:
            logger.info("ASK CACHE HIT user_id=%d question=%.60s", user_id, question)
            metrics.record_cache_hit()
            return cached

        metrics.record_cache_miss()
        t0 = time.monotonic()

        # --- Retrieval (always runs) ---
        pool_limit = settings.RERANK_CANDIDATE_POOL if settings.RERANKING_ENABLED else 8
        with metrics.track_retrieval():
            chunks = self.chunk_service.retrieve_hybrid(
                query=question,
                user_id=user_id,
                limit=pool_limit,
            )

        # --- Optional cross-encoder reranking ---
        rerank_result = RerankingService.rerank(
            query=question,
            candidates=chunks,
            top_k=settings.RERANK_TOP_K,
            user_id=user_id,
        )
        chunks = rerank_result.candidates
        reranked = rerank_result.reranked

        retrieval_elapsed = time.monotonic() - t0
        # Filter low-confidence chunks before synthesis.
        chunks = self._filter_chunks(chunks)

        logger.info(
            "ASK RETRIEVAL user_id=%d chunks=%d (after filter) reranked=%s elapsed=%.2fs sources=%s",
            user_id,
            len(chunks),
            reranked,
            retrieval_elapsed,
            [c["note_title"] for c in chunks[:5]],
        )

        sources = list(dict.fromkeys(c["note_title"] for c in chunks))

        # --- LLM synthesis (optional) ---
        t_llm = time.monotonic()
        result = self._synthesise(question=question, chunks=chunks, sources=sources)
        llm_elapsed = time.monotonic() - t_llm

        logger.info(
            "ASK COMPLETE user_id=%d provider=%s retrieval=%.2fs llm=%.2fs total=%.2fs",
            user_id,
            result.get("provider", "none"),
            retrieval_elapsed,
            llm_elapsed,
            time.monotonic() - t0,
        )

        result["reranked"] = reranked

        # Cache only when we have a real answer (avoid caching degraded responses).
        ttl = settings.ASK_CACHE_TTL_SECONDS
        if not result.get("retrieval_only") and ttl > 0:
            CacheService.set(cache_key, result, expire_seconds=ttl)

        return result

    def stream_ask(self, question: str, user_id: int):
        """
        Streaming ask — yields LLM tokens one by one.
        Retrieval runs up front; stream falls back to a plain-text
        degraded message if all providers fail.
        """
        t0 = time.monotonic()

        pool_limit = settings.RERANK_CANDIDATE_POOL if settings.RERANKING_ENABLED else 8
        with metrics.track_retrieval():
            chunks = self.chunk_service.retrieve_hybrid(
                query=question,
                user_id=user_id,
                limit=pool_limit,
            )
        rerank_result = RerankingService.rerank(
            query=question,
            candidates=chunks,
            top_k=settings.RERANK_TOP_K,
            user_id=user_id,
        )
        chunks = rerank_result.candidates
        chunks = self._filter_chunks(chunks)

        logger.info(
            "STREAM RETRIEVAL user_id=%d chunks=%d reranked=%s elapsed=%.2fs",
            user_id,
            len(chunks),
            rerank_result.reranked,
            time.monotonic() - t0,
        )

        # Citations are not parsed in the streaming path (Sprint 4-C).
        # _build_context_map is still called so the prompt format is consistent
        # with the blocking ask() path.
        context, _context_map = self._build_context_map(chunks)
        prompt = self._build_prompt(question, context)

        try:
            yield from LLMService.generate_stream(prompt=prompt)
        except AllProvidersExhausted:
            logger.warning(
                "STREAM DEGRADED user_id=%d — all providers failed, returning retrieval-only",
                user_id,
            )
            yield self._degraded_message(sources=[c["note_title"] for c in chunks])

    # ------------------------------------------------------------------
    # Synthesis helpers
    # ------------------------------------------------------------------

    def _synthesise(
        self,
        question: str,
        chunks: list[dict],
        sources: list[str],
    ) -> dict:
        """
        Attempt LLM synthesis. On failure, return a retrieval-only response.
        Never raises — errors are logged and a safe dict is always returned.
        """
        if not chunks:
            return {
                "question": question,
                "answer": "No relevant notes were found for your question.",
                "sources": [],
                "citations": [],
                "retrieval_only": False,
                "status": "no_results",
            }

        context, context_map = self._build_context_map(chunks)
        prompt = self._build_prompt(question, context)

        try:
            raw_answer = LLMService.generate(prompt=prompt)
            raw_answer = self._validate_answer(raw_answer, chunks)
        except AllProvidersExhausted as exc:
            logger.warning(
                "ASK ALL PROVIDERS EXHAUSTED — returning retrieval-only response. errors=%s",
                exc,
            )
            return self._retrieval_only_response(question=question, chunks=chunks, sources=sources)
        except Exception as exc:
            logger.exception("ASK unexpected LLM error: %s", exc)
            return self._retrieval_only_response(question=question, chunks=chunks, sources=sources)

        try:
            answer, citations = self._parse_citations(raw_answer, context_map)
            if not citations:
                logger.info("ASK no citations found in answer (graceful degradation)")
            citation_dicts = [c.model_dump() for c in citations]
        except Exception as exc:
            logger.error("ASK citation parse failed — returning uncited answer: %s", exc)
            answer = raw_answer
            citation_dicts = []

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "citations": citation_dicts,
            "retrieval_only": False,
            "status": "ok",
            "provider": "llm",
        }

    def _retrieval_only_response(
        self,
        question: str,
        chunks: list[dict],
        sources: list[str],
    ) -> dict:
        return {
            "question": question,
            "answer": (
                "AI-generated responses are temporarily unavailable. "
                "Here are the most relevant notes we found for your question."
            ),
            "sources": sources,
            "retrieval_only": True,
            "status": "degraded",
            "chunks": [
                {
                    "title": c["note_title"],
                    "preview": c["chunk_text"][:300],
                    "score": round(c.get("score", 0.0), 3),
                    "category": c.get("intent_category"),
                }
                for c in chunks[:5]
            ],
        }

    @staticmethod
    def _degraded_message(sources: list[str]) -> str:
        if sources:
            return (
                "AI-generated responses are temporarily unavailable. "
                f"Relevant notes found: {', '.join(sources[:5])}."
            )
        return "AI-generated responses are temporarily unavailable. No relevant notes were found."

    # ------------------------------------------------------------------
    # Prompt construction
    # ------------------------------------------------------------------

    def _build_prompt(self, question: str, context: str) -> str:
        return f"""\
You are a retrieval assistant helping a user search their personal knowledge notes.

<context>
{context}
</context>

<question>
{question}
</question>

Instructions:
- Read all retrieved context carefully.
- Write a clear, complete answer of 2–5 sentences.
- Synthesise information from multiple notes when relevant.
- Cite the source of every factual claim using its bracket number, e.g. [1] or [2].
- Only use bracket numbers that appear in the context above. Never invent numbers.
- If you cite the same source twice, write [1]...[1] — that is correct.
- Multiple sources per sentence are allowed: "X is true [1] and Y is also true [2]."
- Never respond with a single keyword or phrase alone.
- Do not invent or infer information that is not present in the context.
- Do not explain your reasoning; just answer.
- If the context does not contain enough information, say exactly:
  "I could not find that information in your notes."

Answer:
"""

    @staticmethod
    def _build_context_map(chunks: list[dict]) -> tuple[str, list[ContextEntry]]:
        """
        Build a deduplicated, token-budget-aware context string with stable
        reference numbers ([1], [2], ...) and the mapping that lets
        _parse_citations() resolve those numbers back to note/chunk IDs.

        Returns:
            (context_str, context_map) where context_map[i].ref == i + 1.
            Only entries whose text actually made it into context_str are
            included in context_map — so citation validation is accurate.
        """
        seen_fingerprints: set[str] = set()
        pending: list[ContextEntry] = []

        for chunk in chunks:
            text = chunk["chunk_text"]
            fp = " ".join(text.lower().split())[:80] if len(text) >= _MIN_DEDUP_LEN else None
            if fp and fp in seen_fingerprints:
                continue
            if fp:
                seen_fingerprints.add(fp)
            ref = len(pending) + 1
            pending.append(ContextEntry(
                ref=ref,
                note_id=chunk["note_id"],
                note_title=chunk["note_title"],
                chunk_id=chunk.get("chunk_id"),
                chunk_index=chunk["chunk_index"],
                chunk_text=text,
                snippet=text[:200],
                intent_category=chunk.get("intent_category"),
            ))

        # Token-budget guard — track only entries that fit.
        parts: list[str] = []
        included: list[ContextEntry] = []
        total_chars = 0

        for entry in pending:
            category = entry.intent_category or "Semantic match"
            entry_str = (
                f"[{entry.ref}] {category} | {entry.note_title}\n"
                f"{entry.chunk_text}"
            )
            if total_chars + len(entry_str) > _MAX_CONTEXT_CHARS:
                remaining = _MAX_CONTEXT_CHARS - total_chars
                if remaining > 100:
                    parts.append(entry_str[:remaining] + "…")
                    included.append(entry)
                break
            parts.append(entry_str)
            included.append(entry)
            total_chars += len(entry_str)

        return "\n\n".join(parts), included

    @staticmethod
    def _parse_citations(
        answer: str,
        context_map: list[ContextEntry],
    ) -> tuple[str, list[Citation]]:
        """
        Extract [N] citation markers from the LLM answer.

        Valid markers (1 ≤ N ≤ len(context_map)) are kept in the answer text
        and resolved to Citation objects.  Invalid markers (hallucinated numbers
        outside the valid range) are removed from the answer and logged.

        Returns:
            (cleaned_answer, citations) where citations contains one entry per
            unique ref, ordered by first appearance in the answer.
        """
        if not context_map:
            return answer, []

        valid_refs: set[int] = {entry.ref for entry in context_map}
        entry_by_ref: dict[int, ContextEntry] = {entry.ref: entry for entry in context_map}
        found_refs: list[int] = []  # insertion-ordered, deduplicated

        def _replace(match: re.Match) -> str:
            try:
                n = int(match.group(1))
            except ValueError:
                return match.group(0)  # leave unchanged if not parseable
            if n not in valid_refs:
                logger.warning(
                    "CITATION hallucinated ref=[%d] (valid: %s) — removing from answer",
                    n,
                    sorted(valid_refs),
                )
                return ""
            if n not in found_refs:
                found_refs.append(n)
            return f"[{n}]"

        cleaned = re.sub(r"\[(\d+)\]", _replace, answer)
        # Collapse whitespace artifacts left by removed markers.
        cleaned = re.sub(r" {2,}", " ", cleaned).strip()

        citations = [
            Citation(
                ref=n,
                note_id=entry_by_ref[n].note_id,
                note_title=entry_by_ref[n].note_title,
                chunk_id=entry_by_ref[n].chunk_id,
                snippet=entry_by_ref[n].snippet,
            )
            for n in found_refs
        ]

        return cleaned, citations

    @staticmethod
    def _validate_answer(answer: str, chunks: list[dict]) -> str:
        """
        Reject single-word or single-phrase answers that look like keyword leakage.
        If the answer is suspiciously short, replace it with a note-not-found message.
        """
        stripped = answer.strip()
        # A real answer should have at least one space (i.e. multiple words)
        # and be at least 20 characters long.
        if len(stripped) < 20 or " " not in stripped:
            logger.warning(
                "ASK answer appears to be a bare keyword (%r) — substituting fallback",
                stripped[:60],
            )
            return "I could not find a complete answer in your notes. Please refine your question."
        return stripped

    # ------------------------------------------------------------------
    # Chunk filtering
    # ------------------------------------------------------------------

    @staticmethod
    def _filter_chunks(chunks: list[dict]) -> list[dict]:
        """Drop chunks below the minimum retrieval score."""
        min_score = settings.RETRIEVAL_MIN_SCORE
        filtered = [c for c in chunks if c.get("score", 0.0) >= min_score]
        if len(filtered) < len(chunks):
            logger.debug(
                "ASK chunk filter: %d → %d (min_score=%.2f)",
                len(chunks),
                len(filtered),
                min_score,
            )
        return filtered

    # ------------------------------------------------------------------
    # Cache key
    # ------------------------------------------------------------------

    @staticmethod
    def _cache_key(user_id: int, question: str) -> str:
        # Key includes: user, normalised question, provider priority (so a
        # provider change naturally busts the cache).
        provider_sig = settings.LLM_PROVIDER_PRIORITY or settings.LLM_PROVIDER
        normalised = question.strip().lower()
        digest = hashlib.sha256(
            f"{user_id}:{normalised}:{provider_sig}".encode()
        ).hexdigest()
        return f"ask:{user_id}:{digest}"

    # ------------------------------------------------------------------
    # Internal evaluation API — DO NOT CALL FROM PRODUCTION PATHS
    # ------------------------------------------------------------------

    def ask_with_context(self, question: str, user_id: int) -> dict:
        """
        Internal method used exclusively by the evaluation runner.

        Returns the standard ask() result PLUS a '_eval' key containing
        all artifacts needed for deterministic debugging:
          - retrieved_chunks: full list of chunk dicts (with scores)
          - filtered_chunks: chunks after score filtering
          - prompt: the exact prompt sent to the LLM
          - retrieval_ms: wall-clock time for hybrid retrieval
          - llm_ms: wall-clock time for LLM generation
          - total_ms: end-to-end wall-clock time

        This method does NOT read from or write to the cache so that
        every evaluation call exercises the live pipeline.
        """
        t_start = time.monotonic()

        # Retrieval — no cache
        t_ret = time.monotonic()
        pool_limit = settings.RERANK_CANDIDATE_POOL if settings.RERANKING_ENABLED else 8
        raw_chunks = self.chunk_service.retrieve_hybrid(
            query=question,
            user_id=user_id,
            limit=pool_limit,
        )
        rerank_result = RerankingService.rerank(
            query=question,
            candidates=raw_chunks,
            top_k=settings.RERANK_TOP_K,
            user_id=user_id,
        )
        reranked_chunks = rerank_result.candidates
        retrieval_ms = (time.monotonic() - t_ret) * 1000.0

        filtered_chunks = self._filter_chunks(reranked_chunks)
        context, context_map = self._build_context_map(filtered_chunks)
        prompt = self._build_prompt(question, context)

        # LLM synthesis
        t_llm = time.monotonic()
        sources = list(dict.fromkeys(c["note_title"] for c in filtered_chunks))
        result = self._synthesise(
            question=question,
            chunks=filtered_chunks,
            sources=sources,
        )
        llm_ms = (time.monotonic() - t_llm) * 1000.0
        total_ms = (time.monotonic() - t_start) * 1000.0

        result["reranked"] = rerank_result.reranked
        result["_eval"] = {
            "retrieved_chunks": raw_chunks,
            "reranked": rerank_result.reranked,
            "filtered_chunks": filtered_chunks,
            "context_map": [
                {
                    "ref": e.ref,
                    "note_id": e.note_id,
                    "note_title": e.note_title,
                    "chunk_id": e.chunk_id,
                    "chunk_index": e.chunk_index,
                    "snippet": e.snippet,
                    "intent_category": e.intent_category,
                }
                for e in context_map
            ],
            "prompt": prompt,
            "retrieval_ms": round(retrieval_ms, 2),
            "llm_ms": round(llm_ms, 2),
            "total_ms": round(total_ms, 2),
        }
        return result