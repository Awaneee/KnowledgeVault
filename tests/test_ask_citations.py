"""
Sprint 2-A — Source-Cited Answers tests.

All tests are pure Python: no database, no network, no LLM call.
Covers:
  - ContextEntry dataclass
  - AskService._build_context_map()
  - AskService._parse_citations()
  - Citation schema
  - AskResponse schema (backward-compat + new citations field)
  - ChunkService retrieval dict keys (chunk_id propagation)
  - AskService._synthesise() via mocked LLMService
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.schemas.ask import AskResponse, Citation
from app.services.ask_service import AskService, ContextEntry, _MAX_CONTEXT_CHARS


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _chunk(
    note_id: int = 1,
    note_title: str = "Test Note",
    chunk_text: str = "Some chunk text about PostgreSQL indexing.",
    chunk_id: int | None = 10,
    chunk_index: int = 0,
    score: float = 0.85,
    intent_category: str | None = "Study - PostgreSQL",
) -> dict:
    return {
        "note_id": note_id,
        "note_title": note_title,
        "chunk_id": chunk_id,
        "chunk_text": chunk_text,
        "chunk_index": chunk_index,
        "score": score,
        "semantic_score": score,
        "intent_score": 0.0,
        "source": "semantic",
        "intent_category": intent_category,
    }


def _map_of(n: int) -> list[ContextEntry]:
    """Build a context_map with n entries for testing _parse_citations."""
    return [
        ContextEntry(
            ref=i,
            note_id=100 + i,
            note_title=f"Note {i}",
            chunk_id=200 + i,
            chunk_index=0,
            chunk_text=f"Text for note {i}.",
            snippet=f"Text for note {i}.",
            intent_category=None,
        )
        for i in range(1, n + 1)
    ]


# ===========================================================================
# ContextEntry
# ===========================================================================

class TestContextEntry:
    def test_is_frozen(self):
        entry = ContextEntry(
            ref=1, note_id=1, note_title="N", chunk_id=5,
            chunk_index=0, chunk_text="text", snippet="text", intent_category=None,
        )
        with pytest.raises((TypeError, AttributeError)):
            entry.ref = 99  # type: ignore[misc]

    def test_fields_accessible(self):
        entry = ContextEntry(
            ref=2, note_id=42, note_title="My Note", chunk_id=None,
            chunk_index=1, chunk_text="full text", snippet="full", intent_category="Study",
        )
        assert entry.ref == 2
        assert entry.note_id == 42
        assert entry.chunk_id is None


# ===========================================================================
# _build_context_map
# ===========================================================================

class TestBuildContextMap:
    def test_empty_chunks_returns_empty(self):
        ctx, cmap = AskService._build_context_map([])
        assert ctx == ""
        assert cmap == []

    def test_ref_numbering_is_sequential_from_one(self):
        # Use distinct texts to avoid 80-char fingerprint dedup collapsing them.
        chunks = [
            _chunk(note_id=1, chunk_id=10, chunk_text="B-tree indexes are the PostgreSQL default. " * 3),
            _chunk(note_id=2, chunk_id=20, chunk_text="HNSW builds a layered graph for ANN search. " * 3),
            _chunk(note_id=3, chunk_id=30, chunk_text="GIN indexes are designed for full-text search. " * 3),
        ]
        _, cmap = AskService._build_context_map(chunks)
        assert [e.ref for e in cmap] == [1, 2, 3]

    def test_context_string_contains_bracket_N(self):
        chunks = [
            _chunk(note_id=1, chunk_id=10, chunk_text="B-tree indexes are the PostgreSQL default. " * 3),
            _chunk(note_id=2, chunk_id=20, chunk_text="HNSW builds a layered graph for ANN search. " * 3),
        ]
        ctx, _ = AskService._build_context_map(chunks)
        assert "[1]" in ctx
        assert "[2]" in ctx

    def test_chunk_id_propagated(self):
        _, cmap = AskService._build_context_map([_chunk(chunk_id=99)])
        assert cmap[0].chunk_id == 99

    def test_chunk_id_none_when_missing(self):
        c = _chunk()
        del c["chunk_id"]
        _, cmap = AskService._build_context_map([c])
        assert cmap[0].chunk_id is None

    def test_dedup_fingerprint_skips_near_duplicate(self):
        text = "A" * 200
        c1 = _chunk(note_id=1, chunk_text=text, chunk_id=10)
        c2 = _chunk(note_id=2, chunk_text=text, chunk_id=20)  # same fingerprint
        _, cmap = AskService._build_context_map([c1, c2])
        assert len(cmap) == 1
        assert cmap[0].note_id == 1  # first one kept

    def test_short_chunks_bypass_fingerprint_dedup(self):
        # chunks shorter than _MIN_DEDUP_LEN are always kept
        c1 = _chunk(note_id=1, chunk_text="Short.")
        c2 = _chunk(note_id=2, chunk_text="Short.")
        _, cmap = AskService._build_context_map([c1, c2])
        assert len(cmap) == 2

    def test_snippet_is_first_200_chars(self):
        text = "X" * 300
        _, cmap = AskService._build_context_map([_chunk(chunk_text=text)])
        assert cmap[0].snippet == "X" * 200

    def test_budget_limits_context_map(self):
        # Each chunk is ~600 chars; at 3000-char budget only ~5 fit
        long_text = "W" * 580
        chunks = [_chunk(note_id=i, chunk_id=i, chunk_text=long_text) for i in range(10)]
        ctx, cmap = AskService._build_context_map(chunks)
        assert len(cmap) < 10
        assert len(ctx) <= _MAX_CONTEXT_CHARS + 50  # small headroom for "…"

    def test_context_map_only_includes_entries_in_context_string(self):
        # All entries in cmap must have their [N] appear in the context string
        chunks = [_chunk(note_id=i, chunk_id=i) for i in range(5)]
        ctx, cmap = AskService._build_context_map(chunks)
        for entry in cmap:
            assert f"[{entry.ref}]" in ctx

    def test_intent_category_used_in_context_string(self):
        ctx, _ = AskService._build_context_map([_chunk(intent_category="Study - Docker")])
        assert "Study - Docker" in ctx

    def test_null_intent_category_uses_semantic_match(self):
        ctx, _ = AskService._build_context_map([_chunk(intent_category=None)])
        assert "Semantic match" in ctx

    def test_note_title_in_context_string(self):
        ctx, _ = AskService._build_context_map([_chunk(note_title="My PostgreSQL Notes")])
        assert "My PostgreSQL Notes" in ctx


# ===========================================================================
# _parse_citations
# ===========================================================================

class TestParseCitations:
    def test_empty_context_map_returns_unchanged(self):
        cleaned, cits = AskService._parse_citations("Answer [1].", [])
        assert cleaned == "Answer [1]."
        assert cits == []

    def test_valid_citation_kept(self):
        cmap = _map_of(2)
        cleaned, cits = AskService._parse_citations("B-tree is default [1].", cmap)
        assert "[1]" in cleaned
        assert len(cits) == 1
        assert cits[0].ref == 1
        assert cits[0].note_id == 101

    def test_multiple_valid_citations(self):
        cmap = _map_of(3)
        cleaned, cits = AskService._parse_citations("X [1] and Y [2] and Z [3].", cmap)
        assert len(cits) == 3
        assert [c.ref for c in cits] == [1, 2, 3]

    def test_hallucinated_ref_removed(self):
        cmap = _map_of(2)
        cleaned, cits = AskService._parse_citations("X [5] is false.", cmap)
        assert "[5]" not in cleaned
        assert cits == []

    def test_ref_zero_removed(self):
        cmap = _map_of(2)
        cleaned, cits = AskService._parse_citations("X [0].", cmap)
        assert "[0]" not in cleaned

    def test_mixed_valid_and_hallucinated(self):
        cmap = _map_of(2)
        cleaned, cits = AskService._parse_citations("Valid [1] and bad [9].", cmap)
        assert "[1]" in cleaned
        assert "[9]" not in cleaned
        assert len(cits) == 1
        assert cits[0].ref == 1

    def test_duplicate_citation_deduplicated_in_list(self):
        cmap = _map_of(2)
        cleaned, cits = AskService._parse_citations("B-tree [1] and more [1].", cmap)
        assert len(cits) == 1  # deduplicated
        assert cleaned.count("[1]") == 2  # both kept in text

    def test_citations_ordered_by_first_appearance(self):
        cmap = _map_of(3)
        _, cits = AskService._parse_citations("Y [2] then X [1].", cmap)
        assert [c.ref for c in cits] == [2, 1]  # first seen order

    def test_no_citations_returns_unchanged(self):
        cmap = _map_of(2)
        answer = "No citations here at all."
        cleaned, cits = AskService._parse_citations(answer, cmap)
        assert cleaned == answer
        assert cits == []

    def test_whitespace_normalised_after_removal(self):
        cmap = _map_of(1)
        cleaned, _ = AskService._parse_citations("X  [5]  Y.", cmap)
        assert "  " not in cleaned  # double spaces collapsed

    def test_citation_snippet_is_first_200_chars_of_chunk_text(self):
        long_text = "Z" * 400
        cmap = [
            ContextEntry(
                ref=1, note_id=1, note_title="N", chunk_id=10,
                chunk_index=0, chunk_text=long_text,
                snippet=long_text[:200],
                intent_category=None,
            )
        ]
        _, cits = AskService._parse_citations("Answer [1].", cmap)
        assert len(cits[0].snippet) == 200

    def test_citation_carries_chunk_id(self):
        cmap = _map_of(1)
        _, cits = AskService._parse_citations("X [1].", cmap)
        assert cits[0].chunk_id == 201  # 200 + ref

    def test_citation_chunk_id_none_when_none(self):
        cmap = [
            ContextEntry(
                ref=1, note_id=1, note_title="N", chunk_id=None,
                chunk_index=0, chunk_text="text", snippet="text", intent_category=None,
            )
        ]
        _, cits = AskService._parse_citations("X [1].", cmap)
        assert cits[0].chunk_id is None


# ===========================================================================
# Citation schema
# ===========================================================================

class TestCitationSchema:
    def test_serialises_correctly(self):
        c = Citation(ref=1, note_id=42, note_title="Note A", snippet="snip")
        d = c.model_dump()
        assert d["ref"] == 1
        assert d["note_id"] == 42
        assert d["chunk_id"] is None  # default

    def test_chunk_id_can_be_set(self):
        c = Citation(ref=2, note_id=5, note_title="N", chunk_id=99, snippet="s")
        assert c.chunk_id == 99

    def test_chunk_id_can_be_none(self):
        c = Citation(ref=1, note_id=1, note_title="N", snippet="s")
        assert c.chunk_id is None


# ===========================================================================
# AskResponse schema — backward compatibility + new citations field
# ===========================================================================

class TestAskResponseSchema:
    def test_citations_defaults_empty(self):
        r = AskResponse(question="q", answer="a", sources=[])
        assert r.citations == []

    def test_old_response_without_citations_still_valid(self):
        # Simulates a client that was built before citations existed
        data = {
            "question": "q",
            "answer": "a",
            "sources": ["Note 1"],
            "retrieval_only": False,
            "status": "ok",
        }
        r = AskResponse(**data)
        assert r.citations == []

    def test_citations_populated(self):
        c = Citation(ref=1, note_id=5, note_title="N", snippet="s")
        r = AskResponse(question="q", answer="a [1]", sources=["N"], citations=[c])
        assert len(r.citations) == 1
        assert r.citations[0].ref == 1

    def test_sources_still_present_and_unchanged(self):
        r = AskResponse(question="q", answer="a", sources=["Note A", "Note B"])
        assert r.sources == ["Note A", "Note B"]


# ===========================================================================
# _synthesise() via mocked LLMService
# ===========================================================================

class TestSynthesiseWithMockedLLM:
    """
    These tests verify the full _synthesise() flow without live API calls
    by patching LLMService.generate.
    """

    def _make_service(self) -> AskService:
        mock_db = MagicMock()
        mock_chunk_service = MagicMock()
        svc = AskService.__new__(AskService)
        svc.chunk_service = mock_chunk_service
        return svc

    @patch("app.services.ask_service.LLMService")
    def test_successful_answer_includes_citations(self, mock_llm):
        mock_llm.generate.return_value = "B-tree is the default PostgreSQL index type [1]. HNSW is used for ANN vector search [2]."
        svc = self._make_service()
        # Use distinct texts so fingerprint dedup does not collapse to one entry.
        chunks = [
            _chunk(note_id=1, note_title="PostgreSQL Notes", chunk_id=10,
                   chunk_text="B-tree indexes are the default in PostgreSQL. " * 3),
            _chunk(note_id=2, note_title="Vector DB Notes", chunk_id=11, intent_category=None,
                   chunk_text="HNSW builds a layered graph of approximate neighbors. " * 3),
        ]
        result = svc._synthesise("What are index types?", chunks, ["PostgreSQL Notes", "Vector DB Notes"])
        assert result["retrieval_only"] is False
        assert result["status"] == "ok"
        assert len(result["citations"]) == 2
        assert result["citations"][0]["ref"] == 1
        assert result["citations"][1]["ref"] == 2

    @patch("app.services.ask_service.LLMService")
    def test_hallucinated_ref_removed_from_answer(self, mock_llm):
        mock_llm.generate.return_value = "B-tree [1] and nonsense [9]."
        svc = self._make_service()
        chunks = [_chunk(note_id=1, chunk_id=10)]
        result = svc._synthesise("question", chunks, ["Note"])
        assert "[9]" not in result["answer"]
        assert "[1]" in result["answer"]
        assert len(result["citations"]) == 1

    @patch("app.services.ask_service.LLMService")
    def test_no_citations_in_answer_returns_empty_list(self, mock_llm):
        mock_llm.generate.return_value = "B-tree is the default index type."
        svc = self._make_service()
        chunks = [_chunk(note_id=1, chunk_id=10)]
        result = svc._synthesise("question", chunks, ["Note"])
        assert result["citations"] == []
        assert "B-tree" in result["answer"]

    @patch("app.services.ask_service.LLMService")
    def test_sources_unchanged_alongside_citations(self, mock_llm):
        mock_llm.generate.return_value = "Answer [1]."
        svc = self._make_service()
        sources = ["Note A", "Note B"]
        chunks = [_chunk(note_id=1, chunk_id=10), _chunk(note_id=2, chunk_id=20)]
        result = svc._synthesise("q", chunks, sources)
        assert result["sources"] == sources

    @patch("app.services.ask_service.LLMService")
    def test_all_providers_exhausted_returns_retrieval_only(self, mock_llm):
        from app.services.llm_service import AllProvidersExhausted
        mock_llm.generate.side_effect = AllProvidersExhausted("quota")
        svc = self._make_service()
        chunks = [_chunk(note_id=1, chunk_id=10)]
        result = svc._synthesise("q", chunks, ["N"])
        assert result["retrieval_only"] is True
        assert result.get("citations", []) == []

    @patch("app.services.ask_service.LLMService")
    def test_parse_citations_exception_returns_uncited_answer(self, mock_llm):
        # Answer must be ≥ 20 chars with a space to survive _validate_answer.
        mock_llm.generate.return_value = "Raw answer with details about indexing [1]."
        svc = self._make_service()
        chunks = [_chunk(note_id=1, chunk_id=10,
                         chunk_text="B-tree indexes are the default in PostgreSQL. " * 3)]
        # Patch _parse_citations to raise after _validate_answer succeeds.
        with patch.object(AskService, "_parse_citations", side_effect=RuntimeError("parse fail")):
            result = svc._synthesise("q", chunks, ["N"])
        assert result["retrieval_only"] is False
        assert result["citations"] == []
        assert "Raw answer" in result["answer"]

    def test_empty_chunks_returns_no_results(self):
        svc = self._make_service()
        result = svc._synthesise("q", [], [])
        assert result["status"] == "no_results"
        assert result["citations"] == []
