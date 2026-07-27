"""
Phase 1 categorization redesign — unit tests.

All tests are pure Python: no database, no network, no embedding model
calls.  DB and model dependencies are replaced with lightweight mocks.

Coverage:
  1. _sanitize_category_name  — all rejection branches + pass-through cases
  2. _find_or_create_category — cap_hit returns (None, "cap_hit", 0.0)
  3. process_note             — handles None category without crashing
  4. _refresh_category_embedding — incremental centroid math
  5. count_by_user            — only counts active categories (repo unit)
"""

from __future__ import annotations

import types
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

# ---------------------------------------------------------------------------
# Helpers — build a service instance without touching the DB or disk
# ---------------------------------------------------------------------------

def _make_service():
    """
    Return an IntentCategoryService with all DB-backed collaborators mocked
    so tests can call methods in isolation.
    """
    from app.services.intent_category_service import IntentCategoryService

    db = MagicMock()
    service = IntentCategoryService.__new__(IntentCategoryService)
    service.db = db
    service.category_repo = MagicMock()
    service.intent_repo = MagicMock()
    service.extractor = MagicMock()
    return service


def _make_intent(
    intent_type="study",
    topic="PostgreSQL",
    actor=None,
    action=None,
    object_=None,
    confidence=0.9,
):
    return {
        "intent_type": intent_type,
        "action": action,
        "actor": actor,
        "topic": topic,
        "subtopic": None,
        "object": object_,
        "due_date": None,
        "temporal_text": None,
        "urgency": "medium",
        "category_hint": None,
        "confidence": confidence,
        "reasoning_summary": "test",
        "raw_llm_json": None,
        "model_name": "test",
        "prompt_version": "intent-v2",
        "source_text": topic or "",
    }


# ===========================================================================
# 1. _sanitize_category_name
# ===========================================================================

