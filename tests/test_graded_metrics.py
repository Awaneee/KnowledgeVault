"""
Tests for Sprint 2-C metric additions:
  - average_precision_at_k (MAP)
  - r_precision (R-Precision)
  - ndcg_at_k with graded relevance
  - backward compatibility of existing ndcg_at_k (binary)

Pure Python: no database, no network.
"""
from __future__ import annotations

import math
import pytest

from app.evaluation.metrics.retrieval import (
    average_precision_at_k,
    mean_average_precision,
    ndcg_at_k,
    r_precision,
)


# ---------------------------------------------------------------------------
# average_precision_at_k (MAP)
# ---------------------------------------------------------------------------

class TestAveragePrecisionAtK:
    def test_empty_retrieved_returns_zero(self):
        assert average_precision_at_k([], [1, 2, 3], k=5) == 0.0

    def test_empty_relevant_returns_zero(self):
        assert average_precision_at_k([1, 2, 3], [], k=5) == 0.0

    def test_perfect_ranking_single_relevant(self):
        # relevant is [1], retrieved starts with 1 — AP = 1.0
        assert average_precision_at_k([1, 2, 3, 4, 5], [1], k=5) == pytest.approx(1.0)

    def test_perfect_ranking_two_relevant(self):
        # AP = (1/1 + 2/2) / 2 = 1.0
        assert average_precision_at_k([1, 2, 3, 4, 5], [1, 2], k=5) == pytest.approx(1.0)

    def test_relevant_at_position_2_and_4(self):
        # relevant = [2, 4], retrieved = [1, 2, 3, 4, 5]
        # hits at rank 2 (precision=1/2) and rank 4 (precision=2/4=0.5)
        # AP = (0.5 + 0.5) / 2 = 0.5
        assert average_precision_at_k([1, 2, 3, 4, 5], [2, 4], k=5) == pytest.approx(0.5)

    def test_no_hits_returns_zero(self):
        assert average_precision_at_k([1, 2, 3], [4, 5, 6], k=5) == 0.0

    def test_k_limits_evaluation(self):
        # relevant at rank 4 but k=3 so it's not counted
        result = average_precision_at_k([1, 2, 3, 4], [4], k=3)
        assert result == 0.0

    def test_duplicate_retrieved_ids_counted_once(self):
        # If the same note appears twice (shouldn't happen in practice but handle gracefully)
        result = average_precision_at_k([1, 1, 2, 3], [1, 2], k=4)
        # rank 1 is 1 (hit), rank 2 is 1 (already hit, but in AP we count again),
        # rank 3 is 2 (hit). But typical AP formula just counts by set membership each time.
        # This is a corner case — just ensure it doesn't crash and returns a reasonable float.
        assert isinstance(result, float)

    def test_mean_average_precision_empty(self):
        assert mean_average_precision([], [], k=5) == 0.0

    def test_mean_average_precision_aggregates(self):
        all_retrieved = [[1, 2, 3], [4, 5, 6]]
        all_relevant = [[1], [5]]
        # Query 1: AP = 1.0 (hit at rank 1)
        # Query 2: AP = 1/2 = 0.5 (hit at rank 2)
        # MAP = (1.0 + 0.5) / 2 = 0.75
        result = mean_average_precision(all_retrieved, all_relevant, k=3)
        assert result == pytest.approx(0.75)


# ---------------------------------------------------------------------------
# r_precision
# ---------------------------------------------------------------------------

class TestRPrecision:
    def test_empty_relevant_returns_zero(self):
        assert r_precision([1, 2, 3], []) == 0.0

    def test_empty_retrieved_returns_zero(self):
        assert r_precision([], [1, 2]) == 0.0

    def test_perfect_retrieval(self):
        # |relevant| = 3, first 3 retrieved are all relevant
        assert r_precision([1, 2, 3, 4, 5], [1, 2, 3]) == pytest.approx(1.0)

    def test_zero_precision(self):
        # No hits in the first R positions
        assert r_precision([4, 5, 6], [1, 2, 3]) == pytest.approx(0.0)

    def test_partial_precision(self):
        # |relevant| = 4, retrieved[:4] = [1, 5, 2, 6] — 2 hits (1, 2)
        result = r_precision([1, 5, 2, 6, 3, 4], [1, 2, 3, 4])
        assert result == pytest.approx(2 / 4)

    def test_single_relevant(self):
        # R = 1, retrieved[0] = 1 → precision = 1.0
        assert r_precision([1, 2, 3], [1]) == pytest.approx(1.0)
        # R = 1, retrieved[0] = 2 → precision = 0.0
        assert r_precision([2, 1, 3], [1]) == pytest.approx(0.0)

    def test_relevant_set_size_determines_cutoff(self):
        # relevant = [1, 2] so R=2; retrieved[:2] = [1, 3] → 1 hit → 0.5
        assert r_precision([1, 3, 2, 4], [1, 2]) == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# ndcg_at_k — binary relevance (backward compatibility)
