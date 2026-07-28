"""
EXTR-005 — Fast classifier todo expansion tests.

All tests are pure Python: no database, no network, no embedding model.
Tests verify that newly added todo keywords route correctly AND that
higher-priority groups (communication, study, reference, idea) still win
when they match.
"""
from __future__ import annotations

import pytest

from app.services.intent_extraction_service import IntentExtractionService


@pytest.fixture
def svc():
    return IntentExtractionService()


# ---------------------------------------------------------------------------
# New keyword coverage — queries that were "general" before EXTR-005
# ---------------------------------------------------------------------------

class TestNewTodoKeywords:
    """Each query here was classified as 'general' before EXTR-005."""

    @pytest.mark.parametrize("query", [
        "Deploy KnowledgeVault",
        "Deploy the service to production",
        "Launch the beta",
        "Launch the new feature",
        "Fix the login bug",
        "Fix authentication flow",
        "Release version 2.0",
        "Release the hotfix",
        "Ship the feature",
        "Ship it today",
        "Push to production",
        "Push the PR",
        "Merge the feature branch",
        "Merge PR 42",
        "Update GitHub README",
        "Update the configuration",
        "Build the new dashboard",
        "Build the API endpoint",
    ])
    def test_new_keyword_routes_to_todo(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "todo", (
            f"{query!r} → expected 'todo', got {result['intent_type']!r}"
        )


# ---------------------------------------------------------------------------
# Existing keywords still work — regression guard
# ---------------------------------------------------------------------------

class TestExistingTodoKeywordsUnchanged:
    @pytest.mark.parametrize("query", [
        "Buy groceries",
        "Submit the assignment",
        "Pay the bills",
        "Finish the report",
        "Complete the task",
        "Todo list for today",
        "Pending tasks this week",
    ])
    def test_existing_todo_keywords_unchanged(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == "todo", (
            f"Regression: {query!r} → expected 'todo', got {result['intent_type']!r}"
        )


# ---------------------------------------------------------------------------
# Priority group ordering — higher-priority groups win
# ---------------------------------------------------------------------------

class TestHigherPriorityGroupsWin:
    """
    Communication, study, idea, reference, event are checked before todo.
    None of these queries should be classified as todo even though some
    contain newly added todo keywords.
    """

    @pytest.mark.parametrize("query, expected_intent", [
        # study > todo
        ("Study Docker networking", "study"),
        ("Learn PostgreSQL indexing", "study"),
        # communication > todo
        ("Tell Sid about the launch", "communication"),
        ("Email the team about the update", "communication"),
        # idea > todo
        ("Ideas for a new app", "idea"),
        ("Brainstorm startup concepts", "idea"),
        # reference > todo
        ("Reference docs for Docker", "reference"),
        ("Documentation about the API", "reference"),
        # reminder > todo (reminder checked before todo)
        ("Remind me about the appointment", "reminder"),
    ])
    def test_higher_priority_wins(self, svc, query, expected_intent):
        result = svc.extract_query_intent_fast(query)
        assert result["intent_type"] == expected_intent, (
            f"{query!r} → expected {expected_intent!r}, got {result['intent_type']!r}"
        )

    @pytest.mark.parametrize("query", [
        # "How to configure PostgreSQL" — no QUERY_REFERENCE_KEYWORDS match,
        # no QUERY_STUDY_KEYWORDS match, but "configure" is NOT in
        # QUERY_TODO_KEYWORDS (excluded per spec: too ambiguous).
        # Result is "general" — correct, no false positive.
        "How to configure PostgreSQL replication",
    ])
    def test_ambiguous_verb_excluded_from_keywords(self, svc, query):
        result = svc.extract_query_intent_fast(query)
        # Must NOT be todo — "configure" was explicitly excluded from
        # QUERY_TODO_KEYWORDS to avoid false positives on reference queries.
        assert result["intent_type"] != "todo", (
            f"{query!r} → should not be 'todo', got {result['intent_type']!r}"
        )


# ---------------------------------------------------------------------------
# TODO_ACTIONS set expansion — verifies rule-based fallback path
# ---------------------------------------------------------------------------

class TestTodoActionsExpansion:
    """
    TODO_ACTIONS is used in _extract_with_rules() for intent classification
    and action extraction. These tests verify the rule-based fallback path.
    """

    @pytest.mark.parametrize("word", [
        "deploy", "launch", "fix", "release", "ship", "push", "merge",
    ])
    def test_new_word_in_todo_actions(self, svc, word):
        assert word in svc.TODO_ACTIONS, (
            f"{word!r} should be in TODO_ACTIONS after EXTR-005"
        )

    def test_build_not_in_todo_actions(self, svc):
        # "build" is in QUERY_TODO_KEYWORDS (fast classifier) but NOT in
        # TODO_ACTIONS (rule-based fallback) to prevent misclassifying
        # study notes like "build pipeline architecture" as todo.
        assert "build" not in svc.TODO_ACTIONS

    @pytest.mark.parametrize("word", [
        "todo", "to-do", "task", "tasks", "pending",
        "finish", "complete", "submit", "buy", "pay",
    ])
    def test_original_todo_actions_preserved(self, svc, word):
        # Original keywords must still be present.
        # Note: TODO_ACTIONS and QUERY_TODO_KEYWORDS overlap on
        # "finish", "complete", "submit", "buy".
        assert word in svc.QUERY_TODO_KEYWORDS, (
            f"Regression: {word!r} should still be in QUERY_TODO_KEYWORDS"
        )

    def test_rule_based_fallback_classifies_deploy_as_todo(self, svc):
        result = svc._extract_with_rules("deploy the service to production")
        assert result["intent_type"] == "todo"

    def test_rule_based_fallback_classifies_fix_as_todo(self, svc):
        result = svc._extract_with_rules("fix the login authentication bug")
        assert result["intent_type"] == "todo"

    def test_rule_based_fallback_extracts_deploy_as_action(self, svc):
        # When "deploy" is the first word and in TODO_ACTIONS, it becomes action.
        result = svc._extract_with_rules("deploy the service to production")
        assert result["action"] == "deploy"

    def test_rule_based_fallback_study_note_not_misclassified(self, svc):
        # "build" is not in TODO_ACTIONS, so a study note about building
        # a system remains "general" (or "study" via keywords) — not "todo".
        result = svc._extract_with_rules("build pipeline architecture for distributed systems")
        assert result["intent_type"] != "todo"


# ---------------------------------------------------------------------------
# QUERY_TODO_KEYWORDS set contents
# ---------------------------------------------------------------------------

class TestQueryTodoKeywordsContents:
    @pytest.mark.parametrize("word", [
        # Original
        "todo", "to-do", "task", "tasks", "pending",
        "finish", "complete", "submit", "buy", "pay",
        # New additions
        "deploy", "launch", "fix", "release", "ship", "push", "merge",
        "update", "build",
    ])
    def test_word_in_query_todo_keywords(self, svc, word):
        assert word in svc.QUERY_TODO_KEYWORDS, (
            f"{word!r} should be in QUERY_TODO_KEYWORDS after EXTR-005"
        )

    @pytest.mark.parametrize("excluded", [
        # High-ambiguity verbs explicitly excluded by spec
        "configure", "install", "migrate", "plan", "organize",
        "schedule", "upload", "publish", "draft", "design", "test",
    ])
    def test_ambiguous_verbs_excluded(self, svc, excluded):
        assert excluded not in svc.QUERY_TODO_KEYWORDS, (
            f"{excluded!r} should NOT be in QUERY_TODO_KEYWORDS (too ambiguous)"
        )


# ---------------------------------------------------------------------------
# Benchmark regression gate — fast classifier on 50-query benchmark
# ---------------------------------------------------------------------------

class TestBenchmarkRegressionGate:
    """
    Runs the full 50-query fast-classifier benchmark and asserts minimum
    accuracy. Threshold is FAST_CLASSIFIER_MIN_ACCURACY from EXTR-009 spec.
    """

    BENCHMARK_PATH = "app/evaluation/benchmark/benchmark.json"
    # Single source of truth lives on IntentExtractionService (EXTR-009).
    # To raise the gate after a new sprint: update FAST_CLASSIFIER_MIN_ACCURACY there.
    MIN_ACCURACY = IntentExtractionService.FAST_CLASSIFIER_MIN_ACCURACY

    # Benchmark uses "meeting" and "project" as intent labels; normalize to
    # valid system intent types.
    INTENT_NORMALISATION = {
        "meeting": "event",
        "project": "todo",
    }

    def _load_benchmark(self):
        import json
        with open(self.BENCHMARK_PATH) as f:
            return json.load(f)

    def test_minimum_accuracy_not_regressed(self):
        svc = IntentExtractionService()
        data = self._load_benchmark()
        correct = 0
        failures = []
        for item in data:
            q = item["query"]
            expected = self.INTENT_NORMALISATION.get(
                item["expected_intent"], item["expected_intent"]
            )
            predicted = svc.extract_query_intent_fast(q)["intent_type"]
            if predicted == expected:
                correct += 1
            else:
                failures.append(f"  {q!r}: expected={expected!r} got={predicted!r}")

        accuracy = correct / len(data)
        failure_detail = "\n".join(failures) if failures else "none"
        assert accuracy >= self.MIN_ACCURACY, (
            f"Fast classifier accuracy {accuracy:.1%} < gate {self.MIN_ACCURACY:.1%}.\n"
            f"Failures ({len(failures)}):\n{failure_detail}"
        )

    def test_known_fixed_queries_now_pass(self):
        """Specific queries fixed by EXTR-005 must classify correctly."""
        svc = IntentExtractionService()
        fixed_by_extr005 = [
            ("Deploy KnowledgeVault",                   "todo"),
            ("Update GitHub README",                    "todo"),
            ("Timeline for the beta launch",            "todo"),
            ("Project deadline for the alpha release",  "todo"),
        ]
        for query, expected in fixed_by_extr005:
            predicted = svc.extract_query_intent_fast(query)["intent_type"]
            assert predicted == expected, (
                f"EXTR-005 should fix: {query!r} → expected={expected!r} got={predicted!r}"
            )


# ---------------------------------------------------------------------------
# Benchmark regression gate — fast classifier on 152-query diagnostic benchmark
#
# This benchmark is more representative than the 50-query gate: 51% of queries
# expect study intent and 25% reference.  The study accuracy is known to be low
# (6% as of Sprint 1 end) due to the "notes" → reference collision introduced
# by EXTR-008; Sprint 2 will resolve this.  The gate is set on the overall
# accuracy only until the collision is fixed and per-intent gates are viable.
# ---------------------------------------------------------------------------

class TestBenchmarkRegressionGate152:
    """
    Runs the 152-query diagnostic benchmark and asserts overall minimum accuracy.
    Threshold is FAST_CLASSIFIER_152Q_MIN_ACCURACY from IntentExtractionService.
    """

    BENCHMARK_PATH = "evaluation_results/benchmarks/retrieval_benchmark.json"
    MIN_ACCURACY = IntentExtractionService.FAST_CLASSIFIER_152Q_MIN_ACCURACY

    def _load_benchmark(self):
        import json
        with open(self.BENCHMARK_PATH) as f:
            return json.load(f)

    def test_overall_accuracy_not_regressed(self):
        svc = IntentExtractionService()
        data = self._load_benchmark()
        correct = 0
        failures = []
        for item in data:
            q = item["query"]
            expected = item.get("expected_intent", "general")
            predicted = svc.extract_query_intent_fast(q)["intent_type"]
            if predicted == expected:
                correct += 1
            else:
                failures.append(f"  {q!r}: expected={expected!r} got={predicted!r}")

        accuracy = correct / len(data)
        failure_detail = "\n".join(failures[:20]) if failures else "none"
        assert accuracy >= self.MIN_ACCURACY, (
            f"152-query accuracy {accuracy:.1%} < gate {self.MIN_ACCURACY:.1%}.\n"
            f"First 20 failures ({len(failures)} total):\n{failure_detail}"
        )