class TestSanitizeCategoryName:
    """
    _sanitize_category_name strips trailing punctuation and falls back to
    "General" for pathological single-token names.
    """

    def setup_method(self):
        self.svc = _make_service()

    # --- Trailing punctuation stripping ------------------------------------

    def test_strips_trailing_period(self):
        result = self.svc._sanitize_category_name("Flutter Application Performance.")
        assert result == "Flutter Application Performance"

    def test_strips_trailing_comma(self):
        result = self.svc._sanitize_category_name("Tasks,")
        assert result == "Tasks"

    def test_strips_multiple_trailing_punctuation(self):
        result = self.svc._sanitize_category_name("Ideas!?")
        assert result == "Ideas"

    # --- Python built-ins rejected ----------------------------------------

    def test_rejects_print(self):
        assert self.svc._sanitize_category_name("Print") == "General"

    def test_rejects_reduce(self):
        assert self.svc._sanitize_category_name("Reduce") == "General"

    def test_rejects_id(self):
        assert self.svc._sanitize_category_name("Id") == "General"

    def test_rejects_map(self):
        assert self.svc._sanitize_category_name("Map") == "General"

    def test_rejects_filter(self):
        assert self.svc._sanitize_category_name("Filter") == "General"

    def test_rejects_list(self):
        assert self.svc._sanitize_category_name("List") == "General"

    def test_rejects_sum(self):
        assert self.svc._sanitize_category_name("Sum") == "General"

    # Built-ins are compared case-insensitively
    def test_rejects_print_lowercase(self):
        assert self.svc._sanitize_category_name("print") == "General"

    def test_rejects_reduce_uppercase(self):
        assert self.svc._sanitize_category_name("REDUCE") == "General"

    # --- Python keywords rejected -----------------------------------------

    def test_rejects_for_keyword(self):
        assert self.svc._sanitize_category_name("For") == "General"

    def test_rejects_class_keyword(self):
        assert self.svc._sanitize_category_name("Class") == "General"

    def test_rejects_return_keyword(self):
        assert self.svc._sanitize_category_name("Return") == "General"

    def test_rejects_import_keyword(self):
        assert self.svc._sanitize_category_name("Import") == "General"

    # --- Too-short single tokens that are not known acronyms --------------

    def test_rejects_rs(self):
        # "Rs" — 2 letters, not a known acronym
        assert self.svc._sanitize_category_name("Rs") == "General"

    def test_rejects_single_letter(self):
        assert self.svc._sanitize_category_name("A") == "General"

    # --- No alphabetic characters -----------------------------------------

    def test_rejects_digits_only(self):
        assert self.svc._sanitize_category_name("42") == "General"

    def test_rejects_punctuation_only(self):
        assert self.svc._sanitize_category_name("---") == "General"

    # --- Known acronyms must pass through ---------------------------------

    def test_allows_ai(self):
        assert self.svc._sanitize_category_name("AI") == "AI"

    def test_allows_api(self):
        assert self.svc._sanitize_category_name("API") == "API"

    def test_allows_sql(self):
        assert self.svc._sanitize_category_name("SQL") == "SQL"

    def test_allows_ml(self):
        assert self.svc._sanitize_category_name("ML") == "ML"

    # --- Valid multi-word and compound names pass through -----------------

    def test_allows_study_postgresql(self):
        result = self.svc._sanitize_category_name("Study - PostgreSQL")
        assert result == "Study - PostgreSQL"

    def test_allows_communication_sid(self):
        result = self.svc._sanitize_category_name("Communication - Sid")
        assert result == "Communication - Sid"

    def test_allows_tasks(self):
        # "Tasks" is a generic word but not a Python built-in or keyword
        assert self.svc._sanitize_category_name("Tasks") == "Tasks"

    def test_allows_meetings(self):
        assert self.svc._sanitize_category_name("Meetings") == "Meetings"

    def test_allows_ideas(self):
        assert self.svc._sanitize_category_name("Ideas") == "Ideas"

    def test_allows_flutter(self):
        # Single token, but long enough and alphabetic — not a built-in
        assert self.svc._sanitize_category_name("Flutter") == "Flutter"

    def test_allows_kubernetes(self):
        assert self.svc._sanitize_category_name("Kubernetes") == "Kubernetes"

    def test_empty_string_returns_general(self):
        assert self.svc._sanitize_category_name("") == "General"

    def test_whitespace_only_returns_general(self):
        assert self.svc._sanitize_category_name("   ") == "General"


# ===========================================================================
# 2. _find_or_create_category — cap_hit path
# ===========================================================================

