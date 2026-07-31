"""
Tests for scripts/check_benchmark_confounds.py

All tests are pure Python: no database, no network.
The confound check functions are imported directly (no subprocess).
"""
from __future__ import annotations

import pytest
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.check_benchmark_confounds import (
    check_note_id_validity,
    check_pool_latency_consistency,
    check_strategy_identity,
    check_gates,
)


# ---------------------------------------------------------------------------
# C1: Pool-latency consistency
# ---------------------------------------------------------------------------

def _make_results(hybrid_lat: float, rerank_lat: float, n: int = 5) -> list[dict]:
    rows = []
    for i in range(n):
        rows.append({"strategy": "hybrid", "latency_ms": str(hybrid_lat), "benchmark_id": str(i)})
        rows.append({"strategy": "rerank", "latency_ms": str(rerank_lat), "benchmark_id": str(i)})
    return rows


class TestPoolLatencyConsistency:
    def test_no_issue_when_rerank_much_slower(self):
        results = _make_results(100.0, 420.0)
        issues = check_pool_latency_consistency(results)
        assert issues == []

    def test_issue_when_rerank_only_slightly_slower(self):
        results = _make_results(100.0, 109.0)
        issues = check_pool_latency_consistency(results)
        assert len(issues) == 1
        assert "[C1]" in issues[0]

    def test_issue_when_rerank_same_as_hybrid(self):
        results = _make_results(100.0, 100.0)
        issues = check_pool_latency_consistency(results)
        assert len(issues) == 1

    def test_no_issue_when_exactly_50ms_overhead(self):
        results = _make_results(100.0, 150.0)
        issues = check_pool_latency_consistency(results)
        assert issues == []

    def test_no_issue_when_only_one_strategy(self):
        # Only HYBRID — cannot compare
        results = [{"strategy": "hybrid", "latency_ms": "100.0", "benchmark_id": "1"}]
        issues = check_pool_latency_consistency(results)
        assert issues == []

    def test_no_issue_when_no_results(self):
        issues = check_pool_latency_consistency([])
        assert issues == []


# ---------------------------------------------------------------------------
# C2: Note ID validity
# ---------------------------------------------------------------------------

class TestNoteIdValidity:
    def test_all_ids_present_returns_empty(self):
        benchmark = [{"id": "1", "relevant_note_ids": [54, 55, 56]}]
        db_ids = {54, 55, 56, 100, 101}
        issues = check_note_id_validity(benchmark, db_ids)
        assert issues == []

    def test_missing_id_returns_issue(self):
        benchmark = [{"id": "1", "relevant_note_ids": [54, 999]}]
        db_ids = {54, 55}
        issues = check_note_id_validity(benchmark, db_ids)
        assert len(issues) == 1
        assert "[C2]" in issues[0]
        assert "999" in issues[0]

    def test_multiple_missing_ids(self):
        benchmark = [
            {"id": "1", "relevant_note_ids": [1, 2, 3]},
            {"id": "2", "relevant_note_ids": [4, 5, 6]},
        ]
        db_ids = {1, 2, 4}  # 3, 5, 6 are missing
        issues = check_note_id_validity(benchmark, db_ids)
        # One issue per missing note_id (3 missing: 3, 5, 6)
        assert len(issues) == 3

    def test_empty_benchmark_returns_empty(self):
        issues = check_note_id_validity([], {1, 2, 3})
        assert issues == []

    def test_entry_with_no_relevant_ids_returns_empty(self):
        benchmark = [{"id": "1", "relevant_note_ids": []}]
        issues = check_note_id_validity(benchmark, set())
        assert issues == []


# ---------------------------------------------------------------------------
# C3: Strategy identity
# ---------------------------------------------------------------------------

