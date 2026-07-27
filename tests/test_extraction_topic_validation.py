"""
EXTR-002 — Topic validation layer tests.

All tests are pure Python: no database, no network, no embedding model.
"""
from __future__ import annotations

import pytest

from app.services.intent_extraction_service import IntentExtractionService


@pytest.fixture
def svc():
    return IntentExtractionService()


def _raw(topic=None, actor=None, intent_type="general"):
    return {
        "intent_type": intent_type,
        "action": None,
        "actor": actor,
        "topic": topic,
        "subtopic": None,
        "object": None,
        "temporal_text": None,
        "urgency": "medium",
        "confidence": 0.7,
        "_provider": "gemini",
    }


# ---------------------------------------------------------------------------
# Stop words
# ---------------------------------------------------------------------------

class TestValidateTopicStopWords:
    @pytest.mark.parametrize("bad", [
        "The", "the", "But", "And", "Also", "Just", "Well", "However",
        "Always", "Never", "Common", "Important", "Crucial", "Cross",
        "Based", "Used", "Given",
    ])
    def test_stop_word_rejected(self, svc, bad):
        assert svc._validate_topic(bad, []) is None

    def test_stop_word_repair_logged(self, svc):
        repairs = []
        svc._validate_topic("The", repairs)
        assert len(repairs) == 1
        assert "stop word" in repairs[0]

    def test_multi_word_starting_with_stop_word_rejected(self, svc):
        assert svc._validate_topic("The system design", []) is None

    def test_multi_word_not_starting_with_stop_word_passes(self, svc):
        # "System Design" — "system" is not a stop word
        assert svc._validate_topic("System Design", []) == "System Design"


# ---------------------------------------------------------------------------
# Weak verbs
# ---------------------------------------------------------------------------

class TestValidateTopicWeakVerbs:
    @pytest.mark.parametrize("bad", [
        "Added", "Changed", "Updated", "Deleted", "Fixed",
        "Booked", "Created", "Removed", "Modified",
        "added", "changed", "updated",
    ])
    def test_weak_verb_rejected(self, svc, bad):
        assert svc._validate_topic(bad, []) is None

    def test_weak_verb_repair_logged(self, svc):
        repairs = []
        svc._validate_topic("Added", repairs)
        assert any("weak verb" in r for r in repairs)


# ---------------------------------------------------------------------------
# Question fragments
# ---------------------------------------------------------------------------

class TestValidateTopicQuestionFragments:
    @pytest.mark.parametrize("bad", [
        "Does Redis Eviction work",
        "What is the walrus operator",
        "How to set up Docker",
        "Is this correct",
        "Are these valid",
        "Can we use this",
        "Will this work",
    ])
    def test_question_fragment_rejected(self, svc, bad):
        assert svc._validate_topic(bad, []) is None

    def test_question_repair_logged(self, svc):
        # "What is the walrus operator" — first word "what" is in
        # _TOPIC_QUESTION_STARTS only, so the repair message is unambiguous.
        repairs = []
        svc._validate_topic("What is the walrus operator", repairs)
        assert any("question fragment" in r for r in repairs)


# ---------------------------------------------------------------------------
# Python tokens
# ---------------------------------------------------------------------------

class TestValidateTopicPythonTokens:
    @pytest.mark.parametrize("bad", [
        "print", "reduce", "map", "filter", "id",
        "for", "class", "return", "if", "while",
    ])
    def test_python_token_rejected(self, svc, bad):
        assert svc._validate_topic(bad, []) is None


# ---------------------------------------------------------------------------
# Trailing punctuation stripped
# ---------------------------------------------------------------------------

class TestValidateTopicPunctuation:
    def test_trailing_period_stripped(self, svc):
        result = svc._validate_topic("Flutter Application Performance.", [])
        assert result == "Flutter Application Performance"

    def test_trailing_comma_stripped(self, svc):
        assert svc._validate_topic("Docker,", []) == "Docker"

    def test_trailing_semicolon_stripped(self, svc):
        assert svc._validate_topic("Redis;", []) == "Redis"

    def test_punct_only_returns_none(self, svc):
        assert svc._validate_topic("...", []) is None

    def test_punct_strip_logged(self, svc):
        repairs = []
        svc._validate_topic("Flutter Application Performance.", repairs)
        assert any("punct stripped" in r for r in repairs)


# ---------------------------------------------------------------------------
# Short-token guard
# ---------------------------------------------------------------------------