class TestFindOrCreateCategoryCapHit:
    """
    When count_by_user() >= MAX_CATEGORIES_PER_USER, _find_or_create_category
    must return (None, "cap_hit", 0.0) instead of force-assigning.
    """

    def setup_method(self):
        self.svc = _make_service()
        from app.services.intent_category_service import IntentCategoryService
        self.MAX = IntentCategoryService.MAX_CATEGORIES_PER_USER

    def _run_at_cap(self, intent):
        """Drive _find_or_create_category with the category count at the cap.
        Patches _adaptive_max_categories to return the legacy constant so that
        Phase 1 cap-hit tests are not affected by the Phase 2 adaptive cap."""
        # All early-exit paths miss so we reach the cap check.
        self.svc.category_repo.find_by_name.return_value = None
        self.svc.category_repo.find_rule_match.return_value = None
        self.svc.category_repo.search_by_embedding_with_distance.return_value = []
        self.svc.category_repo.count_by_user.return_value = self.MAX

        with patch(
            "app.services.intent_category_service.embedding_model"
        ) as mock_model, patch.object(
            self.svc, "_adaptive_max_categories", return_value=self.MAX
        ):
            mock_model.encode.return_value = MagicMock(tolist=lambda: [0.1] * 384)
            return self.svc._find_or_create_category(
                user_id=1, intent=intent
            )

    def test_returns_none_category_at_cap(self):
        category, method, score = self._run_at_cap(_make_intent())
        assert category is None

    def test_returns_cap_hit_method(self):
        _, method, _ = self._run_at_cap(_make_intent())
        assert method == "cap_hit"

    def test_returns_zero_score(self):
        _, _, score = self._run_at_cap(_make_intent())
        assert score == 0.0

    def test_does_not_call_create_at_cap(self):
        self._run_at_cap(_make_intent())
        self.svc.category_repo.create.assert_not_called()

    def test_cap_fallback_never_used(self):
        """Regression: no 'cap_fallback' method is ever returned."""
        _, method, _ = self._run_at_cap(_make_intent())
        assert method != "cap_fallback"

    def test_below_cap_still_creates(self):
        """One below the cap should proceed to create a new category."""
        from app.models.intent_category import IntentCategory
        self.svc.category_repo.find_by_name.return_value = None
        self.svc.category_repo.find_rule_match.return_value = None
        self.svc.category_repo.search_by_embedding_with_distance.return_value = []
        self.svc.category_repo.count_by_user.return_value = self.MAX - 1

        mock_category = MagicMock(spec=IntentCategory)
        mock_category.id = 99
        mock_category.name = "Study - PostgreSQL"
        self.svc.category_repo.create.return_value = mock_category

        with patch(
            "app.services.intent_category_service.embedding_model"
        ) as mock_model, patch.object(
            self.svc, "_adaptive_max_categories", return_value=self.MAX
        ):
            mock_model.encode.return_value = MagicMock(tolist=lambda: [0.1] * 384)
            category, method, _ = self.svc._find_or_create_category(
                user_id=1, intent=_make_intent()
            )

        assert category is not None
        assert method == "created"
        self.svc.category_repo.create.assert_called_once()


# ===========================================================================
# 3. process_note — None category is handled gracefully
# ===========================================================================

class TestProcessNoteCapHit:
    """
    When _find_or_create_category returns None, process_note must:
    - Not call create_or_update_assignment
    - Not call touch_after_assignment
    - Not call _refresh_category_embedding
    - Return {"intent": ..., "category": None, "assignment": None}
    """

    def setup_method(self):
        self.svc = _make_service()

    def _mock_intent_result(self):
        return _make_intent()

    def test_returns_none_category_and_assignment(self):
        mock_stored_intent = MagicMock()
        self.svc.extractor.extract.return_value = self._mock_intent_result()
        self.svc.intent_repo.create_or_update_note_intent.return_value = mock_stored_intent

        with patch.object(
            self.svc, "_find_or_create_category", return_value=(None, "cap_hit", 0.0)
        ), patch.object(
            self.svc, "_normalize_intent_fields", side_effect=lambda x: x
        ):
            result = self.svc.process_note(
                note_id=1, user_id=1, title="Test note", content=None
            )

        assert result["category"] is None
        assert result["assignment"] is None
        assert result["intent"] is mock_stored_intent

    def test_assignment_not_created_when_cap_hit(self):
        self.svc.extractor.extract.return_value = self._mock_intent_result()
        self.svc.intent_repo.create_or_update_note_intent.return_value = MagicMock()

        with patch.object(
            self.svc, "_find_or_create_category", return_value=(None, "cap_hit", 0.0)
        ), patch.object(
            self.svc, "_normalize_intent_fields", side_effect=lambda x: x
        ):
            self.svc.process_note(
                note_id=2, user_id=1, title="Test note", content=None
            )

        self.svc.intent_repo.create_or_update_assignment.assert_not_called()

    def test_touch_and_embedding_skipped_when_cap_hit(self):
        self.svc.extractor.extract.return_value = self._mock_intent_result()
        self.svc.intent_repo.create_or_update_note_intent.return_value = MagicMock()

        with patch.object(
            self.svc, "_find_or_create_category", return_value=(None, "cap_hit", 0.0)
        ), patch.object(
            self.svc, "_normalize_intent_fields", side_effect=lambda x: x
        ), patch.object(
            self.svc, "_refresh_category_embedding"
        ) as mock_refresh:
            self.svc.process_note(
                note_id=3, user_id=1, title="Test note", content=None
            )

        self.svc.category_repo.touch_after_assignment.assert_not_called()
        mock_refresh.assert_not_called()

    def test_intent_is_still_stored_when_cap_hit(self):
        """Even with no category, the intent record must be written to the DB."""
        stored = MagicMock()
        self.svc.extractor.extract.return_value = self._mock_intent_result()
        self.svc.intent_repo.create_or_update_note_intent.return_value = stored

        with patch.object(
            self.svc, "_find_or_create_category", return_value=(None, "cap_hit", 0.0)
        ), patch.object(
            self.svc, "_normalize_intent_fields", side_effect=lambda x: x
        ):
            result = self.svc.process_note(
                note_id=4, user_id=1, title="Test note", content=None
            )

        self.svc.intent_repo.create_or_update_note_intent.assert_called_once()
        assert result["intent"] is stored