def _make_results_with_ids(
    query_ids: list[str],
    hybrid_ids: list[str],
    rerank_ids: list[str],
) -> list[dict]:
    rows = []
    for qid, h_ids, r_ids in zip(query_ids, hybrid_ids, rerank_ids):
        rows.append({
            "benchmark_id": qid, "strategy": "hybrid",
            "retrieved_note_ids": h_ids, "latency_ms": "100",
        })
        rows.append({
            "benchmark_id": qid, "strategy": "rerank",
            "retrieved_note_ids": r_ids, "latency_ms": "420",
        })
    return rows


class TestStrategyIdentity:
    def test_different_results_returns_empty(self):
        results = _make_results_with_ids(
            ["1", "2"],
            ["1,2,3", "4,5,6"],
            ["2,1,3", "5,4,6"],   # reranked: order changed
        )
        issues = check_strategy_identity(results)
        assert issues == []

    def test_identical_results_all_queries_raises_issue(self):
        results = _make_results_with_ids(
            ["1", "2"],
            ["1,2,3", "4,5,6"],
            ["1,2,3", "4,5,6"],   # identical
        )
        issues = check_strategy_identity(results)
        assert len(issues) == 1
        assert "[C3]" in issues[0]

    def test_no_results_returns_empty(self):
        issues = check_strategy_identity([])
        assert issues == []

    def test_partial_identity_over_90pct_warns(self):
        # 9/10 queries identical
        qids = [str(i) for i in range(10)]
        same = ["1,2,3"] * 10
        different = ["1,2,3"] * 9 + ["3,2,1"]  # one different
        results = _make_results_with_ids(qids, same, different)
        issues = check_strategy_identity(results)
        assert len(issues) == 1
        assert "[C3]" in issues[0]


# ---------------------------------------------------------------------------
# Gate checks
# ---------------------------------------------------------------------------

def _make_results_with_metrics(
    strategy: str,
    rr: float,
    hit: str,
    lat: float,
    n: int = 10,
) -> list[dict]:
    return [
        {
            "strategy": strategy,
            "reciprocal_rank": str(rr),
            "hit": hit,
            "latency_ms": str(lat),
        }
        for _ in range(n)
    ]


class TestGateChecks:
    def test_above_floor_passes(self):
        results = _make_results_with_metrics("hybrid", rr=0.65, hit="True", lat=150.0)
        gates = {
            "strategies": {
                "HYBRID": {"mrr_floor": 0.58, "hit_rate_floor": 0.72, "avg_latency_ms_ceiling": 300.0}
            }
        }
        issues = check_gates(results, gates)
        assert issues == []

    def test_below_mrr_floor_fails(self):
        results = _make_results_with_metrics("hybrid", rr=0.50, hit="True", lat=100.0)
        gates = {
            "strategies": {
                "HYBRID": {"mrr_floor": 0.58, "hit_rate_floor": 0.70, "avg_latency_ms_ceiling": None}
            }
        }
        issues = check_gates(results, gates)
        assert any("[GATE]" in i and "MRR" in i for i in issues)

    def test_above_latency_ceiling_fails(self):
        results = _make_results_with_metrics("semantic", rr=0.65, hit="True", lat=500.0)
        gates = {
            "strategies": {
                "SEMANTIC": {"mrr_floor": None, "hit_rate_floor": None, "avg_latency_ms_ceiling": 100.0}
            }
        }
        issues = check_gates(results, gates)
        assert any("[GATE]" in i and "Latency" in i for i in issues)

    def test_none_floors_always_pass(self):
        results = _make_results_with_metrics("hybrid", rr=0.01, hit="False", lat=999.0)
        gates = {
            "strategies": {
                "HYBRID": {"mrr_floor": None, "hit_rate_floor": None, "avg_latency_ms_ceiling": None}
            }
        }
        issues = check_gates(results, gates)
        assert issues == []

    def test_unknown_strategy_in_gates_is_ignored(self):
        results = _make_results_with_metrics("hybrid", rr=0.6, hit="True", lat=100.0)
        gates = {
            "strategies": {
                "UNKNOWN_STRATEGY": {"mrr_floor": 0.90}
            }
        }
        # hybrid not in gates → no checks → no issues
        issues = check_gates(results, gates)
        assert issues == []
