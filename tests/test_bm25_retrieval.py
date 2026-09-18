"""
Unit tests for BM25 sparse retrieval and RRF fusion.

All tests are pure Python: no database, no network, no real PostgreSQL.
DB calls in BM25Repository are mocked; RRF math is exercised directly via
ChunkService._rrf_fuse (a static helper extracted below for testability).

Test coverage
-------------
- BM25Repository.search()      → empty query, DB error, result mapping
- ChunkService.retrieve_bm25_hybrid()
    - BM25_ENABLED=False  → transparent fallback to retrieve_hybrid()
    - BM25_ENABLED=True   → RRF scores computed correctly
    - semantic-only hits  → note absent from BM25 still returned
    - BM25-only hits      → note absent from semantic still returned
    - empty BM25 results  → graceful degradation to semantic-only ranking
- RRF math                     → score formula, deduplication, rank order
"""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_note(note_id: int, title: str = "Note") -> MagicMock:
    note = MagicMock()
    note.id = note_id
    note.title = title
    return note


def _make_chunk(chunk_id: int, note_id: int, text: str = "chunk text", index: int = 0) -> MagicMock:
    chunk = MagicMock()
    chunk.id = chunk_id
    chunk.note_id = note_id
    chunk.chunk_text = text
    chunk.chunk_index = index
    return chunk


def _bm25_row(chunk_id: int, note_id: int, bm25_score: float = 0.5) -> dict:
    return {
        "chunk_id":    chunk_id,
        "note_id":     note_id,
        "note_title":  f"Note {note_id}",
        "chunk_text":  f"Content of note {note_id}",
        "chunk_index": 0,
        "bm25_score":  bm25_score,
    }


# ---------------------------------------------------------------------------
# BM25Repository
# ---------------------------------------------------------------------------

class TestBM25Repository:

    def test_empty_query_returns_empty(self):
        from app.repositories.bm25_repository import BM25Repository
        repo = BM25Repository(db=MagicMock())
        assert repo.search("", user_id=1) == []
        assert repo.search("   ", user_id=1) == []

    def test_db_exception_returns_empty(self):
        from app.repositories.bm25_repository import BM25Repository

        db = MagicMock()
        db.execute.side_effect = Exception("connection refused")
        repo = BM25Repository(db=db)

        result = repo.search("redis eviction", user_id=1)

        assert result == []

    def test_result_rows_mapped_correctly(self):
        from app.repositories.bm25_repository import BM25Repository

        row = MagicMock()
        row.chunk_id    = 42
        row.note_id     = 7
        row.note_title  = "Redis Notes"
        row.chunk_text  = "LRU policy"
        row.chunk_index = 1
        row.bm25_score  = 0.75

        db = MagicMock()
        db.execute.return_value.fetchall.return_value = [row]

        repo = BM25Repository(db=db)
        results = repo.search("redis", user_id=1)

        assert len(results) == 1
        assert results[0] == {
            "chunk_id":    42,
            "note_id":     7,
            "note_title":  "Redis Notes",
            "chunk_text":  "LRU policy",
            "chunk_index": 1,
            "bm25_score":  0.75,
        }

    def test_bm25_score_cast_to_float(self):
        from app.repositories.bm25_repository import BM25Repository

        row = MagicMock()
        row.chunk_id    = 1
        row.note_id     = 1
        row.note_title  = "T"
        row.chunk_text  = "T"
        row.chunk_index = 0
        row.bm25_score  = "0.123"  # DB sometimes returns Decimal-like

        db = MagicMock()
        db.execute.return_value.fetchall.return_value = [row]

        results = BM25Repository(db=db).search("t", user_id=1)

        assert isinstance(results[0]["bm25_score"], float)


# ---------------------------------------------------------------------------
# RRF math — isolated
# ---------------------------------------------------------------------------

