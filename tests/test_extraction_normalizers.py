"""
Sprint 1 hardening — direct unit tests for the six previously untested
validators and helpers in IntentExtractionService.

All tests are pure Python: no database, no network, no LLM.
Covered:  _strip_safe, _validate_urgency, _validate_confidence,
          _validate_intent_type, _parse_due_date, _is_weak_object,
          _clean_token, _clean_short_text.
"""
from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.services.intent_extraction_service import (
    IntentExtractionService,
    INTENT_TYPE_SYNONYMS,
    VALID_INTENT_TYPES,
    VALID_URGENCY,
)


@pytest.fixture
def svc():
    return IntentExtractionService()


# ---------------------------------------------------------------------------
# _strip_safe
# ---------------------------------------------------------------------------

class TestStripSafe:
    def test_none_returns_none(self):
        assert IntentExtractionService._strip_safe(None) is None

    def test_dict_returns_none(self):
        assert IntentExtractionService._strip_safe({"a": 1}) is None

    def test_list_returns_none(self):
        assert IntentExtractionService._strip_safe([1, 2]) is None

    def test_empty_string_returns_none(self):
        assert IntentExtractionService._strip_safe("") is None

    def test_whitespace_only_returns_none(self):
        assert IntentExtractionService._strip_safe("   ") is None

    def test_null_synonym_returns_none(self):
        assert IntentExtractionService._strip_safe("null") is None
        assert IntentExtractionService._strip_safe("none") is None
        assert IntentExtractionService._strip_safe("n/a") is None
        assert IntentExtractionService._strip_safe("NULL") is None

    def test_strips_leading_trailing_whitespace(self):
        assert IntentExtractionService._strip_safe("  hello  ") == "hello"

    def test_int_converted_to_string(self):
        assert IntentExtractionService._strip_safe(42) == "42"

    def test_float_converted_to_string(self):
        assert IntentExtractionService._strip_safe(3.14) == "3.14"

    def test_removes_zero_width_space(self):
        # U+200B is zero-width space (category Cf)
        assert IntentExtractionService._strip_safe("hello​world") == "helloworld"

    def test_normal_string_passes_through(self):
        assert IntentExtractionService._strip_safe("PostgreSQL") == "PostgreSQL"

    def test_multiword_string_preserved(self):
        assert IntentExtractionService._strip_safe("System Design") == "System Design"


# ---------------------------------------------------------------------------
# _validate_urgency
# ---------------------------------------------------------------------------

class TestValidateUrgency:
    @pytest.mark.parametrize("val", ["low", "medium", "high"])
    def test_valid_values_pass(self, svc, val):
        assert svc._validate_urgency(val, []) == val

    def test_none_defaults_to_medium(self, svc):
        repairs = []
        assert svc._validate_urgency(None, []) == "medium"
        assert len(repairs) == 0  # no repair logged when no list provided

    def test_none_repair_logged(self, svc):
        repairs = []
        svc._validate_urgency(None, repairs)
        assert any("urgency=None" in r for r in repairs)

    def test_fuzzy_high_match(self, svc):
        repairs = []
        result = svc._validate_urgency("urgency_high", repairs)
        assert result == "high"
        assert any("fuzzy" in r for r in repairs)

    def test_fuzzy_low_match(self, svc):
        result = svc._validate_urgency("very_low", [])
        assert result == "low"

    def test_fuzzy_medium_match(self, svc):
        result = svc._validate_urgency("medium_priority", [])
        assert result == "medium"

    def test_unknown_defaults_to_medium(self, svc):
        repairs = []
        result = svc._validate_urgency("extreme", repairs)
        assert result == "medium"
        assert any("unknown" in r for r in repairs)

    def test_uppercase_valid(self, svc):
        # Lowercased before comparison
        assert svc._validate_urgency("HIGH", []) == "high"

    def test_dict_input_defaults_to_medium(self, svc):
        # dict/list stripped to None by _strip_safe
        result = svc._validate_urgency({"level": "high"}, [])
        assert result == "medium"


