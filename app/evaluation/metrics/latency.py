"""
Latency metrics.

Pure Python. No database. No services. Unit-testable.

All functions accept a sequence of latency values in milliseconds (float).
"""

from __future__ import annotations

import math
import statistics
from typing import Sequence


def average_latency(latencies: Sequence[float]) -> float:
    """Arithmetic mean latency in milliseconds. Returns 0.0 for empty input."""
    if not latencies:
        return 0.0
    return statistics.mean(latencies)


def median_latency(latencies: Sequence[float]) -> float:
    """Median latency in milliseconds. Returns 0.0 for empty input."""
    if not latencies:
        return 0.0
    return statistics.median(latencies)


def p95_latency(latencies: Sequence[float]) -> float:
    """
    95th-percentile latency in milliseconds.

    Uses linear interpolation (same method as numpy.percentile default and
    Python 3.12 statistics.quantiles) so results are deterministic without
    requiring numpy.

    Returns 0.0 for empty input.
    """
    if not latencies:
        return 0.0

    sorted_vals = sorted(latencies)
    n = len(sorted_vals)

    if n == 1:
        return sorted_vals[0]

    # Linear interpolation between the two surrounding values.
    # index = (p/100) * (n - 1)
    index = 0.95 * (n - 1)
    lower = math.floor(index)
    upper = math.ceil(index)
    fraction = index - lower

    return sorted_vals[lower] + fraction * (sorted_vals[upper] - sorted_vals[lower])


def max_latency(latencies: Sequence[float]) -> float:
    """Maximum latency in milliseconds. Returns 0.0 for empty input."""
    if not latencies:
        return 0.0
    return max(latencies)