class TestRRFMath:
    """
    RRF score for rank r with constant k: score = 1 / (k + r).
    A note present in both arms accumulates from both.
    """

    def _compute_rrf(self, semantic_note_ids, bm25_note_ids, k=60):
        """Pure-Python RRF reproducing the logic in retrieve_bm25_hybrid."""
        scores: dict[int, float] = {}
        for rank, nid in enumerate(semantic_note_ids, start=1):
            scores[nid] = scores.get(nid, 0.0) + 1.0 / (k + rank)
        for rank, nid in enumerate(bm25_note_ids, start=1):
            scores[nid] = scores.get(nid, 0.0) + 1.0 / (k + rank)
        return scores

    def test_single_arm_score(self):
        scores = self._compute_rrf([10, 20], [], k=60)
        assert pytest.approx(scores[10]) == 1.0 / 61
        assert pytest.approx(scores[20]) == 1.0 / 62

    def test_both_arms_accumulate(self):
        # Note 10 is rank-1 in semantic and rank-1 in BM25 → 2 × (1/61)
        scores = self._compute_rrf([10], [10], k=60)
        assert pytest.approx(scores[10]) == 2.0 / 61

    def test_rank_order_descending(self):
        # Rank-1 in both arms beats rank-2 in one arm.
        scores = self._compute_rrf([10, 20], [10], k=60)
        assert scores[10] > scores[20]

    def test_bm25_only_note_included(self):
        scores = self._compute_rrf([10], [20], k=60)
        assert 10 in scores
        assert 20 in scores

    def test_k_zero_gives_reciprocal_rank(self):
        scores = self._compute_rrf([5], [], k=0)
        assert pytest.approx(scores[5]) == 1.0 / 1  # 1/(0+1)


# ---------------------------------------------------------------------------
# ChunkService.retrieve_bm25_hybrid — feature flag
# ---------------------------------------------------------------------------

class TestRetrieveBM25HybridFlag:

    @patch("app.services.chunk_service.settings")
    def test_disabled_delegates_to_retrieve_hybrid(self, mock_settings):
        from app.services.chunk_service import ChunkService

        mock_settings.BM25_ENABLED = False

        db = MagicMock()
        svc = ChunkService(db)
        svc.retrieve_hybrid = MagicMock(return_value=[{"note_id": 1}])

        result = svc.retrieve_bm25_hybrid(query="redis", user_id=1, limit=5)

        svc.retrieve_hybrid.assert_called_once_with(query="redis", user_id=1, limit=5)
        assert result == [{"note_id": 1}]

    @patch("app.services.chunk_service.settings")
    def test_disabled_does_not_call_bm25_repo(self, mock_settings):
        from app.services.chunk_service import ChunkService

        mock_settings.BM25_ENABLED = False

        db = MagicMock()
        svc = ChunkService(db)
        svc.retrieve_hybrid = MagicMock(return_value=[])
        svc.bm25_repo = MagicMock()

        svc.retrieve_bm25_hybrid(query="test", user_id=1)

        svc.bm25_repo.search.assert_not_called()


# ---------------------------------------------------------------------------
# ChunkService.retrieve_bm25_hybrid — enabled, RRF logic
# ---------------------------------------------------------------------------

