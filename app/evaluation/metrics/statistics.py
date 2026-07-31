"""
Statistical utilities for retrieval benchmark comparison.

Pure Python (no numpy/scipy required for basic operations).  Scipy is used
for the Wilcoxon signed-rank test when available; a sign-test approximation
is provided as a fallback so the module is always importable.

All public functions accept plain sequences of floats and return plain Python
values so they are fully unit-testable without any database or service setup.
"""

from __future__ import annotations

import math
import random
import statistics
from typing import Sequence

# Optional scipy import — degrades gracefully.
try:
    from scipy.stats import wilcoxon as _scipy_wilcoxon  # type: ignore[import]
    _HAS_SCIPY = True
except ImportError:  # pragma: no cover
    _HAS_SCIPY = False


# ---------------------------------------------------------------------------
# Bootstrap confidence interval
# ---------------------------------------------------------------------------

def bootstrap_mean_ci(
    scores: Sequence[float],
    ci: float = 0.95,
    n_boot: int = 1000,
    seed: int = 42,
) -> tuple[float, float]:
    """
    95% bootstrap confidence interval for the mean of ``scores``.

    Returns (lower, upper). For n < 2, returns (mean, mean) with zero width.

    Parameters
    ----------
    scores  : Per-query scores (e.g. reciprocal ranks, hit values).
    ci      : Confidence level (default 0.95).
    n_boot  : Bootstrap resamples (default 1000).
    seed    : RNG seed for reproducibility (default 42).
    """
    n = len(scores)
    if n == 0:
        return (0.0, 0.0)
    if n == 1:
        v = float(scores[0])
        return (v, v)

    rng = random.Random(seed)
    scores_list = list(scores)

    boot_means: list[float] = []
    for _ in range(n_boot):
        sample = [rng.choice(scores_list) for _ in range(n)]
        boot_means.append(statistics.mean(sample))

    boot_means.sort()
    alpha = (1.0 - ci) / 2.0
    lower_idx = max(0, int(alpha * n_boot))
    upper_idx = min(n_boot - 1, int((1.0 - alpha) * n_boot))
    return (boot_means[lower_idx], boot_means[upper_idx])


def bootstrap_delta_ci(
    scores_a: Sequence[float],
    scores_b: Sequence[float],
    ci: float = 0.95,
    n_boot: int = 1000,
    seed: int = 42,
) -> tuple[float, float, bool]:
    """
    Bootstrap confidence interval for (mean(a) - mean(b)).

    Returns (lower, upper, significant) where ``significant`` is True if the
    CI excludes zero — i.e. the difference is statistically reliable at the
    given confidence level.

    Requires len(scores_a) == len(scores_b) (paired samples).

    Parameters
    ----------
    scores_a  : Per-query scores for strategy A (candidate).
    scores_b  : Per-query scores for strategy B (baseline).
    ci        : Confidence level (default 0.95).
    n_boot    : Bootstrap resamples (default 1000).
    seed      : RNG seed (default 42).
    """
    n = len(scores_a)
    if n != len(scores_b):
        raise ValueError(
            f"scores_a and scores_b must have the same length; "
            f"got {len(scores_a)} vs {len(scores_b)}"
        )
    if n == 0:
        return (0.0, 0.0, False)

    rng = random.Random(seed)
    pairs = list(zip(scores_a, scores_b))

    boot_deltas: list[float] = []
    for _ in range(n_boot):
        sample = [rng.choice(pairs) for _ in range(n)]
        mean_a = statistics.mean(a for a, _ in sample)
        mean_b = statistics.mean(b for _, b in sample)
        boot_deltas.append(mean_a - mean_b)

    boot_deltas.sort()
    alpha = (1.0 - ci) / 2.0
    lower_idx = max(0, int(alpha * n_boot))
    upper_idx = min(n_boot - 1, int((1.0 - alpha) * n_boot))
    lower = boot_deltas[lower_idx]
    upper = boot_deltas[upper_idx]
    significant = lower > 0.0 or upper < 0.0  # CI excludes zero
    return (lower, upper, significant)


# ---------------------------------------------------------------------------
# Wilcoxon signed-rank test
# ---------------------------------------------------------------------------

def wilcoxon_p_value(
    scores_a: Sequence[float],
    scores_b: Sequence[float],
) -> float | None:
    """
    Two-sided Wilcoxon signed-rank test on paired score differences.

    Returns the p-value (float), or None if scores are identical or scipy
    is not available.

    Uses scipy.stats.wilcoxon when available, otherwise falls back to a
    normal approximation of the sign test (less accurate but always available).
    """
    diffs = [float(a) - float(b) for a, b in zip(scores_a, scores_b)]
    nonzero = [d for d in diffs if d != 0.0]

    if not nonzero:
        return None  # all differences zero — test undefined

    if _HAS_SCIPY:
        try:
            _, p = _scipy_wilcoxon(nonzero)
            return float(p)
        except Exception:
            pass

    # Normal approximation fallback (sign test).
    n = len(nonzero)
    positives = sum(1 for d in nonzero if d > 0)
    # Under H0, positives ~ Binomial(n, 0.5) ≈ Normal(n/2, sqrt(n)/2)
    z = abs(positives - n / 2.0) / (math.sqrt(n) / 2.0)
    # Two-sided p-value from standard normal approximation
    p_approx = 2.0 * (1.0 - _standard_normal_cdf(z))
    return p_approx


def is_statistically_significant(
    scores_a: Sequence[float],
    scores_b: Sequence[float],
    alpha: float = 0.05,
) -> bool:
    """
    Return True if scores_a and scores_b are significantly different
    at the given alpha level (two-sided Wilcoxon).
    """
    p = wilcoxon_p_value(scores_a, scores_b)
    if p is None:
        return False
    return p < alpha


# ---------------------------------------------------------------------------
# Gate checking
# ---------------------------------------------------------------------------

def check_gate(
    metric_value: float,
    floor: float | None,
    ceiling: float | None = None,
) -> tuple[bool, str]:
    """
    Check a metric value against floor and ceiling gates.

    Returns (passed, reason_string).
    """
    if floor is not None and metric_value < floor:
        return (False, f"{metric_value:.4f} < floor {floor:.4f}")
    if ceiling is not None and metric_value > ceiling:
        return (False, f"{metric_value:.4f} > ceiling {ceiling:.4f}")
    return (True, "ok")


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _standard_normal_cdf(z: float) -> float:
    """Approximation of the standard normal CDF using math.erf."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))