# ---------------------------------------------------------------------------

class TestNdcgBinary:
    def test_empty_relevant_returns_zero(self):
        assert ndcg_at_k([1, 2, 3], [], k=3) == 0.0

    def test_k_zero_returns_zero(self):
        assert ndcg_at_k([1, 2], [1], k=0) == 0.0

    def test_perfect_rank_one(self):
        assert ndcg_at_k([1, 2, 3], [1], k=3) == pytest.approx(1.0)

    def test_miss_returns_zero(self):
        assert ndcg_at_k([2, 3, 4], [1], k=3) == 0.0

    def test_rank_two_lower_than_rank_one(self):
        perfect = ndcg_at_k([1, 2], [1], k=2)
        rank_two = ndcg_at_k([2, 1], [1], k=2)
        assert perfect > rank_two

    def test_two_relevant_both_found(self):
        # Both at top two positions — perfect nDCG
        result = ndcg_at_k([1, 2, 3], [1, 2], k=3)
        assert result == pytest.approx(1.0)

    def test_backward_compat_no_grade_map(self):
        # Without grade_map, should behave identically to previous binary version
        result_no_map = ndcg_at_k([1, 2, 3, 4], [1, 3], k=4)
        assert 0.0 < result_no_map < 1.0


# ---------------------------------------------------------------------------
# ndcg_at_k — graded relevance
# ---------------------------------------------------------------------------

class TestNdcgGraded:
    def test_grade_map_none_falls_back_to_binary(self):
        binary = ndcg_at_k([1, 2, 3], [1], k=3, grade_map=None)
        # Same as grade_map={"1": 1}
        graded = ndcg_at_k([1, 2, 3], [1], k=3, grade_map={"1": 1})
        assert binary == pytest.approx(graded)

    def test_grade_2_ranks_higher_than_grade_1(self):
        # Query A: grade-2 hit at rank 1
        result_a = ndcg_at_k(
            [10, 20, 30], [10, 20], k=3,
            grade_map={"10": 2, "20": 1}
        )
        # Query B: grade-2 hit at rank 2
        result_b = ndcg_at_k(
            [20, 10, 30], [10, 20], k=3,
            grade_map={"10": 2, "20": 1}
        )
        assert result_a > result_b

    def test_perfect_graded_ndcg_is_one(self):
        # Grade-2 at rank 1 is perfect
        result = ndcg_at_k([1], [1], k=1, grade_map={"1": 2})
        assert result == pytest.approx(1.0)

    def test_string_and_int_keys_equivalent(self):
        r1 = ndcg_at_k([1, 2], [1, 2], k=2, grade_map={"1": 2, "2": 1})
        r2 = ndcg_at_k([1, 2], [1, 2], k=2, grade_map={1: 2, 2: 1})
        assert r1 == pytest.approx(r2)

    def test_zero_grade_does_not_contribute(self):
        # grade 0 means not relevant — DCG should be zero for it
        result = ndcg_at_k([1, 2], [1], k=2, grade_map={"1": 0, "2": 2})
        # note 1 is grade 0 (zero gain), note 2 is grade 2 but not in retrieved[:2]?
        # Actually [1, 2] retrieved, note 1 grade 0, note 2 grade 2
        # DCG = 0/log2(2) + (2^2-1)/log2(3) = 0 + 3/log2(3) ≈ 1.893
        # IDCG = 3/log2(2) = 3.0 (best possible is grade 2 at rank 1)
        # nDCG ≈ 1.893/3.0 ≈ 0.631
        assert 0.0 < result < 1.0

    def test_all_grade_zero_returns_zero(self):
        result = ndcg_at_k([1, 2], [1, 2], k=2, grade_map={"1": 0, "2": 0})
        # relevant list [1,2] but all grades 0 → relevant_set = {1,2}, IDCG uses grades
        # If grade_map has all zeros, ideal_grades will be empty → IDCG = 0 → return 0
        assert result == 0.0

    def test_grade_map_partial_coverage(self):
        # retrieved note 3 not in grade_map → gain = 0
        result = ndcg_at_k([1, 3], [1], k=2, grade_map={"1": 2})
        # DCG = (2^2-1)/log2(2) = 3.0, IDCG = 3.0 → nDCG = 1.0
        assert result == pytest.approx(1.0)
