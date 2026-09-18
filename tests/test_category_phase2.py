"""
Phase 2 category pipeline redesign — unit tests (ADR-002).

All tests are pure Python: no database, no network, no embedding model calls.
DB and model dependencies are replaced with lightweight mocks.

Coverage:
  1. _compatible()         — Phase 2 gates (intent_type + actor only, no topic)
  2. _compatible_strict()  — Phase 1 fallback (exact topic string equality restored)
  3. _reuse_threshold()    — per-intent-type dispatch
  4. _adaptive_max_categories() — scaling formula and flag toggling
  5. _should_create_general_category() — topic quality guard
  6. _get_or_create_general_catchall() — creates / reuses the catchall
  7. _find_or_create_category() pipeline — 4-step order with feature flags
  8. Backwards compatibility — flags=False restores Phase 1 behaviour
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch, call

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_service():
    from app.services.intent_category_service import IntentCategoryService
    svc = IntentCategoryService.__new__(IntentCategoryService)
    svc.db = MagicMock()
    svc.category_repo = MagicMock()
    svc.intent_repo = MagicMock()
    svc.extractor = MagicMock()
    return svc


def _make_category(
    id=1, name="Study - PostgreSQL", intent_type="study",
    actor=None, note_count=5,
):
    from app.models.intent_category import IntentCategory
    cat = MagicMock(spec=IntentCategory)
    cat.id = id
    cat.name = name
    cat.intent_type = intent_type
    cat.actor = actor
    cat.note_count = note_count
    cat.status = "active"
    return cat


def _make_intent(
    intent_type="study", topic="PostgreSQL", actor=None, action=None, confidence=0.9
):
    return {
        "intent_type": intent_type,
        "action": action,
        "actor": actor,
        "topic": topic,
        "subtopic": None,
        "object": None,
        "due_date": None,
        "temporal_text": None,
        "urgency": "medium",
        "confidence": confidence,
        "category_hint": None,
        "source_text": topic or "",
        "raw_llm_json": None,
        "model_name": "test",
        "prompt_version": "intent-v2",
        "reasoning_summary": None,
    }


# ===========================================================================
# 1. _compatible() — Phase 2: intent_type + actor only
# ===========================================================================

class TestCompatiblePhase2:
    """_compatible() in Phase 2 mode checks intent_type and actor only.
    Topic string equality is NOT checked (that's the dead-code fix)."""

    def setup_method(self):
        self.svc = _make_service()

    # --- intent_type gate --------------------------------------------------

    def test_same_intent_type_is_compatible(self):
        cat = _make_category(intent_type="study")
        assert self.svc._compatible(cat, _make_intent(intent_type="study"))

    def test_different_intent_type_is_incompatible(self):
        cat = _make_category(intent_type="study")
        assert not self.svc._compatible(cat, _make_intent(intent_type="question"))

    def test_general_vs_study_incompatible(self):
        # Evidence: 5 notes within T=0.28 were rejected for 'study' vs 'general'
        # _compatible() must keep this gate
        cat = _make_category(intent_type="study")
        assert not self.svc._compatible(cat, _make_intent(intent_type="general"))

    # --- actor gate --------------------------------------------------------

    def test_matching_actors_compatible(self):
        cat = _make_category(intent_type="communication", actor="Sid")
        intent = _make_intent(intent_type="communication", actor="Sid")
        assert self.svc._compatible(cat, intent)

    def test_different_actors_incompatible(self):
        cat = _make_category(intent_type="communication", actor="Sid")
        intent = _make_intent(intent_type="communication", actor="Siddhant")
        assert not self.svc._compatible(cat, intent)

    def test_actor_presence_mismatch_incompatible(self):
        # Category has actor, intent does not → incompatible
        cat = _make_category(intent_type="communication", actor="Sid")
        intent = _make_intent(intent_type="communication", actor=None)
        assert not self.svc._compatible(cat, intent)

    def test_no_actor_both_compatible(self):
        cat = _make_category(intent_type="study", actor=None)
        intent = _make_intent(intent_type="study", actor=None)
        assert self.svc._compatible(cat, intent)

    # --- KEY: topic is NOT checked -----------------------------------------

    def test_different_topic_still_compatible(self):
        """Phase 2 core change: near-miss topics ("k8s" vs "Kubernetes")
        should be able to reuse via distance threshold, not string equality."""
        cat = _make_category(name="Study - Kubernetes", intent_type="study")
        intent = _make_intent(intent_type="study", topic="k8s")
        # In Phase 1 this would fail (topic_mismatch); in Phase 2 it passes
        assert self.svc._compatible(cat, intent)

    def test_completely_different_topic_still_compatible_when_type_matches(self):
        """The distance threshold (not _compatible) decides topic proximity.
        _compatible() only gates on intent_type + actor."""
        cat = _make_category(name="Study - Redis", intent_type="study")
        intent = _make_intent(intent_type="study", topic="Kafka")
        # Compatible at the logic level — the distance threshold will prevent
        # the actual reuse (Redis and Kafka are >0.30 apart in embedding space)
        assert self.svc._compatible(cat, intent)

    # --- actor case-insensitive comparison ---------------------------------

    def test_actor_comparison_is_case_insensitive(self):
        cat = _make_category(intent_type="communication", actor="Sid")
        intent = _make_intent(intent_type="communication", actor="sid")
        # Normalization makes this compatible
        cat.actor = "Sid"
        assert self.svc._compatible(cat, intent)


# ===========================================================================
# 2. _compatible_strict() — Phase 1 fallback
# ===========================================================================

class TestCompatibleStrict:
    """Phase 1 behaviour: adds exact topic-string equality check."""

    def setup_method(self):
        self.svc = _make_service()

    def test_same_topic_and_type_compatible(self):
        cat = _make_category(name="Study - PostgreSQL", intent_type="study")
        intent = _make_intent(intent_type="study", topic="PostgreSQL")
        assert self.svc._compatible_strict(cat, intent)

    def test_different_topic_strict_incompatible(self):
        """This is the dead-code case: same normalization as canonical_name."""
        cat = _make_category(name="Study - Kubernetes", intent_type="study")
        intent = _make_intent(intent_type="study", topic="k8s")
        # In strict mode, "kubernetes" != "k8s" → incompatible
        assert not self.svc._compatible_strict(cat, intent)

    def test_intent_type_mismatch_still_fails(self):
        cat = _make_category(name="Study - Redis", intent_type="study")
        intent = _make_intent(intent_type="reference", topic="Redis")
        assert not self.svc._compatible_strict(cat, intent)


# ===========================================================================
# 3. _reuse_threshold() — per-intent dispatch
# ===========================================================================

class TestReuseThreshold:

    def setup_method(self):
        self.svc = _make_service()

    def test_study_uses_precise_threshold(self):
        assert self.svc._reuse_threshold("study") == 0.30

    def test_reference_uses_precise_threshold(self):
        assert self.svc._reuse_threshold("reference") == 0.30

    def test_question_uses_precise_threshold(self):
        assert self.svc._reuse_threshold("question") == 0.30

    def test_idea_uses_broad_threshold(self):
        assert self.svc._reuse_threshold("idea") == 0.40

    def test_general_uses_intermediate_threshold(self):
        # general uses 0.35 (between precise and broad)
        assert self.svc._reuse_threshold("general") == 0.35

    def test_todo_uses_broad_threshold(self):
        assert self.svc._reuse_threshold("todo") == 0.40

    def test_event_uses_broad_threshold(self):
        assert self.svc._reuse_threshold("event") == 0.40

    def test_reminder_uses_broad_threshold(self):
        assert self.svc._reuse_threshold("reminder") == 0.40

    def test_communication_uses_intermediate_threshold(self):
        assert self.svc._reuse_threshold("communication") == 0.35

    def test_unknown_type_returns_broad(self):
        # Unknown types default to the broad threshold
        assert self.svc._reuse_threshold("project") == 0.40


# ===========================================================================
# 4. _adaptive_max_categories()
# ===========================================================================

class TestAdaptiveMaxCategories:

    def setup_method(self):
        self.svc = _make_service()

    def _mock_note_count(self, count: int):
        from sqlalchemy import func
        mock_q = MagicMock()
        mock_q.filter.return_value = mock_q
        mock_q.scalar.return_value = count
        self.svc.db.query.return_value = mock_q

    def test_flag_off_returns_legacy_constant(self):
        with patch("app.services.intent_category_service.settings") as s:
            s.CATEGORY_ADAPTIVE_CAP_ENABLED = False
            from app.services.intent_category_service import IntentCategoryService
            result = self.svc._adaptive_max_categories(user_id=1)
        assert result == IntentCategoryService.MAX_CATEGORIES_PER_USER

    def test_at_1055_notes_returns_105(self):
        self._mock_note_count(1055)
        with patch("app.services.intent_category_service.settings") as s:
            s.CATEGORY_ADAPTIVE_CAP_ENABLED = True
            s.CATEGORY_NOTES_PER_CAP = 10
            s.CATEGORY_ADAPTIVE_CAP_MIN = 50
            s.CATEGORY_ADAPTIVE_CAP_MAX = 2000
            result = self.svc._adaptive_max_categories(user_id=1)
        assert result == 105

    def test_at_100_notes_respects_floor(self):
        self._mock_note_count(100)
        with patch("app.services.intent_category_service.settings") as s:
            s.CATEGORY_ADAPTIVE_CAP_ENABLED = True
            s.CATEGORY_NOTES_PER_CAP = 10
            s.CATEGORY_ADAPTIVE_CAP_MIN = 50
            s.CATEGORY_ADAPTIVE_CAP_MAX = 2000
            result = self.svc._adaptive_max_categories(user_id=1)
        assert result == 50  # floor

    def test_at_100k_notes_respects_ceiling(self):
        self._mock_note_count(100_000)
        with patch("app.services.intent_category_service.settings") as s:
            s.CATEGORY_ADAPTIVE_CAP_ENABLED = True
            s.CATEGORY_NOTES_PER_CAP = 10
            s.CATEGORY_ADAPTIVE_CAP_MIN = 50
            s.CATEGORY_ADAPTIVE_CAP_MAX = 2000
            result = self.svc._adaptive_max_categories(user_id=1)
        assert result == 2000  # ceiling

    def test_at_3000_notes_returns_300(self):
        self._mock_note_count(3000)
        with patch("app.services.intent_category_service.settings") as s:
            s.CATEGORY_ADAPTIVE_CAP_ENABLED = True
            s.CATEGORY_NOTES_PER_CAP = 10
            s.CATEGORY_ADAPTIVE_CAP_MIN = 50
            s.CATEGORY_ADAPTIVE_CAP_MAX = 2000
            result = self.svc._adaptive_max_categories(user_id=1)
        assert result == 300

    def test_zero_notes_returns_floor(self):
        self._mock_note_count(0)
        with patch("app.services.intent_category_service.settings") as s:
            s.CATEGORY_ADAPTIVE_CAP_ENABLED = True
            s.CATEGORY_NOTES_PER_CAP = 10
            s.CATEGORY_ADAPTIVE_CAP_MIN = 50
            s.CATEGORY_ADAPTIVE_CAP_MAX = 2000
            result = self.svc._adaptive_max_categories(user_id=1)
        assert result == 50


# ===========================================================================
# 5. _should_create_general_category()
# ===========================================================================

class TestShouldCreateGeneralCategory:

    def setup_method(self):
        self.svc = _make_service()

    def _intent(self, topic):
        return {"topic": topic, "subtopic": None, "object": None,
                "source_text": topic or "", "category_hint": None,
                "intent_type": "general", "actor": None, "action": None}

    # --- Should create (True) ----------------------------------------------

    def test_brand_name_allowed(self):
        assert self.svc._should_create_general_category(self._intent("Kubernetes"))

    def test_acronym_allowed(self):
        assert self.svc._should_create_general_category(self._intent("AI"))

    def test_meaningful_multi_word_allowed(self):
        assert self.svc._should_create_general_category(self._intent("System Design"))

    def test_long_single_word_allowed(self):
        # "Database" — 8 chars, not a verb, not a keyword
        assert self.svc._should_create_general_category(self._intent("Database"))

    def test_redis_allowed(self):
        # Known brand, single word
        assert self.svc._should_create_general_category(self._intent("Redis"))

    # --- Should reject (False) ---------------------------------------------

    def test_empty_topic_rejected(self):
        assert not self.svc._should_create_general_category(self._intent(None))

    def test_single_verb_rejected(self):
        assert not self.svc._should_create_general_category(self._intent("Added"))

    def test_change_verb_rejected(self):
        assert not self.svc._should_create_general_category(self._intent("Changed"))

    def test_python_builtin_rejected(self):
        assert not self.svc._should_create_general_category(self._intent("Print"))

    def test_python_keyword_rejected(self):
        assert not self.svc._should_create_general_category(self._intent("For"))

    def test_two_char_token_rejected(self):
        assert not self.svc._should_create_general_category(self._intent("Rs"))

    def test_question_fragment_rejected(self):
        assert not self.svc._should_create_general_category(
            self._intent("Does Redis Eviction")
        )

    def test_are_fragment_rejected(self):
        assert not self.svc._should_create_general_category(
            self._intent("Are Advantages Docker")
        )

    def test_three_char_unknown_rejected(self):
        # "Vq", "Am" — 2 chars, not acronym
        assert not self.svc._should_create_general_category(self._intent("Vq"))


# ===========================================================================
# 6. _get_or_create_general_catchall()
# ===========================================================================

class TestGetOrCreateGeneralCatchall:

    def setup_method(self):
        self.svc = _make_service()

    def test_returns_existing_catchall_if_found(self):
        existing = _make_category(name="General", intent_type="general")
        self.svc.category_repo.find_by_name.return_value = existing
        result = self.svc._get_or_create_general_catchall(user_id=1)
        assert result is existing
        self.svc.category_repo.create.assert_not_called()

    def test_creates_catchall_when_not_found(self):
        self.svc.category_repo.find_by_name.return_value = None
        self.svc.category_repo.count_by_user.return_value = 50
        new_cat = _make_category(name="General", intent_type="general")
        self.svc.category_repo.create.return_value = new_cat

        with patch.object(self.svc, "_adaptive_max_categories", return_value=105):
            result = self.svc._get_or_create_general_catchall(user_id=1)

        assert result is new_cat
        self.svc.category_repo.create.assert_called_once()
        call_kwargs = self.svc.category_repo.create.call_args.kwargs
        assert call_kwargs["name"] == "General"
        assert call_kwargs["intent_type"] == "general"

    def test_returns_none_when_cap_reached(self):
        self.svc.category_repo.find_by_name.return_value = None
        self.svc.category_repo.count_by_user.return_value = 105

        with patch.object(self.svc, "_adaptive_max_categories", return_value=105):
            result = self.svc._get_or_create_general_catchall(user_id=1)

        assert result is None
        self.svc.category_repo.create.assert_not_called()


# ===========================================================================
# 7. _find_or_create_category() — 4-step pipeline
# ===========================================================================

class TestFindOrCreateCategoryPhase2Pipeline:
    """Integration-level pipeline tests with mocked repos."""

    def setup_method(self):
        self.svc = _make_service()
        # Default: flags ON, canonical misses, vector finds nothing, cap OK
        self.svc.category_repo.find_by_name.return_value = None
        self.svc.category_repo.count_by_user.return_value = 50
        self.svc.category_repo.search_by_embedding_with_distance.return_value = []
        mock_cat = _make_category()
        self.svc.category_repo.create.return_value = mock_cat

    def _run(self, intent_type="study", topic="Kafka"):
        intent = {
            "intent_type": intent_type, "action": None, "actor": None,
            "topic": topic, "subtopic": None, "object": None,
            "due_date": None, "temporal_text": None, "urgency": "medium",
            "confidence": 0.9, "category_hint": None, "source_text": "",
            "raw_llm_json": None, "model_name": "test", "prompt_version": "v2",
            "reasoning_summary": None,
        }
        with patch("app.services.intent_category_service.settings") as s:
            s.CATEGORY_FUZZY_COMPAT_ENABLED = True
            s.CATEGORY_ADAPTIVE_CAP_ENABLED = True
            s.CATEGORY_NOTES_PER_CAP = 10
            s.CATEGORY_ADAPTIVE_CAP_MIN = 50
            s.CATEGORY_ADAPTIVE_CAP_MAX = 2000
            s.CATEGORY_CONSERVATIVE_GENERAL_ENABLED = True
            s.CATEGORY_INGEST_THRESHOLD = 0.28
            with patch("app.services.intent_category_service.get_embedding_model") as em:
                em.return_value.encode.return_value = MagicMock(tolist=lambda: [0.1] * 384)
                with patch.object(self.svc, "_adaptive_max_categories", return_value=105):
                    return self.svc._find_or_create_category(user_id=1, intent=intent)

    # --- Step 1: canonical name --------------------------------------------

    def test_canonical_hit_returns_canonical(self):
        cat = _make_category()
        self.svc.category_repo.find_by_name.return_value = cat
        _, method, _ = self._run()
        assert method == "canonical_name"

    def test_canonical_hit_skips_vector_search(self):
        cat = _make_category()
        self.svc.category_repo.find_by_name.return_value = cat
        self._run()
        self.svc.category_repo.search_by_embedding_with_distance.assert_not_called()

    # --- Step 2: vector reuse ----------------------------------------------

    def test_vector_hit_returns_vector(self):
        compat_cat = _make_category(name="Study - Kubernetes", intent_type="study")
        self.svc.category_repo.search_by_embedding_with_distance.return_value = [
            (compat_cat, 0.25),
        ]
        _, method, score = self._run(intent_type="study", topic="k8s")
        assert method == "vector"
        assert pytest.approx(score, abs=0.01) == 0.75  # 1.0 - 0.25

    def test_vector_incompatible_candidate_skipped(self):
        """A vector candidate with wrong intent_type must be skipped."""
        wrong_type_cat = _make_category(name="Reference - Kafka", intent_type="reference")
        self.svc.category_repo.search_by_embedding_with_distance.return_value = [
            (wrong_type_cat, 0.15),
        ]
        _, method, _ = self._run(intent_type="study", topic="Kafka")
        # Vector returned something but _compatible() rejects it
        # Falls through to create
        assert method == "created"

    # --- Step 3: adaptive cap ----------------------------------------------

    def test_cap_hit_returns_none(self):
        # Drive _find_or_create_category directly so we can set adaptive_max=50
        # and count=50 without _run()'s internal override of _adaptive_max_categories.
        self.svc.category_repo.count_by_user.return_value = 50
        intent = {
            "intent_type": "study", "action": None, "actor": None,
            "topic": "Kafka", "subtopic": None, "object": None,
            "due_date": None, "temporal_text": None, "urgency": "medium",
            "confidence": 0.9, "category_hint": None, "source_text": "",
            "raw_llm_json": None, "model_name": "test", "prompt_version": "v2",
            "reasoning_summary": None,
        }
        with patch("app.services.intent_category_service.settings") as s, \
             patch("app.services.intent_category_service.get_embedding_model") as em, \
             patch.object(self.svc, "_adaptive_max_categories", return_value=50):
            s.CATEGORY_FUZZY_COMPAT_ENABLED = True
            s.CATEGORY_ADAPTIVE_CAP_ENABLED = True
            s.CATEGORY_CONSERVATIVE_GENERAL_ENABLED = True
            s.CATEGORY_INGEST_THRESHOLD = 0.28
            em.return_value.encode.return_value = MagicMock(tolist=lambda: [0.1] * 384)
            cat, method, score = self.svc._find_or_create_category(user_id=1, intent=intent)
        assert cat is None
        assert method == "cap_hit"
        assert score == 0.0

    def test_below_cap_proceeds_to_create(self):
        self.svc.category_repo.count_by_user.return_value = 40
        with patch.object(self.svc, "_adaptive_max_categories", return_value=105):
            _, method, _ = self._run()
        assert method == "created"

    # --- Step 4: general intent conservation --------------------------

    def test_general_bad_topic_uses_catchall(self):
        catchall = _make_category(name="General", intent_type="general")
        self.svc.category_repo.count_by_user.return_value = 50
        with patch.object(self.svc, "_adaptive_max_categories", return_value=105), \
             patch.object(self.svc, "_get_or_create_general_catchall", return_value=catchall):
            cat, method, _ = self._run(intent_type="general", topic="Added")
        assert method == "general_catchall"
        assert cat is catchall

    def test_general_good_topic_creates_new_category(self):
        self.svc.category_repo.count_by_user.return_value = 50
        with patch.object(self.svc, "_adaptive_max_categories", return_value=105):
            _, method, _ = self._run(intent_type="general", topic="Kubernetes")
        assert method == "created"

    # --- Rule_match is absent from pipeline --------------------------------

    def test_rule_match_not_called(self):
        """rule_match is retired (ADR-002); it should never be called."""
        self._run()
        self.svc.category_repo.find_rule_match.assert_not_called()

    # --- Step ordering: canonical before vector ----------------------------

    def test_canonical_fires_before_vector(self):
        cat = _make_category()
        self.svc.category_repo.find_by_name.return_value = cat
        _, method, _ = self._run()
        assert method == "canonical_name"
        # Vector search should not have been reached
        self.svc.category_repo.search_by_embedding_with_distance.assert_not_called()

    def test_vector_fires_before_create(self):
        compat_cat = _make_category(name="Study - Kafka", intent_type="study")
        self.svc.category_repo.search_by_embedding_with_distance.return_value = [
            (compat_cat, 0.22),
        ]
        _, method, _ = self._run(intent_type="study", topic="Kafka")
        assert method == "vector"
        self.svc.category_repo.create.assert_not_called()


# ===========================================================================
# 8. Backwards compatibility — CATEGORY_FUZZY_COMPAT_ENABLED=False
# ===========================================================================

class TestBackwardsCompatibility:
    """When feature flags are off, Phase 1 behaviour is fully restored."""

    def setup_method(self):
        self.svc = _make_service()
        self.svc.category_repo.find_by_name.return_value = None
        self.svc.category_repo.count_by_user.return_value = 50
        self.svc.category_repo.search_by_embedding_with_distance.return_value = []
        self.svc.category_repo.create.return_value = _make_category()

    def _run_flags_off(self, intent_type="study", topic="PostgreSQL"):
        intent = {
            "intent_type": intent_type, "action": None, "actor": None,
            "topic": topic, "subtopic": None, "object": None,
            "due_date": None, "temporal_text": None, "urgency": "medium",
            "confidence": 0.9, "category_hint": None, "source_text": "",
            "raw_llm_json": None, "model_name": "test", "prompt_version": "v2",
            "reasoning_summary": None,
        }
        with patch("app.services.intent_category_service.settings") as s:
            s.CATEGORY_FUZZY_COMPAT_ENABLED = False
            s.CATEGORY_ADAPTIVE_CAP_ENABLED = False
            s.CATEGORY_CONSERVATIVE_GENERAL_ENABLED = False
            s.CATEGORY_INGEST_THRESHOLD = 0.28
            from app.services.intent_category_service import IntentCategoryService
            s_val = IntentCategoryService.MAX_CATEGORIES_PER_USER
            with patch("app.services.intent_category_service.get_embedding_model") as em:
                em.return_value.encode.return_value = MagicMock(tolist=lambda: [0.1] * 384)
                return self.svc._find_or_create_category(user_id=1, intent=intent)

    def test_flags_off_still_does_canonical_match(self):
        cat = _make_category()
        self.svc.category_repo.find_by_name.return_value = cat
        _, method, _ = self._run_flags_off()
        assert method == "canonical_name"

    def test_flags_off_uses_strict_compat(self):
        """With flag off, _compatible_strict is used (topic equality required)."""
        # A near-miss candidate that would pass Phase 2 _compatible but fail strict
        near_miss = _make_category(name="Study - Kubernetes", intent_type="study")
        self.svc.category_repo.search_by_embedding_with_distance.return_value = [
            (near_miss, 0.15),  # within 0.28
        ]
        # Set count below the legacy cap so the note can proceed to create
        self.svc.category_repo.count_by_user.return_value = 40
        _, method, _ = self._run_flags_off(intent_type="study", topic="k8s")
        # strict: "k8s" != "kubernetes" → falls through to create
        assert method == "created"

    def test_flags_off_uses_legacy_cap(self):
        """With CATEGORY_ADAPTIVE_CAP_ENABLED=False, falls back to MAX_CATEGORIES_PER_USER (now 200)."""
        # Must equal IntentCategoryService.MAX_CATEGORIES_PER_USER (currently 200).
        # Update here if the constant changes again.
        self.svc.category_repo.count_by_user.return_value = 200
        cat, method, _ = self._run_flags_off()
        assert method == "cap_hit"
        assert cat is None

    def test_flags_off_general_creates_freely(self):
        """With CATEGORY_CONSERVATIVE_GENERAL_ENABLED=False, all topics create."""
        # count_by_user = 40 so we won't hit cap
        self.svc.category_repo.count_by_user.return_value = 40
        _, method, _ = self._run_flags_off(intent_type="general", topic="Added")
        # Without the guard, "Added" creates a new category
        assert method == "created"


# ===========================================================================
# EXTR-003 — _CATEGORY_INVALID_SINGLE_TOKENS guard in _sanitize_category_name
# ===========================================================================

class TestSanitizeCategoryNameInvalidTokenGuard:
    """
    Verifies the defense-in-depth guard added by EXTR-003.

    _validate_topic() in IntentExtractionService is the primary gate.
    This guard catches any garbage single-token that reaches category naming
    via the rule-based fallback or future code paths.
    """

    @pytest.mark.parametrize("bad", [
        # Conjunctions
        "Also", "also", "But", "but", "Or", "or",
        # Adverbs observed in phase2 corpus
        "Always", "always", "Never", "never", "Instead", "instead",
        "However", "however", "Already", "already", "Just", "just",
        # Weak adjectives from phase2
        "Common", "common", "Important", "important", "Crucial", "crucial",
        # Verb forms from phase2
        "Added", "added", "Changed", "changed", "Updated", "updated",
        "Deleted", "deleted", "Booked", "booked", "Fixed", "fixed",
        # Null/undefined leakage
        "None", "none", "Null", "null",
    ])
    def test_invalid_single_token_returns_general(self, bad):
        svc = _make_service()
        assert svc._sanitize_category_name(bad) == "General"

    def test_compound_name_with_dash_bypasses_guard(self):
        svc = _make_service()
        # " - " in the name means it is NOT a single token — guard is skipped.
        assert svc._sanitize_category_name("Study - PostgreSQL") == "Study - PostgreSQL"

    def test_multi_word_name_with_space_bypasses_guard(self):
        svc = _make_service()
        # A space makes it multi-token — guard is skipped.
        assert svc._sanitize_category_name("Flutter Application Performance") == "Flutter Application Performance"

    @pytest.mark.parametrize("good", [
        "PostgreSQL", "Flutter", "Kubernetes", "FastAPI",
        "Tasks", "Meetings", "Ideas", "General",
    ])
    def test_valid_single_word_not_affected(self, good):
        svc = _make_service()
        assert svc._sanitize_category_name(good) == good

    def test_existing_python_builtin_guard_still_works(self):
        svc = _make_service()
        assert svc._sanitize_category_name("print") == "General"
        assert svc._sanitize_category_name("reduce") == "General"

    def test_existing_python_keyword_guard_still_works(self):
        svc = _make_service()
        assert svc._sanitize_category_name("for") == "General"
        assert svc._sanitize_category_name("class") == "General"

    def test_existing_too_short_guard_still_works(self):
        svc = _make_service()
        # "rs" is not in _ACRONYM_WORDS, len=2 → rejected by too_short guard
        assert svc._sanitize_category_name("rs") == "General"

    def test_existing_no_alpha_guard_still_works(self):
        svc = _make_service()
        assert svc._sanitize_category_name("42") == "General"
        assert svc._sanitize_category_name("---") == "General"

    def test_trailing_period_still_stripped_before_guard(self):
        svc = _make_service()
        # Trailing punct is stripped first; result is multi-word, bypasses guard.
        result = svc._sanitize_category_name("Flutter Application Performance.")
        assert result == "Flutter Application Performance"

    def test_guard_is_case_insensitive(self, ):
        svc = _make_service()
        # The check uses lower = cleaned.lower(), so case doesn't matter.
        assert svc._sanitize_category_name("ALSO") == "General"
        assert svc._sanitize_category_name("ALWAYS") == "General"