class TestValidateTopicShortTokens:
    def test_two_char_non_acronym_rejected(self, svc):
        # "rs" is not in _TOPIC_SHORT_ACRONYMS
        assert svc._validate_topic("rs", []) is None

    def test_single_char_rejected(self, svc):
        assert svc._validate_topic("x", []) is None

    @pytest.mark.parametrize("acronym", [
        "AI", "ai", "API", "api", "Go", "go", "ML", "ml",
        "SQL", "sql", "UI", "ui", "AWS", "aws",
    ])
    def test_known_acronym_passes(self, svc, acronym):
        assert svc._validate_topic(acronym, []) is not None


# ---------------------------------------------------------------------------
# Valid inputs pass through unchanged
# ---------------------------------------------------------------------------

class TestValidateTopicValidInputs:
    @pytest.mark.parametrize("good, expected", [
        ("PostgreSQL", "PostgreSQL"),
        ("Flutter", "Flutter"),
        ("System Design", "System Design"),
        ("AI", "AI"),
        ("Go", "Go"),
        ("SQL", "SQL"),
        ("Cross-encoder Reranking", "Cross-encoder Reranking"),
        ("Knowledge Retrieval", "Knowledge Retrieval"),
        ("JWT Authentication", "JWT Authentication"),
        ("Graph Algorithms", "Graph Algorithms"),
        ("Machine Learning", "Machine Learning"),
    ])
    def test_valid_topic_passes_unchanged(self, svc, good, expected):
        assert svc._validate_topic(good, []) == expected

    def test_none_input_returns_none(self, svc):
        assert svc._validate_topic(None, []) is None

    def test_empty_string_returns_none(self, svc):
        assert svc._validate_topic("", []) is None

    def test_null_string_returns_none(self, svc):
        assert svc._validate_topic("null", []) is None

    def test_none_string_returns_none(self, svc):
        assert svc._validate_topic("none", []) is None


# ---------------------------------------------------------------------------
# Integration: _normalize() uses _validate_topic for topic field
# ---------------------------------------------------------------------------

class TestValidateTopicInNormalize:
    def test_stop_word_topic_nulled(self, svc):
        result = svc._normalize(_raw(topic="But"), "But this is interesting")
        assert result["topic"] is None

    def test_trailing_period_stripped_in_normalize(self, svc):
        result = svc._normalize(
            _raw(topic="Flutter Application Performance."),
            "Flutter Application Performance."
        )
        assert result["topic"] == "Flutter Application Performance"

    def test_valid_topic_preserved_in_normalize(self, svc):
        assert svc._normalize(_raw(topic="PostgreSQL"), "PostgreSQL notes")["topic"] == "PostgreSQL"

    def test_question_fragment_nulled_in_normalize(self, svc):
        result = svc._normalize(_raw(topic="Does Redis Eviction"), "")
        assert result["topic"] is None

    def test_python_builtin_nulled_in_normalize(self, svc):
        result = svc._normalize(_raw(topic="reduce"), "reduce function")
        assert result["topic"] is None

    def test_rescue_still_works_with_validate_topic(self, svc):
        # Tech actor "Python" is rescued as topic via _validate_topic
        raw = _raw(actor="Python", topic=None, intent_type="communication")
        result = svc._normalize(raw, "Python migration discussion")
        assert result["actor"] is None
        assert result["topic"] == "Python"  # TECH_MAP value passes _validate_topic


# ---------------------------------------------------------------------------
# Rule-based fallback: _extract_with_rules() must not emit garbage topics
# ---------------------------------------------------------------------------

class TestRuleBasedFallbackTopicValidation:
    def test_stop_word_capitalized_not_used_as_topic(self, svc):
        # "Also" is a capitalized word that the old code would pick up.
        result = svc._extract_with_rules("Also the endpoint returns a 422 error")
        assert result["topic"] not in {"Also", "The", "Endpoint"}

    def test_tech_term_in_rule_fallback_still_works(self, svc):
        # TECH_MAP scan runs before capitalized-word scan; Redis is valid.
        result = svc._extract_with_rules("Also check the Redis configuration")
        assert result["topic"] == "Redis"

    def test_valid_capitalized_topic_still_extracted(self, svc):
        # "Kubernetes" is a valid topic and passes _validate_topic.
        result = svc._extract_with_rules("Need to study Kubernetes networking")
        assert result["topic"] == "Kubernetes"

    def test_weak_verb_capitalized_not_used_as_topic(self, svc):
        result = svc._extract_with_rules("Updated the migration scripts today")
        assert result["topic"] != "Updated"

    def test_none_topic_when_no_valid_capitalized_word(self, svc):
        # All caps words are stop words / weak verbs; topic should be None.
        result = svc._extract_with_rules("Also added some changes here")
        assert result["topic"] is None
