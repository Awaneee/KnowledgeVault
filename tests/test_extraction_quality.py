"""
EXTR-007 — compute_extraction_quality() unit tests.

All tests are pure Python: no LLM call, no database, no network.
Tests cover the four sub-score components (intent, topic, actor, consistency)
and the final composite score, plus boundary and edge-case inputs.
"""
from __future__ import annotations

import pytest

from app.services.intent_extraction_service import IntentExtractionService


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _intent(
    intent_type="reference",
    topic="PostgreSQL",
    actor=None,
    obj="indexing strategies",
    confidence=0.9,
    model_name="gemini",
) -> dict:
    return {
        "intent_type": intent_type,
        "topic": topic,
        "actor": actor,
        "object": obj,
        "confidence": confidence,
        "model_name": model_name,
    }


def score(**kwargs) -> float:
    return IntentExtractionService.compute_extraction_quality(_intent(**kwargs))


# ---------------------------------------------------------------------------
# Return-type and range contract
# ---------------------------------------------------------------------------

class TestReturnContract:
    def test_returns_float(self):
        assert isinstance(score(), float)

    def test_score_in_unit_interval(self):
        assert 0.0 <= score() <= 1.0

    def test_empty_dict_does_not_raise(self):
        result = IntentExtractionService.compute_extraction_quality({})
        assert 0.0 <= result <= 1.0

    def test_result_rounded_to_4dp(self):
        result = score()
        assert result == round(result, 4)

    def test_score_is_clamped_at_1(self):
        # Perfect inputs should not exceed 1.0
        result = score(
            intent_type="reference",
            topic="Docker",
            actor=None,
            obj="container networking",
            confidence=1.0,
            model_name="gemini",
        )
        assert result <= 1.0

    def test_score_is_clamped_at_0(self):
        # Worst-case inputs should not go below 0.0
        result = score(
            intent_type="general",
            topic=None,
            actor=None,
            obj=None,
            confidence=0.0,
            model_name="heuristic",
        )
        assert result >= 0.0


# ---------------------------------------------------------------------------
# Intent quality sub-score
# ---------------------------------------------------------------------------

class TestIntentQuality:
    def test_general_intent_lower_than_specific(self):
        specific = score(intent_type="study", confidence=0.85)
        general = score(intent_type="general", confidence=0.85)
        assert general < specific

    def test_low_confidence_penalises_score(self):
        high_conf = score(confidence=0.9)
        low_conf = score(confidence=0.3)
        assert low_conf < high_conf

    def test_heuristic_model_penalises_score(self):
        llm = score(model_name="gemini")
        heuristic = score(model_name="heuristic")
        assert heuristic < llm

    def test_heuristic_fast_penalises_score(self):
        llm = score(model_name="gemini")
        heuristic_fast = score(model_name="heuristic-fast")
        assert heuristic_fast < llm

    def test_confidence_below_07_penalty_is_proportional(self):
        # At conf=0.5: penalty = (0.7 - 0.5) * 0.6 = 0.12; at conf=0.6: 0.06
        low = score(confidence=0.5, intent_type="study")
        mid = score(confidence=0.6, intent_type="study")
        assert low < mid

    def test_confidence_at_threshold_no_penalty(self):
        # No confidence penalty when conf == 0.7
        at_threshold = score(confidence=0.70, intent_type="study", model_name="gemini")
        above = score(confidence=0.71, intent_type="study", model_name="gemini")
        # Scores should be equal or very close (within float rounding)
        assert abs(at_threshold - above) < 0.01


# ---------------------------------------------------------------------------
# Topic quality sub-score
# ---------------------------------------------------------------------------