# ---------------------------------------------------------------------------
# _validate_confidence
# ---------------------------------------------------------------------------

class TestValidateConfidence:
    def test_float_in_range_passes(self, svc):
        assert svc._validate_confidence(0.85, []) == 0.85

    def test_string_float_parsed(self, svc):
        assert svc._validate_confidence("0.72", []) == 0.72

    def test_int_zero_valid(self, svc):
        assert svc._validate_confidence(0, []) == 0.0

    def test_int_one_valid(self, svc):
        assert svc._validate_confidence(1, []) == 1.0

    def test_above_one_clamped(self, svc):
        repairs = []
        result = svc._validate_confidence(1.5, repairs)
        assert result == 1.0
        assert any("clamped" in r for r in repairs)

    def test_below_zero_clamped(self, svc):
        repairs = []
        result = svc._validate_confidence(-0.1, repairs)
        assert result == 0.0
        assert any("clamped" in r for r in repairs)

    def test_none_defaults_to_half(self, svc):
        repairs = []
        result = svc._validate_confidence(None, repairs)
        assert result == 0.5
        assert any("unparseable" in r for r in repairs)

    def test_unparseable_string_defaults_to_half(self, svc):
        repairs = []
        result = svc._validate_confidence("high", repairs)
        assert result == 0.5
        assert any("unparseable" in r for r in repairs)

    def test_result_rounded_to_4dp(self, svc):
        result = svc._validate_confidence(0.123456789, [])
        assert result == round(0.123456789, 4)

    def test_dict_defaults_to_half(self, svc):
        result = svc._validate_confidence({"score": 0.9}, [])
        assert result == 0.5


# ---------------------------------------------------------------------------
# _validate_intent_type
# ---------------------------------------------------------------------------

class TestValidateIntentType:
    @pytest.mark.parametrize("val", sorted(VALID_INTENT_TYPES))
    def test_all_valid_types_pass(self, svc, val):
        assert svc._validate_intent_type(val, []) == val

    def test_none_becomes_general(self, svc):
        repairs = []
        result = svc._validate_intent_type(None, repairs)
        assert result == "general"
        assert any("intent_type=None" in r for r in repairs)

    def test_unknown_becomes_general(self, svc):
        repairs = []
        result = svc._validate_intent_type("xyz_unknown", repairs)
        assert result == "general"
        assert any("unknown" in r for r in repairs)

    @pytest.mark.parametrize("synonym, expected", list(INTENT_TYPE_SYNONYMS.items())[:6])
    def test_synonym_mapped(self, svc, synonym, expected):
        repairs = []
        result = svc._validate_intent_type(synonym, repairs)
        assert result == expected
        assert any("synonym" in r for r in repairs)

    def test_task_synonym_maps_to_todo(self, svc):
        assert svc._validate_intent_type("task", []) == "todo"

    def test_email_synonym_maps_to_communication(self, svc):
        assert svc._validate_intent_type("email", []) == "communication"

    def test_note_synonym_maps_to_general(self, svc):
        assert svc._validate_intent_type("note", []) == "general"

    def test_uppercased_valid_type(self, svc):
        # _strip_safe keeps case; lowered comparison handles it
        assert svc._validate_intent_type("STUDY", []) == "study"

    def test_dict_value_becomes_general(self, svc):
        result = svc._validate_intent_type({"type": "study"}, [])
        assert result == "general"


# ---------------------------------------------------------------------------
# _parse_due_date
# ---------------------------------------------------------------------------

