"""
Information-retrieval metrics.

Pure Python. No database. No services. Fully unit-testable.

All functions accept:
    retrieved   : ordered list of retrieved note IDs (most relevant first)
    relevant    : set (or list) of ground-truth relevant note IDs
    k           : cut-off rank
"""

from __future__ import annotations

import statistics
from typing import Sequence


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
# nDCG@K
# ---------------------------------------------------------------------------

import math

def ndcg_at_k(
    retrieved: Sequence[int],
    relevant: Sequence[int],
    k: int,
) -> float:
    """
    Normalized Discounted Cumulative Gain at K.
    Assuming binary relevance (1 if relevant, 0 otherwise).
    """
    if k <= 0 or not relevant:
        return 0.0

    relevant_set = set(relevant)
    dcg = 0.0
    for i, item in enumerate(retrieved[:k]):
        if item in relevant_set:
            dcg += 1.0 / math.log2(i + 2)  # +2 because i is 0-indexed and log2(rank+1)

    idcg = 0.0
    for i in range(min(k, len(relevant_set))):
        idcg += 1.0 / math.log2(i + 2)

    if idcg == 0.0:
        return 0.0

    return dcg / idcg

def mean_ndcg_at_k(
    all_retrieved: Sequence[Sequence[int]],
    all_relevant: Sequence[Sequence[int]],
    k: int,
) -> float:
    """
    Average nDCG@K across multiple queries.
    """
    if not all_retrieved:
        return 0.0

    scores = [
        ndcg_at_k(retrieved, relevant, k)
        for retrieved, relevant in zip(all_retrieved, all_relevant)
    ]
    return statistics.mean(scores)
