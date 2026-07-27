"""
Unit tests for production hardening:
  - Intent validation and auto-repair
  - Concise naming rules (maximum 4 words)
  - Fast classifier actor and topic extraction
  - Category compatibility and reuse checks
"""

import pytest
from unittest.mock import MagicMock

from app.services.intent_extraction_service import IntentExtractionService
from app.services.intent_category_service import IntentCategoryService


@pytest.fixture
def extraction_service():
    return IntentExtractionService()


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def category_service(mock_db):
    return IntentCategoryService(mock_db)


# ---------------------------------------------------------------------------
# Test validation & auto-repair (Part 5)
# ---------------------------------------------------------------------------

def test_intent_validation_basic(extraction_service):
    # Valid input should pass through
    raw_data = {
        "intent_type": "study",
        "action": "revise",
        "actor": None,
        "topic": "PostgreSQL",
        "subtopic": "indexing",
        "object": "indexing strategies",
        "temporal_text": "tomorrow",
        "urgency": "high",
        "confidence": 0.95
    }
    normalized = extraction_service._normalize(raw_data, "source text")
    assert normalized["intent_type"] == "study"
    assert normalized["urgency"] == "high"
    assert normalized["confidence"] == 0.95
    assert normalized["topic"] == "PostgreSQL"
    assert normalized["subtopic"] == "indexing"


def test_intent_validation_repair_and_clamping(extraction_service):
    # Invalid values should be clamped or auto-repaired
    raw_data = {
        "intent_type": "learn",        # Synonym of 'study'
        "action": "revise",
        "actor": "me",                 # Self-reference should be cleared
        "topic": "A" * 150,            # Should be truncated to 120 chars
        "urgency": "super_urgent",     # Invalid, should default to medium
        "confidence": 12.5             # Out of range, should clamp to 1.0
    }
    normalized = extraction_service._normalize(raw_data, "source text")
    assert normalized["intent_type"] == "study"
    assert normalized["actor"] is None
    assert normalized["urgency"] == "medium"
    assert normalized["confidence"] == 1.0
    assert len(normalized["topic"]) == 120


def test_invisible_unicode_and_untrusted_types(extraction_service):
    # Dicts, lists, and invisible Unicode should be stripped/rejected
    raw_data = {
        "intent_type": "todo",
        "action": {"type": "verb", "value": "buy"},  # Dict value rejected
        "actor": "Sid\u200b",                         # Zero-width space stripped
        "object": ["groceries", "milk"],             # List value rejected
        "urgency": "low",
        "confidence": 0.8
    }
    normalized = extraction_service._normalize(raw_data, "todo")
    assert normalized["action"] is None
    assert normalized["actor"] == "Sid"
    assert normalized["object"] is None


# ---------------------------------------------------------------------------
# Test category name generation (Part 3)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "intent,expected_name",
    [
        # Communication
        ({"intent_type": "communication", "actor": "Sid"}, "Communication - Sid"),
        ({"intent_type": "communication", "topic": "internship"}, "Communication - Internship"),
        ({"intent_type": "communication"}, "Communication"),
        # Study
        ({"intent_type": "study", "topic": "PostgreSQL"}, "Study - PostgreSQL"),
        ({"intent_type": "study"}, "Study"),
        # Reference
        ({"intent_type": "reference", "topic": "Docker Containers"}, "Reference - Docker Containers"),
        ({"intent_type": "reference"}, "Reference"),
        # Ideas
        ({"intent_type": "idea", "topic": "AI Resume Reviewer"}, "Ideas - AI Resume"),
        ({"intent_type": "idea"}, "Ideas"),
        # Todo mapping to buckets
        ({"intent_type": "todo", "topic": "groceries", "action": "buy"}, "Shopping"),
        ({"intent_type": "todo", "topic": "rent", "action": "pay"}, "Bills"),
        ({"intent_type": "todo", "topic": "doctor appointment"}, "Appointments"),
        ({"intent_type": "todo", "topic": "pickup package"}, "Errands"),
        ({"intent_type": "todo", "topic": "medicine"}, "Health"),
        ({"intent_type": "todo", "topic": "stocks"}, "Finance"),
        ({"intent_type": "todo", "topic": "flight ticket"}, "Travel"),
        # Todo default
        ({"intent_type": "todo", "topic": "random task"}, "Tasks"),
        # Reminder
        ({"intent_type": "reminder", "topic": "medication"}, "Appointments"),
        ({"intent_type": "reminder"}, "Reminders"),
        # Question
        ({"intent_type": "question", "topic": "Kafka partitions"}, "Questions - Kafka Partitions"),
        ({"intent_type": "question"}, "Questions"),
        # Event
        ({"intent_type": "event", "actor": "Professor"}, "Meetings - Professor"),
        ({"intent_type": "event"}, "Meetings"),
        # General
        ({"intent_type": "general", "topic": "Quantum Computing"}, "Quantum Computing"),
        ({"intent_type": "general"}, "General"),
    ]
)
def test_category_naming_rules(category_service, intent, expected_name):
    generated = category_service._generate_category_name(intent)
    assert generated == expected_name