class TestTopicQuality:
    def test_no_topic_lowest_topic_score(self):
        with_topic = score(topic="Docker")
        without_topic = score(topic=None)
        assert without_topic < with_topic

    def test_known_tech_topic_highest(self):
        tech = score(topic="Docker")
        unknown = score(topic="SomeRandomDomain")
        assert tech >= unknown

    def test_multi_word_topic_high(self):
        multi = score(topic="System Design")
        short_unknown = score(topic="Xyz")
        assert multi > short_unknown

    def test_four_char_topic_reasonable(self):
        result = score(topic="Auth")
        assert result > 0.3

    def test_very_short_topic_low(self):
        # A single unknown 1-char topic gets the ≤2 short-token path (0.30)
        # Use a 2-char unknown word; known acronyms like "ai" bypass this
        result = score(topic="Zz")
        assert result < score(topic="Docker")

    def test_known_tech_terms_score_full_topic(self):
        for tech in ["redis", "postgresql", "docker", "kafka", "react"]:
            result = IntentExtractionService.compute_extraction_quality(
                {"intent_type": "reference", "topic": tech, "actor": None,
                 "object": "something", "confidence": 0.9, "model_name": "gemini"}
            )
            # Topic sub-score should be 1.0, contributing 0.35 to a score > 0.5
            assert result > 0.5, f"Known tech {tech!r} should produce score > 0.5"


# ---------------------------------------------------------------------------
# Actor quality sub-score
# ---------------------------------------------------------------------------

class TestActorQuality:
    def test_null_actor_ok_for_non_communication(self):
        # actor_q = 0.8 for non-communication; actor_q = 0.1 for communication
        non_comm = score(intent_type="study", actor=None)
        comm = score(intent_type="communication", actor=None)
        assert non_comm > comm

    def test_tech_term_as_actor_penalises_score(self):
        no_actor = score(intent_type="study", actor=None)
        tech_actor = score(intent_type="study", actor="docker")
        assert tech_actor < no_actor

    def test_valid_person_name_high_actor_score(self):
        with_name = score(intent_type="communication", actor="Sid")
        without = score(intent_type="communication", actor=None)
        assert with_name > without

    def test_multi_word_name_reasonable(self):
        two_words = score(intent_type="communication", actor="John Doe")
        assert two_words > 0.3

    def test_more_than_3_word_actor_lower(self):
        long_actor = score(intent_type="communication", actor="John Doe Smith Jr")
        short_actor = score(intent_type="communication", actor="John")
        assert long_actor < short_actor

    def test_tech_actor_case_insensitive(self):
        upper = score(actor="Docker")
        lower = score(actor="docker")
        assert upper == lower


# ---------------------------------------------------------------------------
# Consistency sub-score
# ---------------------------------------------------------------------------

class TestConsistencyQuality:
    def test_high_confidence_nothing_extracted_penalised(self):
        # conf > 0.6 and topic=None, actor=None, obj=None → consistency_q = 0.3
        inconsistent = IntentExtractionService.compute_extraction_quality({
            "intent_type": "reference",
            "topic": None,
            "actor": None,
            "object": None,
            "confidence": 0.9,
            "model_name": "gemini",
        })
        consistent = score(confidence=0.9)  # has topic + object
        assert inconsistent < consistent

    def test_low_confidence_nothing_extracted_not_penalised(self):
        # conf <= 0.6 with null fields → consistency_q = 0.9
        low_conf_null = IntentExtractionService.compute_extraction_quality({
            "intent_type": "general",
            "topic": None,
            "actor": None,
            "object": None,
            "confidence": 0.5,
            "model_name": "gemini",
        })
        # Should not be penalised by consistency; overall score limited by intent/topic only
        high_conf_null = IntentExtractionService.compute_extraction_quality({
            "intent_type": "general",
            "topic": None,
            "actor": None,
            "object": None,
            "confidence": 0.9,
            "model_name": "gemini",
        })
        assert low_conf_null > high_conf_null

    def test_any_one_field_satisfies_consistency(self):
        only_topic = IntentExtractionService.compute_extraction_quality({
            "intent_type": "reference",
            "topic": "Docker",
            "actor": None,
            "object": None,
            "confidence": 0.9,
            "model_name": "gemini",
        })
        none_extracted = IntentExtractionService.compute_extraction_quality({
            "intent_type": "reference",
            "topic": None,
            "actor": None,
            "object": None,
            "confidence": 0.9,
            "model_name": "gemini",
        })
        assert only_topic > none_extracted