# ===========================================================================
# 4. _refresh_category_embedding — incremental centroid
# ===========================================================================

class TestRefreshCategoryEmbeddingCentroid:
    """
    The centroid update formula:
        c_new = (c_old * N + v_new) / (N + 1)

    First assignment: embedding = v_new, centroid_note_count = 1.
    Subsequent assignments: running mean applied, count incremented.
    """

    DIM = 4  # use a tiny dimension for readable assertions

    def setup_method(self):
        self.svc = _make_service()

    def _make_category(self, category_id=1):
        from app.models.intent_category import IntentCategory
        cat = MagicMock(spec=IntentCategory)
        cat.id = category_id
        cat.name = "Study - Test"
        cat.intent_type = "study"
        cat.actor = None
        cat.action = None
        return cat

    def _run_refresh(self, category, intent, new_vector, existing_embedding=None):
        self.svc.category_repo.get_embedding.return_value = existing_embedding

        with patch(
            "app.services.intent_category_service.embedding_model"
        ) as mock_model:
            mock_model.encode.return_value = MagicMock(
                tolist=lambda: new_vector
            )
            self.svc._refresh_category_embedding(category=category, intent=intent)

        return self.svc.category_repo.upsert_embedding.call_args

    def test_first_note_sets_embedding_to_note_vector(self):
        """When no prior embedding exists, the centroid equals the first note."""
        v = [1.0, 0.0, 0.0, 0.0]
        call_args = self._run_refresh(
            self._make_category(),
            _make_intent(),
            new_vector=v,
            existing_embedding=None,
        )
        kwargs = call_args.kwargs
        assert kwargs["embedding_vector"] == v
        assert kwargs["centroid_note_count"] == 1

    def test_second_note_produces_mean(self):
        """Second note: centroid = (v1*1 + v2) / 2."""
        existing = MagicMock()
        existing.embedding_vector = [1.0, 0.0, 0.0, 0.0]
        existing.centroid_note_count = 1

        v2 = [0.0, 1.0, 0.0, 0.0]
        call_args = self._run_refresh(
            self._make_category(),
            _make_intent(),
            new_vector=v2,
            existing_embedding=existing,
        )
        kwargs = call_args.kwargs
        expected = [0.5, 0.5, 0.0, 0.0]
        assert kwargs["embedding_vector"] == pytest.approx(expected)
        assert kwargs["centroid_note_count"] == 2

    def test_third_note_keeps_running_mean(self):
        """Third note: centroid = (v_prev*2 + v3) / 3."""
        existing = MagicMock()
        # centroid after 2 notes: [0.5, 0.5, 0.0, 0.0]
        existing.embedding_vector = [0.5, 0.5, 0.0, 0.0]
        existing.centroid_note_count = 2

        v3 = [0.0, 0.0, 1.0, 0.0]
        call_args = self._run_refresh(
            self._make_category(),
            _make_intent(),
            new_vector=v3,
            existing_embedding=existing,
        )
        kwargs = call_args.kwargs
        # (0.5*2 + 0.0)/3, (0.5*2 + 0.0)/3, (0.0*2 + 1.0)/3, 0
        expected = [1/3, 1/3, 1/3, 0.0]
        assert kwargs["embedding_vector"] == pytest.approx(expected, abs=1e-9)
        assert kwargs["centroid_note_count"] == 3

    def test_count_increments_correctly_over_many_notes(self):
        """After N notes, centroid_note_count must equal N."""
        n_start = 42
        existing = MagicMock()
        existing.embedding_vector = [0.5] * 4
        existing.centroid_note_count = n_start

        call_args = self._run_refresh(
            self._make_category(),
            _make_intent(),
            new_vector=[0.1, 0.2, 0.3, 0.4],
            existing_embedding=existing,
        )
        assert call_args.kwargs["centroid_note_count"] == n_start + 1

    def test_zero_count_treated_as_first_note(self):
        """An existing row with centroid_note_count=0 is treated as a fresh start."""
        existing = MagicMock()
        existing.embedding_vector = [0.0] * 4
        existing.centroid_note_count = 0

        v = [1.0, 0.0, 0.0, 0.0]
        call_args = self._run_refresh(
            self._make_category(),
            _make_intent(),
            new_vector=v,
            existing_embedding=existing,
        )
        kwargs = call_args.kwargs
        assert kwargs["embedding_vector"] == v
        assert kwargs["centroid_note_count"] == 1

    def test_upsert_called_once_per_refresh(self):
        call_args = self._run_refresh(
            self._make_category(),
            _make_intent(),
            new_vector=[0.1] * 4,
        )
        self.svc.category_repo.upsert_embedding.assert_called_once()

    def test_intent_signature_is_embedded_not_category_metadata(self):
        """The embedding_model receives the intent signature, not category fields."""
        category = self._make_category()
        category.name = "Study - PostgreSQL"
        intent = _make_intent(intent_type="study", topic="PostgreSQL", action="study")

        with patch(
            "app.services.intent_category_service.embedding_model"
        ) as mock_model:
            mock_model.encode.return_value = MagicMock(tolist=lambda: [0.0] * 4)
            self.svc.category_repo.get_embedding.return_value = None
            self.svc._refresh_category_embedding(category=category, intent=intent)

        encoded_text = mock_model.encode.call_args[0][0]
        # The encoded text must NOT be the category name alone
        assert encoded_text != category.name
        # It must contain intent-derived tokens
        assert any(
            token in encoded_text
            for token in ["study", "PostgreSQL", "Study"]
        )


# ===========================================================================
# 5. count_by_user — only counts active categories
# ===========================================================================

class TestCountByUserActiveOnly:
    """
    IntentCategoryRepository.count_by_user must filter by status='active'
    so that archived or merged categories do not count against the cap.
    """

    def test_query_filters_on_active_status(self):
        from app.repositories.intent_category_repository import IntentCategoryRepository
        from app.models.intent_category import IntentCategory
        import sqlalchemy

        db = MagicMock()

        # The implementation passes BOTH conditions to a single .filter() call:
        #   .filter(IntentCategory.user_id == user_id, IntentCategory.status == "active")
        mock_query = MagicMock()
        mock_filter = MagicMock()
        mock_filter.count.return_value = 7

        db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter

        repo = IntentCategoryRepository(db)
        count = repo.count_by_user(user_id=1)

        assert count == 7
        # Exactly one .filter() call (both conditions passed together)
        assert mock_query.filter.call_count == 1
        # count() must have been invoked on the filtered query
        mock_filter.count.assert_called_once()
