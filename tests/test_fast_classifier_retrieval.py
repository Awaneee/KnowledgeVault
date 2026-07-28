"""
EXTR-008 — Fast classifier retrieval-query vocabulary expansion tests.

All tests are pure Python: no database, no network, no embedding model.
Tests verify that newly added study/idea/reference keywords route correctly
AND that the priority reorder (event before reference) prevents false
positives on queries like "meeting notes".
"""
from __future__ import annotations

import pytest

from app.services.intent_extraction_service import IntentExtractionService


@pytest.fixture
def svc():
    return IntentExtractionService()


# ---------------------------------------------------------------------------
# Study vocabulary additions — EXTR-008
# ---------------------------------------------------------------------------

class TestStudyVocabularyAdditions:
    """Queries that were misclassified (as general/question) before EXTR-008."""

    @pytest.mark.parametrize("query", [
        "AI research notes",
        "Show my AI research reading goals",
        "security research findings",
        "my machine learning research",
    ])
    def test_research_routes_to_study(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "study", (
            f"{query!r} → expected 'study', got {result['intent_type']!r}"
        )

    @pytest.mark.parametrize("query", [
        "FastAPI tutorial",
        "Kubernetes tutorial for beginners",
        "Object oriented programming tutorial",
        "PostgreSQL tutorial",
    ])
    def test_tutorial_routes_to_study(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "study", (
            f"{query!r} → expected 'study', got {result['intent_type']!r}"
        )

    @pytest.mark.parametrize("query", [
        "Kubernetes tutorials",
        "system design tutorials",
        "Docker tutorials for beginners",
    ])
    def test_tutorials_plural_routes_to_study(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "study", (
            f"{query!r} → expected 'study', got {result['intent_type']!r}"
        )

    @pytest.mark.parametrize("query", [
        # Existing keywords must still work — regression guard
        "Study Docker networking",
        "Learn PostgreSQL indexing",
        "revise machine learning",
    ])
    def test_existing_study_keywords_unchanged(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "study", (
            f"Regression: {query!r} → expected 'study', got {result['intent_type']!r}"
        )


# ---------------------------------------------------------------------------
# Idea vocabulary additions — EXTR-008
# ---------------------------------------------------------------------------

class TestIdeaVocabularyAdditions:

    @pytest.mark.parametrize("query", [
        "Brainstorming app names",
        "Brainstorming session for the startup",
        "brainstorming product ideas",
    ])
    def test_brainstorming_routes_to_idea(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "idea", (
            f"{query!r} → expected 'idea', got {result['intent_type']!r}"
        )

    @pytest.mark.parametrize("query", [
        # Existing keywords must still work — regression guard
        "Startup idea for AI",
        "brainstorm product concepts",
        "new idea for a tool",
    ])
    def test_existing_idea_keywords_unchanged(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "idea", (
            f"Regression: {query!r} → expected 'idea', got {result['intent_type']!r}"
        )


# ---------------------------------------------------------------------------
# Reference vocabulary additions — EXTR-008
# ---------------------------------------------------------------------------

class TestReferenceVocabularyAdditions:

    @pytest.mark.parametrize("query", [
        "my Python notes",
        "PostgreSQL notes",
        "architecture notes",
        "Docker networking notes",
        "show my AI notes",
    ])
    def test_notes_routes_to_reference(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "reference", (
            f"{query!r} → expected 'reference', got {result['intent_type']!r}"
        )

    @pytest.mark.parametrize("query", [
        "Docker commands cheat sheet",
        "Redis cheat sheet",
        "Git cheat sheet",
    ])
    def test_cheat_sheet_routes_to_reference(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "reference", (
            f"{query!r} → expected 'reference', got {result['intent_type']!r}"
        )

    @pytest.mark.parametrize("query", [
        "Redis cheatsheet",
        "PostgreSQL cheatsheet",
        "Kubernetes cheatsheets",
    ])
    def test_cheatsheet_token_routes_to_reference(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "reference", (
            f"{query!r} → expected 'reference', got {result['intent_type']!r}"
        )

    @pytest.mark.parametrize("query", [
        "Docker resources",
        "AI ML resources",
        "AI resource",          # "machine learning resource" excluded: "learning" fires study first
    ])
    def test_resources_routes_to_reference(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "reference", (
            f"{query!r} → expected 'reference', got {result['intent_type']!r}"
        )

    @pytest.mark.parametrize("query", [
        "PostgreSQL guide",
        "FastAPI guide for beginners",
        "Kubernetes guides",
    ])
    def test_guide_routes_to_reference(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "reference", (
            f"{query!r} → expected 'reference', got {result['intent_type']!r}"
        )

    @pytest.mark.parametrize("query", [
        # Existing keywords must still work — regression guard
        "Reference docs for Docker",
        "Documentation about the API",
        "show references for PostgreSQL",
    ])
    def test_existing_reference_keywords_unchanged(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "reference", (
            f"Regression: {query!r} → expected 'reference', got {result['intent_type']!r}"
        )


# ---------------------------------------------------------------------------
# Priority reorder: event before reference — EXTR-008
#
# Adding "notes" to QUERY_REFERENCE_KEYWORDS would steal "meeting notes"
# (expected: event) if reference were still checked before event. The reorder
# prevents this. These tests are the primary regression guard for Change 4.
# ---------------------------------------------------------------------------

class TestEventPriorityOverReference:

    @pytest.mark.parametrize("query", [
        "Meeting notes",
        "meeting notes from today",
        "team meeting notes",
        "our weekly meeting notes",
    ])
    def test_meeting_notes_routes_to_event_not_reference(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "event", (
            f"{query!r} → expected 'event', got {result['intent_type']!r}\n"
            f"Priority reorder guard: 'meeting' (event) must beat 'notes' (reference)."
        )

    @pytest.mark.parametrize("query", [
        "weekly team meetings",
        "scheduled events for next week",
        "upcoming events",
        "meeting about PostgreSQL migration",
    ])
    def test_event_keywords_still_route_to_event(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "event", (
            f"Regression: {query!r} → expected 'event', got {result['intent_type']!r}"
        )


# ---------------------------------------------------------------------------
# Todo regression guard — pure todo queries are unaffected
# ---------------------------------------------------------------------------

class TestTodoRegressionGuard:
    """
    Verifies that adding new reference/study keywords did not accidentally
    introduce words that steal from clean todo queries (i.e. queries that
    contain no reference or study keywords).

    Note: reference (priority 6) correctly outranks todo (priority 7), so
    any query containing BOTH a reference keyword and a todo keyword will
    route to reference. That is correct behaviour, not a false positive.
    Queries tested here are pure todo — no reference or study keyword present.
    """

    @pytest.mark.parametrize("query", [
        "Deploy the service to production",   # deploy → todo; no reference keyword
        "Fix the authentication bug",         # fix → todo; no reference keyword
        "Buy groceries",                      # buy → todo; no reference keyword
        "Finish the report",                  # finish → todo; "report" not in reference
        "Ship the feature branch",            # ship → todo; no reference keyword
    ])
    def test_pure_todo_queries_still_route_to_todo(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "todo", (
            f"Regression: {query!r} → expected 'todo', got {result['intent_type']!r}"
        )


# ---------------------------------------------------------------------------
# Higher-priority groups still win over the new keywords
# ---------------------------------------------------------------------------

class TestHigherPriorityGroupsStillWinOverNewKeywords:
    """
    Each group above reference in the priority order must still fire first
    when its keywords are present, even if a new EXTR-008 reference keyword
    is also present.
    """

    @pytest.mark.parametrize("query, expected", [
        # study (priority 3) wins over "guide" (reference, priority 6)
        ("Study the PostgreSQL guide",          "study"),
        # study (priority 3) wins over "notes" (reference, priority 6)
        ("Study notes on Docker",               "study"),
        # study (priority 3) wins over "tutorial" — "learn" triggers study
        ("Learn from the FastAPI tutorial",     "study"),
        # idea (priority 4) wins over "notes" (reference, priority 6)
        ("Ideas and brainstorming notes",       "idea"),
        # reminder (priority 2) wins over "notes" (reference, priority 6)
        ("Remind me to review my notes",        "reminder"),
        # communication (priority 1) wins over "notes" (reference, priority 6)
        ("Email Sid my cheatsheet notes",       "communication"),
    ])
    def test_higher_priority_wins(self, svc, query, expected):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == expected, (
            f"{query!r} → expected {expected!r}, got {result['intent_type']!r}"
        )
