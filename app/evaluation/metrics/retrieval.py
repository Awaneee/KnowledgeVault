"""
Information-retrieval metrics.

Pure Python. No database. No services. Fully unit-testable.

All functions accept:
    retrieved   : ordered list of retrieved note IDs (most relevant first)
    relevant    : set (or list) of ground-truth relevant note IDs
    k           : cut-off rank

Graded relevance
----------------
``ndcg_at_k`` accepts an optional ``grade_map`` argument (dict mapping
note_id → integer grade ∈ {0,1,2}).  When provided, gain = 2^grade − 1 is
used in place of binary 0/1, giving grade-2 hits more weight than grade-1
hits.  ``relevant`` must still list all non-zero-grade IDs so that IDCG can
be computed correctly.
"""

from __future__ import annotations

import math
import statistics
from typing import Optional, Sequence


# ---------------------------------------------------------------------------
# Precision@K
# ---------------------------------------------------------------------------

def precision_at_k(
    retrieved: Sequence[int],
    relevant: Sequence[int],
    k: int,
) -> float:
    """
    Fraction of the top-K retrieved items that are relevant.

        P@K = |{retrieved[:k]} ∩ relevant| / K

    Returns 0.0 when k <= 0.
    """
    if k <= 0:
        return 0.0

    top_k = set(retrieved[:k])
    relevant_set = set(relevant)
    hits = len(top_k & relevant_set)
    return hits / k


# ---------------------------------------------------------------------------
# Recall@K
# ---------------------------------------------------------------------------

def recall_at_k(
    retrieved: Sequence[int],
    relevant: Sequence[int],
    k: int,
) -> float:
    """
    Fraction of all relevant items that appear in the top-K results.

        R@K = |{retrieved[:k]} ∩ relevant| / |relevant|

    Returns 0.0 when the relevant set is empty.
    """
    relevant_set = set(relevant)
    if not relevant_set:
        return 0.0

    top_k = set(retrieved[:k])
    hits = len(top_k & relevant_set)
    return hits / len(relevant_set)


# ---------------------------------------------------------------------------
# R-Precision
# ---------------------------------------------------------------------------

def r_precision(
    retrieved: Sequence[int],
    relevant: Sequence[int],
) -> float:
    """
    Precision at K = |relevant|.

    Evaluates whether the system can retrieve exactly the right number of
    results when the relevant set size is known.  Useful for comparing
    strategies on queries with very different relevant-set sizes.

    Returns 0.0 when the relevant set is empty.
    """
    relevant_set = set(relevant)
    if not relevant_set:
        return 0.0
    R = len(relevant_set)
    hits = sum(1 for item in retrieved[:R] if item in relevant_set)
    return hits / R


# ---------------------------------------------------------------------------
# Hit Rate (binary relevance in top-K)
# ---------------------------------------------------------------------------

def hit_rate(
    retrieved: Sequence[int],
    relevant: Sequence[int],
    k: int,
) -> bool:
    """
    True if at least one relevant item appears in the top-K results.
    """
    relevant_set = set(relevant)
    return bool(set(retrieved[:k]) & relevant_set)


# ---------------------------------------------------------------------------
# Reciprocal Rank
# ---------------------------------------------------------------------------

def reciprocal_rank(
    retrieved: Sequence[int],
    relevant: Sequence[int],
) -> float:
    """
    1 / rank of the first relevant item in the retrieved list.
    Returns 0.0 if no relevant item is found.

    Rank is 1-indexed.
    """
    relevant_set = set(relevant)
    for rank, item in enumerate(retrieved, start=1):
        if item in relevant_set:
            return 1.0 / rank
    return 0.0


# ---------------------------------------------------------------------------
# Mean Reciprocal Rank
# ---------------------------------------------------------------------------

def mean_reciprocal_rank(
    all_retrieved: Sequence[Sequence[int]],
    all_relevant: Sequence[Sequence[int]],
) -> float:
    """
    Average Reciprocal Rank across multiple queries.

        MRR = (1/|Q|) * Σ RR(q)

    Returns 0.0 if the query list is empty.

    Parameters
    ----------
    all_retrieved : one list of retrieved IDs per query
    all_relevant  : one list of relevant IDs per query (parallel to above)
    """
    if not all_retrieved:
        return 0.0

    rr_scores = [
        reciprocal_rank(retrieved, relevant)
        for retrieved, relevant in zip(all_retrieved, all_relevant)
    ]
    return statistics.mean(rr_scores)


