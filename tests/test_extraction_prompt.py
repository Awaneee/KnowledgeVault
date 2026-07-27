"""
EXTR-004 — Prompt v3 structure tests.

All tests are pure Python: no LLM call, no database, no network.
These tests verify the prompt contains the required rules and examples;
they do not test LLM output quality (which requires a live Gemini call).
"""
from __future__ import annotations

from datetime import date

import pytest

from app.services.intent_extraction_service import IntentExtractionService


@pytest.fixture
def svc():
    return IntentExtractionService()


@pytest.fixture
def prompt(svc):
    return svc._build_prompt("test note")


@pytest.fixture
def query_prompt(svc):
    return svc._build_prompt("test query", is_query=True)


# ---------------------------------------------------------------------------
# Version
# ---------------------------------------------------------------------------

class TestPromptVersion:
    def test_version_is_v3(self):
        assert IntentExtractionService.PROMPT_VERSION == "intent-v3"


# ---------------------------------------------------------------------------
# Required fields present
# ---------------------------------------------------------------------------

class TestPromptFields:
    def test_all_nine_fields_defined(self, prompt):
        for field in [
            "intent_type", "action", "actor", "topic", "subtopic",
            "object", "temporal_text", "urgency", "confidence",
        ]:
            assert field in prompt, f"Field {field!r} missing from prompt"

    def test_all_intent_types_listed(self, prompt):
        for intent in [
            "communication", "todo", "study", "reminder", "idea",
            "reference", "question", "event", "general",
        ]:
            assert intent in prompt, f"Intent type {intent!r} missing from prompt"


# ---------------------------------------------------------------------------
# New rules added in v3
# ---------------------------------------------------------------------------

class TestPromptActorRule:
    def test_actor_must_be_human_name(self, prompt):
        assert "human person" in prompt or "given name or surname" in prompt

    def test_tech_terms_are_never_actors(self, prompt):
        assert "NEVER actors" in prompt

    def test_programming_languages_called_out(self, prompt):
        # "Python, Go" are named as examples of non-actors
        assert "Python" in prompt
        assert "Go" in prompt

    def test_generic_words_excluded_from_actor(self, prompt):
        assert "team" in prompt and "project" in prompt

    def test_actor_null_guidance(self, prompt):
        assert "no human name" in prompt or "actor to null" in prompt


class TestPromptTopicRule:
    def test_stop_word_prohibition_present(self, prompt):
        assert "NEVER return" in prompt

    def test_bad_topic_examples_present(self, prompt):
        # Spec requires these specific BAD examples
        assert '"The"' in prompt
        assert '"But"' in prompt
        assert '"Also"' in prompt
        assert '"Used"' in prompt

    def test_good_topic_examples_present(self, prompt):
        assert '"PostgreSQL"' in prompt
        assert '"Flutter"' in prompt

    def test_null_guidance_present(self, prompt):
        assert "null is always better" in prompt

    def test_code_note_guidance_present(self, prompt):
        assert "function name" in prompt
        assert "built-in" in prompt


# ---------------------------------------------------------------------------
# Date injection
# ---------------------------------------------------------------------------

class TestPromptDateInjection:
    def test_current_date_injected(self, prompt):
        assert date.today().isoformat() in prompt


# ---------------------------------------------------------------------------
# Note vs query mode
# ---------------------------------------------------------------------------

class TestPromptInputType:
    def test_note_mode_says_note(self, prompt):
        assert "Input type: note" in prompt

    def test_query_mode_says_query(self, query_prompt):
        assert "Input type: query" in query_prompt

    def test_input_text_injected(self, svc):
        p = svc._build_prompt("my specific input text")
        assert "my specific input text" in p


# ---------------------------------------------------------------------------
# Examples count and content
# ---------------------------------------------------------------------------

class TestPromptExamples:
    def test_nine_examples_present(self, prompt):
        # Each example starts with "→ {" on its own line
        assert prompt.count("→ {") >= 9

    def test_code_example_present(self, prompt):
        # New in v3: code-dump example teaching Python as topic
        assert "def reduce_list" in prompt

    def test_stop_word_example_present(self, prompt):
        # New in v3: fragment example teaching topic:null
        assert "threading approach" in prompt or "race conditions" in prompt

    def test_team_communication_example_present(self, prompt):
        # New in v3: no-actor example for team communication
        assert "backend team" in prompt

    def test_cross_encoder_example_present(self, prompt):
        # New in v3: multi-word technical topic example
        assert "Cross-encoder" in prompt or "cross-encoder" in prompt

    def test_original_tell_sid_example_preserved(self, prompt):
        assert '"actor":"Sid"' in prompt

    def test_original_buy_groceries_example_preserved(self, prompt):
        assert "groceries" in prompt

    def test_original_docker_example_preserved(self, prompt):
        assert "Docker container networking" in prompt

    def test_null_topic_example_in_stop_word_case(self, prompt):
        # The stop-word fragment example must have topic:null
        assert '"topic":null' in prompt


# ---------------------------------------------------------------------------
# Backward-compatible structure: JSON-only, no markdown
# ---------------------------------------------------------------------------

class TestPromptOutputFormat:
    def test_no_markdown_instruction_present(self, prompt):
        assert "No markdown" in prompt

    def test_json_only_instruction_present(self, prompt):
        assert "JSON only" in prompt

    def test_return_strict_json_present(self, prompt):
        assert "STRICT JSON" in prompt