class TestParseDueDate:
    def test_none_returns_none(self, svc):
        assert svc._parse_due_date(None) is None

    def test_empty_string_returns_none(self, svc):
        assert svc._parse_due_date("") is None

    def test_valid_iso_string(self, svc):
        result = svc._parse_due_date("2026-08-15")
        assert result == date(2026, 8, 15)

    def test_date_object_passes_through(self, svc):
        d = date(2026, 12, 25)
        assert svc._parse_due_date(d) == d

    def test_invalid_format_returns_none(self, svc):
        assert svc._parse_due_date("15-08-2026") is None
        assert svc._parse_due_date("August 15") is None
        assert svc._parse_due_date("not a date") is None

    def test_partial_date_returns_none(self, svc):
        assert svc._parse_due_date("2026-08") is None

    def test_numeric_zero_returns_none(self, svc):
        assert svc._parse_due_date(0) is None

    def test_future_date_valid(self, svc):
        future = (date.today() + timedelta(days=30)).isoformat()
        result = svc._parse_due_date(future)
        assert result == date.today() + timedelta(days=30)


# ---------------------------------------------------------------------------
# _is_weak_object
# ---------------------------------------------------------------------------

class TestIsWeakObject:
    def test_none_is_weak(self, svc):
        assert svc._is_weak_object(None, "todo") is True

    def test_empty_string_is_weak(self, svc):
        assert svc._is_weak_object("", "todo") is True

    def test_generic_word_is_weak(self, svc):
        for w in ["general", "study", "task", "note", "thing"]:
            assert svc._is_weak_object(w, "todo") is True, f"{w!r} should be weak"

    def test_intent_type_as_object_is_weak(self, svc):
        assert svc._is_weak_object("todo", "todo") is True
        assert svc._is_weak_object("study", "study") is True

    def test_too_short_is_weak(self, svc):
        assert svc._is_weak_object("ab", "todo") is True
        assert svc._is_weak_object("x", "todo") is True

    def test_three_char_is_not_weak(self, svc):
        assert svc._is_weak_object("API", "todo") is False

    def test_substantive_object_not_weak(self, svc):
        assert svc._is_weak_object("PostgreSQL migration script", "study") is False
        assert svc._is_weak_object("groceries", "todo") is False
        assert svc._is_weak_object("internship offer", "communication") is False


# ---------------------------------------------------------------------------
# _clean_token (used for the action field)
# ---------------------------------------------------------------------------

class TestCleanToken:
    def test_none_returns_none(self, svc):
        assert svc._clean_token(None, 80, "action", []) is None

    def test_empty_returns_none(self, svc):
        assert svc._clean_token("", 80, "action", []) is None

    def test_valid_token_lowercased(self, svc):
        assert svc._clean_token("Tell", 80, "action", []) == "tell"

    def test_truncated_at_max_len(self, svc):
        repairs = []
        long_val = "a" * 100
        result = svc._clean_token(long_val, 80, "action", repairs)
        assert len(result) == 80
        assert any("truncated" in r for r in repairs)

    def test_dict_returns_none(self, svc):
        assert svc._clean_token({"action": "tell"}, 80, "action", []) is None


# ---------------------------------------------------------------------------
# _clean_short_text (used for object, subtopic, temporal_text)
# ---------------------------------------------------------------------------

class TestCleanShortText:
    def test_none_returns_none(self, svc):
        assert svc._clean_short_text(None, 255, "object", []) is None

    def test_valid_text_passes(self, svc):
        assert svc._clean_short_text("internship offer", 255, "object", []) == "internship offer"

    def test_truncated_at_max_len(self, svc):
        repairs = []
        long_val = "x" * 300
        result = svc._clean_short_text(long_val, 255, "object", repairs)
        assert len(result) == 255
        assert any("truncated" in r for r in repairs)

    def test_preserves_capitalisation(self, svc):
        assert svc._clean_short_text("PostgreSQL Indexing", 255, "subtopic", []) == "PostgreSQL Indexing"

    def test_dict_returns_none(self, svc):
        assert svc._clean_short_text({"key": "val"}, 255, "object", []) is None

    def test_empty_string_returns_none(self, svc):
        assert svc._clean_short_text("", 255, "object", []) is None
