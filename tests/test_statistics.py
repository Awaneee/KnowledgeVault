"""
Tests for app/evaluation/metrics/statistics.py

Pure Python: no database, no network, no external models.
"""
from __future__ import annotations

import math
import pytest

from app.evaluation.metrics.statistics import (
    bootstrap_mean_ci,
    bootstrap_delta_ci,
    check_gate,
    is_statistically_significant,
    wilcoxon_p_value,
)


# ---------------------------------------------------------------------------
# bootstrap_mean_ci
# ---------------------------------------------------------------------------

class TestBootstrapMeanCI:
    def test_empty_returns_zeros(self):
        lo, hi = bootstrap_mean_ci([])
        assert lo == 0.0
        assert hi == 0.0

    def test_single_value_returns_that_value(self):
        lo, hi = bootstrap_mean_ci([0.75])
        assert lo == 0.75
        assert hi == 0.75

    def test_ci_contains_true_mean(self):
        # All ones — mean is exactly 1.0, CI should be [1.0, 1.0]
        lo, hi = bootstrap_mean_ci([1.0] * 50)
        assert lo == pytest.approx(1.0, abs=1e-6)
        assert hi == pytest.approx(1.0, abs=1e-6)

    def test_ci_width_increases_with_variance(self):
        narrow = bootstrap_mean_ci([0.5] * 50, n_boot=500, seed=42)
        wide = bootstrap_mean_ci([0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0], n_boot=500, seed=42)
        assert (narrow[1] - narrow[0]) < (wide[1] - wide[0])

    def test_ci_bounds_ordered(self):
        scores = [0.1, 0.5, 0.3, 0.9, 0.2, 0.7, 0.4, 0.8, 0.6, 0.3]
        lo, hi = bootstrap_mean_ci(scores)
        assert lo <= hi

    def test_ci_within_zero_to_one_for_bounded_scores(self):
        scores = [float(i) / 10 for i in range(11)]
        lo, hi = bootstrap_mean_ci(scores)
        assert 0.0 <= lo <= 1.0
        assert 0.0 <= hi <= 1.0

    def test_ci_is_reproducible_with_same_seed(self):
        scores = [0.6, 0.4, 0.8, 0.2, 0.7, 0.3, 0.9, 0.1, 0.5, 0.6]
        result_a = bootstrap_mean_ci(scores, seed=99)
        result_b = bootstrap_mean_ci(scores, seed=99)
        assert result_a == result_b

    def test_different_seeds_may_differ(self):
        scores = [0.1, 0.9, 0.5, 0.3, 0.7] * 4
        r_a = bootstrap_mean_ci(scores, seed=1)
        r_b = bootstrap_mean_ci(scores, seed=2)
        # Not guaranteed to differ but almost certainly will with 500 draws
        # Just check they are both valid
        assert r_a[0] <= r_a[1]
        assert r_b[0] <= r_b[1]


# ---------------------------------------------------------------------------
# bootstrap_delta_ci
# ---------------------------------------------------------------------------