# ---------------------------------------------------------------------------
# Composite score ordering
# ---------------------------------------------------------------------------

class TestCompositeOrdering:
    def test_ideal_extraction_scores_high(self):
        result = score(
            intent_type="reference",
            topic="Docker",
            actor=None,
            obj="container networking",
            confidence=0.92,
            model_name="gemini",
        )
        assert result >= 0.75

    def test_heuristic_fallback_scores_low(self):
        result = score(
            intent_type="general",
            topic=None,
            actor=None,
            obj=None,
            confidence=0.55,
            model_name="heuristic",
        )
        assert result < 0.4

    def test_partial_extraction_mid_range(self):
        # "Networking" is not a known tech term and is a single word ≥4 chars,
        # so topic_q=0.70. With study/gemini/0.65 confidence this lands mid-range.
        result = score(
            intent_type="study",
            topic="Networking",
            actor=None,
            obj=None,
            confidence=0.65,
            model_name="gemini",
        )
        assert 0.3 < result < 0.95

    def test_communication_with_actor_higher_than_without(self):
        with_actor = score(
            intent_type="communication",
            topic=None,
            actor="Sid",
            obj="internship",
            confidence=0.95,
        )
        without_actor = score(
            intent_type="communication",
            topic=None,
            actor=None,
            obj="internship",
            confidence=0.95,
        )
        assert with_actor > without_actor


# ---------------------------------------------------------------------------
# Weight sanity: verify the published 35/35/15/15 split is enforced
# ---------------------------------------------------------------------------

class TestWeightSanity:
    def test_topic_and_intent_weights_dominant(self):
        # A result with great topic+intent but poor actor+consistency should
        # still score higher than one with great actor+consistency but poor topic+intent
        topic_intent_dominant = IntentExtractionService.compute_extraction_quality({
            "intent_type": "reference",  # good intent_q
            "topic": "Docker",           # topic_q = 1.0
            "actor": "John Doe Smith Jr Extra",  # actor_q = 0.6 (>3 words)
            "object": None,              # consistency_q = 0.9 (topic present)
            "confidence": 0.9,
            "model_name": "gemini",
        })
        actor_consistency_dominant = IntentExtractionService.compute_extraction_quality({
            "intent_type": "general",    # intent_q penalised
            "topic": None,               # topic_q = 0.0
            "actor": "Sid",              # actor_q = 0.9 (communication=False, so actor_q 0.9)
            "object": "something",       # consistency_q = 0.9
            "confidence": 0.9,
            "model_name": "gemini",
        })
        assert topic_intent_dominant > actor_consistency_dominant


# ---------------------------------------------------------------------------
# Edge cases / robustness
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_missing_confidence_defaults_to_05(self):
        result = IntentExtractionService.compute_extraction_quality({
            "intent_type": "reference",
            "topic": "Docker",
            "actor": None,
            "object": "networking",
        })
        assert 0.0 <= result <= 1.0

    def test_none_confidence_defaults_to_05(self):
        result = IntentExtractionService.compute_extraction_quality({
            "intent_type": "reference",
            "topic": "Docker",
            "actor": None,
            "object": "networking",
            "confidence": None,
        })
        assert 0.0 <= result <= 1.0

    def test_string_confidence_zero_handled(self):
        # confidence field absent — uses 0.5 default
        result = IntentExtractionService.compute_extraction_quality({
            "intent_type": "study",
            "topic": "Python",
            "actor": None,
            "object": "generators",
        })
        assert 0.0 <= result <= 1.0

    def test_unknown_model_name_no_penalty(self):
        known = score(model_name="gemini")
        unknown = score(model_name="some-other-model")
        # No penalty for non-heuristic models
        assert known == unknown

    def test_deterministic_same_input(self):
        payload = _intent()
        assert (
            IntentExtractionService.compute_extraction_quality(payload)
            == IntentExtractionService.compute_extraction_quality(payload)
        )

    def test_called_as_classmethod(self):
        result = IntentExtractionService.compute_extraction_quality(_intent())
        assert 0.0 <= result <= 1.0
