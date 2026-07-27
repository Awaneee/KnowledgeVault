"""
EXTR-001 — Actor tech-term validation tests.

All tests are pure Python: no database, no network, no embedding model.
"""
from __future__ import annotations

import pytest

from app.services.intent_extraction_service import IntentExtractionService


@pytest.fixture
def svc():
    return IntentExtractionService()


def _raw(actor=None, topic=None, intent_type="communication"):
    return {
        "intent_type": intent_type,
        "action": "discuss",
        "actor": actor,
        "topic": topic,
        "subtopic": None,
        "object": "migration",
        "temporal_text": None,
        "urgency": "medium",
        "confidence": 0.8,
        "_provider": "gemini",
    }


# ---------------------------------------------------------------------------
# _clean_actor — tech-term rejection
# ---------------------------------------------------------------------------

class TestCleanActorTechTerms:
    @pytest.mark.parametrize("tech", [
        "Python", "python", "PYTHON",
        "Docker", "docker",
        "Redis", "redis",
        "PostgreSQL", "postgresql",
        "Go", "go",
        "FastAPI", "fastapi",
        "Flutter", "flutter",
        "Kubernetes", "kubernetes",
        "React", "react",
        "JavaScript", "javascript",
    ])
    def test_tech_term_rejected(self, svc, tech):
        repairs = []
        result = svc._clean_actor(tech, repairs)
        assert result is None
        assert any("technology term" in r for r in repairs)

    def test_tech_term_rejection_covers_all_tech_map_keys(self, svc):
        for key in IntentExtractionService.TECH_MAP:
            assert svc._clean_actor(key, []) is None, (
                f"TECH_MAP key {key!r} should be rejected as actor"
            )
            assert svc._clean_actor(key.title(), []) is None, (
                f"TECH_MAP key {key.title()!r} (title-cased) should be rejected as actor"
            )


# ---------------------------------------------------------------------------
# _clean_actor — noise-word rejection
# ---------------------------------------------------------------------------

class TestCleanActorNoiseWords:
    @pytest.mark.parametrize("noise", [
        "Mock", "mock",
        "Show", "show",
        "Unprocessable", "unprocessable",
        "Booked", "booked",
        "Backend", "backend",
        "Frontend", "frontend",
        "Db", "db",
        "Api", "api",
    ])
    def test_noise_word_rejected(self, svc, noise):
        repairs = []
        result = svc._clean_actor(noise, repairs)
        assert result is None
        assert any("noise word" in r for r in repairs)


# ---------------------------------------------------------------------------
# _clean_actor — valid human names pass through
# ---------------------------------------------------------------------------

class TestCleanActorHumanNames:
    @pytest.mark.parametrize("name, expected", [
        ("Sid", "Sid"),
        ("Siddhant", "Siddhant"),
        ("John Smith", "John Smith"),
        ("Riya", "Riya"),
        ("google", "Google"),  # not in tech terms — title-cased
    ])
    def test_human_name_passes(self, svc, name, expected):
        result = svc._clean_actor(name, [])
        assert result == expected

    def test_self_reference_still_rejected(self, svc):
        assert svc._clean_actor("me", []) is None
        assert svc._clean_actor("myself", []) is None

    def test_composite_still_rejected(self, svc):
        assert svc._clean_actor("Sid/Riya", []) is None
        assert svc._clean_actor("Sid,Riya", []) is None


# ---------------------------------------------------------------------------
# Tech-actor rescue in _normalize()
# ---------------------------------------------------------------------------

class TestTechActorRescue:
    def test_tech_actor_rescued_as_topic_when_topic_null(self, svc):
        result = svc._normalize(_raw(actor="Python"), "Discuss Python migration")
        assert result["actor"] is None
        assert result["topic"] == "Python"

    def test_tech_actor_rescue_uses_canonical_capitalisation(self, svc):
        result = svc._normalize(_raw(actor="postgresql"), "PostgreSQL migration")
        assert result["actor"] is None
        assert result["topic"] == "PostgreSQL"

    def test_tech_actor_rescue_uses_canonical_capitalisation_k8s(self, svc):
        # k8s maps to Kubernetes in TECH_MAP
        result = svc._normalize(_raw(actor="k8s"), "k8s cluster setup")
        assert result["actor"] is None
        assert result["topic"] == "Kubernetes"

    def test_noise_actor_not_rescued(self, svc):
        result = svc._normalize(_raw(actor="Mock"), "Mock test discussion")
        assert result["actor"] is None
        assert result["topic"] is None  # noise words have no canonical rescue

    def test_rescue_does_not_override_existing_topic(self, svc):
        result = svc._normalize(
            _raw(actor="Python", topic="FastAPI"),
            "FastAPI and Python"
        )
        assert result["actor"] is None
        assert result["topic"] == "FastAPI"  # existing topic preserved

    def test_rescue_repair_logged(self, svc):
        # The rescue appends to repairs; repairs are logged at WARNING.
        # We verify the final result is correct; log inspection is via pytest -s.
        result = svc._normalize(_raw(actor="Docker"), "Docker container setup")
        assert result["topic"] == "Docker"

    def test_no_rescue_when_actor_is_noise_and_topic_is_none(self, svc):
        result = svc._normalize(_raw(actor="Unprocessable"), "422 error")
        assert result["actor"] is None
        assert result["topic"] is None

    def test_rescue_fires_only_when_actor_was_suppressed_as_tech_term(self, svc):
        # "team" is not in _ACTOR_TECH_TERMS or _ACTOR_NOISE_WORDS.
        # _clean_actor() does not check _ACTOR_GENERIC_WORDS (that set is used
        # only in _extract_with_rules() for rule-based inference, not here).
        # "team" passes through as "Team"; rescue does not fire.
        result = svc._normalize(_raw(actor="team"), "team discussion")
        assert result["actor"] == "Team"
        assert result["topic"] is None  # rescue only fires for suppressed tech terms