class TestBootstrapDeltaCI:
    def test_empty_returns_zeros_not_significant(self):
        lo, hi, sig = bootstrap_delta_ci([], [])
        assert lo == 0.0
        assert hi == 0.0
        assert sig is False

    def test_mismatched_lengths_raises(self):
        with pytest.raises(ValueError, match="same length"):
            bootstrap_delta_ci([0.5, 0.6], [0.5])

    def test_identical_scores_not_significant(self):
        scores = [0.4, 0.6, 0.5, 0.3, 0.7] * 4
        lo, hi, sig = bootstrap_delta_ci(scores, scores)
        assert not sig
        assert abs(lo) < 0.1
        assert abs(hi) < 0.1

    def test_large_positive_delta_is_significant(self):
        # A scores much higher than B
        a = [1.0] * 30
        b = [0.0] * 30
        lo, hi, sig = bootstrap_delta_ci(a, b, n_boot=2000, seed=42)
        assert sig
        assert lo > 0.5
        assert hi > 0.5

    def test_bounds_ordered(self):
        a = [0.7, 0.8, 0.6, 0.9, 0.5] * 4
        b = [0.4, 0.5, 0.3, 0.6, 0.4] * 4
        lo, hi, _ = bootstrap_delta_ci(a, b)
        assert lo <= hi

    def test_delta_reflects_direction(self):
        a = [0.8] * 20
        b = [0.4] * 20
        lo, hi, sig = bootstrap_delta_ci(a, b, n_boot=500, seed=42)
        assert lo > 0  # CI should be entirely positive (a > b)

    def test_negative_delta_produces_negative_ci(self):
        a = [0.2] * 20
        b = [0.8] * 20
        lo, hi, sig = bootstrap_delta_ci(a, b, n_boot=500, seed=42)
        assert hi < 0  # CI should be entirely negative (a < b)


# ---------------------------------------------------------------------------
# wilcoxon_p_value
# ---------------------------------------------------------------------------

class TestWilcoxonPValue:
    def test_identical_scores_returns_none(self):
        a = [0.5, 0.5, 0.5, 0.5, 0.5]
        p = wilcoxon_p_value(a, a)
        assert p is None

    def test_clearly_different_scores_small_p(self):
        a = [1.0] * 20
        b = [0.0] * 20
        p = wilcoxon_p_value(a, b)
        assert p is not None
        assert p < 0.05

    def test_p_value_in_zero_one(self):
        a = [0.6, 0.7, 0.5, 0.8, 0.4, 0.6, 0.7, 0.5, 0.8, 0.4]
        b = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        p = wilcoxon_p_value(a, b)
        if p is not None:
            assert 0.0 <= p <= 1.0

    def test_symmetric_returns_same_p(self):
        a = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
        b = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        p1 = wilcoxon_p_value(a, b)
        p2 = wilcoxon_p_value(b, a)
        if p1 is not None and p2 is not None:
            assert pytest.approx(p1, abs=0.01) == p2


# ---------------------------------------------------------------------------
# is_statistically_significant
# ---------------------------------------------------------------------------

class TestIsStatisticallySignificant:
    def test_identical_not_significant(self):
        a = [0.5] * 10
        assert not is_statistically_significant(a, a)

    def test_large_difference_significant(self):
        a = [1.0] * 30
        b = [0.0] * 30
        assert is_statistically_significant(a, b)

    def test_identical_values_not_significant(self):
        a = [0.7, 0.7, 0.7]
        b = [0.7, 0.7, 0.7]
        assert not is_statistically_significant(a, b)


# ---------------------------------------------------------------------------
# check_gate
# ---------------------------------------------------------------------------

class TestCheckGate:
    def test_no_gate_passes(self):
        passed, reason = check_gate(0.5)
        assert passed
        assert reason == "ok"

    def test_above_floor_passes(self):
        passed, reason = check_gate(0.62, floor=0.58)
        assert passed
        assert reason == "ok"

    def test_below_floor_fails(self):
        passed, reason = check_gate(0.55, floor=0.58)
        assert not passed
        assert "floor" in reason

    def test_below_ceiling_passes(self):
        passed, reason = check_gate(120.0, ceiling=300.0)
        assert passed

    def test_above_ceiling_fails(self):
        passed, reason = check_gate(450.0, ceiling=300.0)
        assert not passed
        assert "ceiling" in reason

    def test_none_floor_is_ignored(self):
        passed, _ = check_gate(0.001, floor=None)
        assert passed

    def test_none_ceiling_is_ignored(self):
        passed, _ = check_gate(999999.0, ceiling=None)
        assert passed


def check_gate(value: float, floor=None, ceiling=None):
    from app.evaluation.metrics.statistics import check_gate as _cg
    return _cg(value, floor, ceiling)