# ---------------------------------------------------------------------------
# Mean Average Precision (MAP)
# ---------------------------------------------------------------------------

def average_precision_at_k(
    retrieved: Sequence[int],
    relevant: Sequence[int],
    k: int,
) -> float:
    """
    Average Precision at K for a single query.

    AP@K = (1 / |relevant|) * Σ_r P@r × rel(r)

    where r ranges over ranks 1..k and rel(r) = 1 if item at rank r is
    relevant.  Returns 0.0 when the relevant set is empty.
    """
    relevant_set = set(relevant)
    if not relevant_set:
        return 0.0

    hits = 0
    precision_sum = 0.0
    for rank, item in enumerate(retrieved[:k], start=1):
        if item in relevant_set:
            hits += 1
            precision_sum += hits / rank

    return precision_sum / len(relevant_set)


def mean_average_precision(
    all_retrieved: Sequence[Sequence[int]],
    all_relevant: Sequence[Sequence[int]],
    k: int,
) -> float:
    """Mean AP@K across multiple queries. Returns 0.0 for empty input."""
    if not all_retrieved:
        return 0.0
    scores = [
        average_precision_at_k(r, rel, k)
        for r, rel in zip(all_retrieved, all_relevant)
    ]
    return statistics.mean(scores)


# ---------------------------------------------------------------------------
# nDCG@K  (binary or graded relevance)
# ---------------------------------------------------------------------------

def ndcg_at_k(
    retrieved: Sequence[int],
    relevant: Sequence[int],
    k: int,
    grade_map: Optional[dict[int | str, int]] = None,
) -> float:
    """
    Normalized Discounted Cumulative Gain at K.

    When ``grade_map`` is None, binary relevance is assumed: gain = 1 for
    any note in ``relevant``, 0 otherwise.

    When ``grade_map`` is provided (note_id → integer grade), graded gain is
    used: gain = 2^grade − 1.  Both integer and string keys are accepted
    (JSON grade_map dicts have string keys).

    Parameters
    ----------
    retrieved  : ranked list of retrieved note IDs.
    relevant   : list of all non-zero-grade note IDs (for IDCG computation).
    k          : cut-off rank.
    grade_map  : optional mapping note_id → grade ∈ {0, 1, 2, ...}.
    """
    if k <= 0 or not relevant:
        return 0.0

    relevant_set = set(relevant)

    if grade_map is None:
        # Binary relevance
        def _gain(note_id: int) -> float:
            return 1.0 if note_id in relevant_set else 0.0

        ideal_grades = [1.0] * min(k, len(relevant_set))
    else:
        # Normalise keys to int for consistent lookup
        _gmap: dict[int, int] = {}
        for key, grade in grade_map.items():
            try:
                _gmap[int(key)] = int(grade)
            except (ValueError, TypeError):
                pass

        def _gain(note_id: int) -> float:
            g = _gmap.get(note_id, 0)
            return float(2 ** g - 1)

        ideal_grades = sorted(
            (float(2 ** g - 1) for g in _gmap.values() if g > 0),
            reverse=True,
        )

    dcg = sum(
        _gain(item) / math.log2(i + 2)
        for i, item in enumerate(retrieved[:k])
    )

    idcg = sum(
        g / math.log2(i + 2)
        for i, g in enumerate(ideal_grades[:k])
    )

    return dcg / idcg if idcg > 0.0 else 0.0


def mean_ndcg_at_k(
    all_retrieved: Sequence[Sequence[int]],
    all_relevant: Sequence[Sequence[int]],
    k: int,
) -> float:
    """Average nDCG@K across multiple queries."""
    if not all_retrieved:
        return 0.0

    scores = [
        ndcg_at_k(retrieved, relevant, k)
        for retrieved, relevant in zip(all_retrieved, all_relevant)
    ]
    return statistics.mean(scores)
