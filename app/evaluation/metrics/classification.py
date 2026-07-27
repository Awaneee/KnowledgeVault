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

def canonicalize_category_name(name: Optional[str]) -> str:
    if name is None:
        return ""
    cleaned = name.strip().lower()
    
    if cleaned in {"study tasks", "study"}:
        return "study"
    if cleaned.startswith("study tasks - ") or cleaned.startswith("study - "):
        return "study"
        
    if cleaned in {"reference notes", "reference"}:
        return "reference"
    if cleaned.startswith("reference notes - ") or cleaned.startswith("reference - "):
        return "reference"
        
    if cleaned == "to do":
        return "tasks"
    todo_buckets = {"tasks", "shopping", "bills", "appointments", "errands", "health", "finance", "travel"}
    if cleaned in todo_buckets:
        return "tasks"
        
    if cleaned == "things to tell sid":
        return "communication"
    if cleaned.startswith("communication"):
        return "communication"
        
    if cleaned == "questions":
        return "questions"
    if cleaned.startswith("questions - "):
        return "questions"
        
    if cleaned == "meetings":
        return "meetings"
    if cleaned.startswith("meetings - "):
        return "meetings"
        
    if cleaned == "ideas":
        return "ideas"
    if cleaned.startswith("ideas - "):
        return "ideas"
        
    if cleaned == "reminders":
        return "reminders"
        
    return cleaned

def category_accuracy(
    predicted_categories: Sequence[Optional[str]],
    expected_categories: Sequence[str],
) -> float:
    """
    Fraction of queries where the predicted category name matches the
    expected category name (after canonicalization of stale/old names).

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
        and canonicalize_category_name(predicted) == canonicalize_category_name(expected)
    )

    return correct / len(expected_categories)