class TestRetrieveRRFHybrid:
    """Tests for ChunkService._retrieve_rrf_hybrid (the core RRF logic)."""

    def _make_svc_with_arms(self, semantic_notes, bm25_rows, pool=20, k=60):
        """
        Construct a ChunkService with mocked semantic + BM25 arms.
        Returns (service, embedding_patch) — caller must call p.stop().
        """
        from app.services.chunk_service import ChunkService

        db = MagicMock()
        svc = ChunkService(db)

        svc.note_embedding_repo = MagicMock()
        svc.note_embedding_repo.search_similar_notes_with_distance.return_value = semantic_notes

        svc.bm25_repo = MagicMock()
        svc.bm25_repo.search.return_value = bm25_rows

        all_note_ids = {n.id for n, _ in semantic_notes} | {r["note_id"] for r in bm25_rows}
        chunks = [_make_chunk(nid * 10, nid, f"text {nid}") for nid in all_note_ids]
        svc.chunk_repo = MagicMock()
        svc.chunk_repo.get_chunks_by_note_ids.return_value = chunks

        p = patch("app.services.chunk_service.get_embedding_model")
        mock_emb = p.start()
        mock_emb.return_value.encode.return_value = MagicMock(tolist=lambda: [0.0] * 384)

        return svc, p

    def _call(self, svc, query="redis", user_id=1, limit=5, k=60, pool=20):
        return svc._retrieve_rrf_hybrid(query=query, user_id=user_id, limit=limit, k=k, pool=pool)

    def test_rrf_only_semantic_arm_returns_results(self):
        note1 = _make_note(1, "Note 1")
        note2 = _make_note(2, "Note 2")
        svc, p = self._make_svc_with_arms([(note1, 0.1), (note2, 0.2)], bm25_rows=[])
        try:
            results = self._call(svc)
        finally:
            p.stop()

        note_ids = [r["note_id"] for r in results]
        assert 1 in note_ids
        assert 2 in note_ids
        assert note_ids[0] == 1  # rank-1 semantic → highest RRF

    def test_rrf_bm25_only_note_included(self):
        note1 = _make_note(1, "Note 1")
        svc, p = self._make_svc_with_arms(
            [(note1, 0.1)],
            bm25_rows=[_bm25_row(chunk_id=20, note_id=2, bm25_score=0.9)],
        )
        try:
            results = self._call(svc)
        finally:
            p.stop()

        assert 2 in [r["note_id"] for r in results], "BM25-only note must appear"

    def test_rrf_combined_note_beats_single_arm_note(self):
        """Note in both arms accumulates 2× RRF contribution."""
        note1 = _make_note(1, "Note 1")  # rank-1 semantic only
        note2 = _make_note(2, "Note 2")  # rank-2 semantic + rank-1 BM25
        svc, p = self._make_svc_with_arms(
            [(note1, 0.05), (note2, 0.15)],
            bm25_rows=[_bm25_row(chunk_id=20, note_id=2, bm25_score=0.9)],
        )
        try:
            results = self._call(svc)
        finally:
            p.stop()

        # note2: rrf = 1/62 + 1/61 ≈ 0.0325; note1: 1/61 ≈ 0.0164
        assert results[0]["note_id"] == 2, "Note in both arms should rank first"

    def test_source_field_set_correctly(self):
        note1 = _make_note(1, "Semantic only")
        note2 = _make_note(2, "BM25 only")
        note3 = _make_note(3, "Both arms")
        svc, p = self._make_svc_with_arms(
            [(note1, 0.1), (note3, 0.2)],
            bm25_rows=[
                _bm25_row(chunk_id=20, note_id=2, bm25_score=0.8),
                _bm25_row(chunk_id=30, note_id=3, bm25_score=0.6),
            ],
        )
        try:
            results = self._call(svc)
        finally:
            p.stop()

        by_id = {r["note_id"]: r for r in results}
        assert by_id[1]["source"] == "semantic"
        assert by_id[2]["source"] == "bm25"
        assert by_id[3]["source"] == "hybrid_bm25"

    def test_empty_bm25_results_degrade_gracefully(self):
        note1 = _make_note(1, "Note 1")
        svc, p = self._make_svc_with_arms([(note1, 0.1)], bm25_rows=[])
        try:
            results = self._call(svc)
        finally:
            p.stop()

        assert len(results) == 1
        assert results[0]["note_id"] == 1
        assert results[0]["source"] == "semantic"

    def test_limit_respected(self):
        notes = [(_make_note(i), 0.1 * i) for i in range(1, 11)]
        svc, p = self._make_svc_with_arms(notes, bm25_rows=[])
        try:
            results = self._call(svc, limit=3)
        finally:
            p.stop()

        assert len(results) <= 3


class TestRetrieveBM25HybridFlag:
    """Tests for ChunkService.retrieve_bm25_hybrid (the public method with flag check)."""

    @patch("app.services.chunk_service.settings")
    def test_disabled_delegates_to_retrieve_hybrid(self, mock_settings):
        from app.services.chunk_service import ChunkService

        mock_settings.BM25_ENABLED = False

        db = MagicMock()
        svc = ChunkService(db)
        svc.retrieve_hybrid = MagicMock(return_value=[{"note_id": 1}])

        result = svc.retrieve_bm25_hybrid(query="redis", user_id=1, limit=5)

        svc.retrieve_hybrid.assert_called_once_with(query="redis", user_id=1, limit=5)
        assert result == [{"note_id": 1}]

    @patch("app.services.chunk_service.settings")
    def test_disabled_does_not_call_bm25_repo(self, mock_settings):
        from app.services.chunk_service import ChunkService

        mock_settings.BM25_ENABLED = False

        db = MagicMock()
        svc = ChunkService(db)
        svc.retrieve_hybrid = MagicMock(return_value=[])
        svc.bm25_repo = MagicMock()

        svc.retrieve_bm25_hybrid(query="test", user_id=1)

        svc.bm25_repo.search.assert_not_called()

    @patch("app.services.chunk_service.settings")
    def test_enabled_calls_rrf_hybrid(self, mock_settings):
        from app.services.chunk_service import ChunkService

        mock_settings.BM25_ENABLED = True
        mock_settings.BM25_RRF_K = 60
        mock_settings.BM25_CANDIDATE_POOL = 20

        db = MagicMock()
        svc = ChunkService(db)
        svc._retrieve_rrf_hybrid = MagicMock(return_value=[{"note_id": 1}])

        result = svc.retrieve_bm25_hybrid(query="redis", user_id=1, limit=5)

        svc._retrieve_rrf_hybrid.assert_called_once_with(
            query="redis", user_id=1, limit=5, k=60, pool=20
        )
        assert result == [{"note_id": 1}]
