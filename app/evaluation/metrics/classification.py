"""
Classification metrics for intent and category evaluation.

Pure Python. No database. No services. Unit-testable.

Both functions accept optional strings; None is treated as "no prediction
available" and is counted as incorrect.
"""

from __future__ import annotations

from typing import Optional, Sequence


# ---------------------------------------------------------------------------
# Intent Accuracy
# ---------------------------------------------------------------------------

def intent_accuracy(
    predicted_intents: Sequence[Optional[str]],
    expected_intents: Sequence[str],
) -> float:
    """
    Fraction of queries where the predicted intent_type exactly matches
    the expected intent_type.

        accuracy = correct / total

    A None prediction is always counted as incorrect.
    Returns 0.0 if the sequence is empty.

    Both predicted and expected are compared case-insensitively after
    stripping whitespace, matching the normalisation applied by
    IntentExtractionService._clean_token().
    """
    if not expected_intents:
        return 0.0

    if len(predicted_intents) != len(expected_intents):
        raise ValueError(
            "predicted_intents and expected_intents must have the same length; "
            f"got {len(predicted_intents)} vs {len(expected_intents)}"
        )

    correct = sum(
        1
        for predicted, expected in zip(predicted_intents, expected_intents)
        if predicted is not None
        and predicted.strip().lower() == expected.strip().lower()
    )

    return correct / len(expected_intents)


# ---------------------------------------------------------------------------
# Category Accuracy
# ---------------------------------------------------------------------------

def category_accuracy(
    predicted_categories: Sequence[Optional[str]],
    expected_categories: Sequence[str],
) -> float:
    """
    Fraction of queries where the predicted category name exactly matches
    the expected category name.

    Comparison is case-insensitive after stripping whitespace, matching
    the format produced by IntentCategoryService._generate_category_name().

    A None prediction is always counted as incorrect.
    Returns 0.0 if the sequence is empty.
    """
    if not expected_categories:
        return 0.0

    if len(predicted_categories) != len(expected_categories):
        raise ValueError(
            "predicted_categories and expected_categories must have the same "
            f"length; got {len(predicted_categories)} vs {len(expected_categories)}"
        )

    correct = sum(
        1
        for predicted, expected in zip(predicted_categories, expected_categories)
        if predicted is not None
        and predicted.strip().lower() == expected.strip().lower()
    )

    return correct / len(expected_categories)