def test_category_naming_four_word_limit(category_service):
    # Names must be strictly <= 4 words
    intent = {
        "intent_type": "study",
        "topic": "PostgreSQL Query Optimization and Indexing Strategies"
    }
    generated = category_service._generate_category_name(intent)
    assert len(generated.split()) <= 4
    # Re-verify that it's truncated cleanly
    assert generated == "Study - PostgreSQL Query"


# ---------------------------------------------------------------------------
# Test fast intent classifier (Part 6)
# ---------------------------------------------------------------------------

def test_fast_classifier_communication_and_actor(extraction_service):
    # Communication intent & actor extraction
    query = "things to tell Sid about the internship"
    result = extraction_service.extract_query_intent_fast(query)
    assert result["intent_type"] == "communication"
    assert result["actor"] == "Sid"
    assert result["topic"] == "internship"


def test_fast_classifier_avoid_false_actor(extraction_service):
    # General words like "team", "project", "everyone" shouldn't be actors
    query = "discuss with the team about project progress"
    result = extraction_service.extract_query_intent_fast(query)
    assert result["intent_type"] == "communication"
    assert result["actor"] is None
    assert result["topic"] == "team project progress"


def test_fast_classifier_study_and_todo(extraction_service):
    # Study query
    query = "study graph algorithms"
    result = extraction_service.extract_query_intent_fast(query)
    assert result["intent_type"] == "study"
    assert result["topic"] == "graph algorithms"

    # Todo query
    query = "buy bread and milk"
    result = extraction_service.extract_query_intent_fast(query)
    assert result["intent_type"] == "todo"
    assert result["topic"] == "bread milk"


# ---------------------------------------------------------------------------
# Test category reuse compatibility (Part 4)
# ---------------------------------------------------------------------------

def test_category_reuse_compatibility(category_service):
    from app.models.intent_category import IntentCategory

    # Case 1: Same intent type, same actor/no actor -> compatible
    cat = IntentCategory(intent_type="study", actor=None)
    intent = {"intent_type": "study", "actor": None}
    assert category_service._compatible(cat, intent) is True

    # Case 2: Different intent type -> incompatible
    cat = IntentCategory(intent_type="study", actor=None)
    intent = {"intent_type": "reference", "actor": None}
    assert category_service._compatible(cat, intent) is False

    # Case 3: Same intent type, one has actor, other doesn't -> incompatible
    cat = IntentCategory(intent_type="communication", actor="Sid")
    intent = {"intent_type": "communication", "actor": None}
    assert category_service._compatible(cat, intent) is False

    # Case 4: Same intent type, different actors -> incompatible
    cat = IntentCategory(intent_type="communication", actor="Sid")
    intent = {"intent_type": "communication", "actor": "Mom"}
    assert category_service._compatible(cat, intent) is False

    # Case 5: Same intent type, no actor, different topics -> incompatible
    cat = IntentCategory(intent_type="study", name="Study - PostgreSQL", actor=None)
    intent = {"intent_type": "study", "topic": "Docker", "actor": None}
    assert category_service._compatible(cat, intent) is False

    # Case 6: Same intent type, no actor, same topics but different phrasing/aliases -> compatible
    cat = IntentCategory(intent_type="study", name="Study - PostgreSQL", actor=None)
    intent = {"intent_type": "study", "topic": "postgres", "actor": None}
    assert category_service._compatible(cat, intent) is True
