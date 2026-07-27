"""
Ask evaluation data models.

Pure Pydantic — no SQLAlchemy, no database tables.
All timing fields are in milliseconds.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Root-cause classification for failed / low-quality evaluations
# ---------------------------------------------------------------------------

class FailureRootCause(str, Enum):
    """
    Taxonomy of root causes for low-quality evaluation results.

    RETRIEVAL_FAILURE      — relevant notes were not retrieved (recall miss)
    INSUFFICIENT_CONTEXT   — relevant notes retrieved but content lacks
                             the specific information needed to answer
    HALLUCINATION          — answer contains facts not present in context
    PROMPT_CONSTRUCTION    — answer is malformed / off-topic despite good context
    EVALUATOR_FAILURE      — judge returned malformed JSON or crashed
    UNKNOWN                — quality is low but no specific cause identified
    """
    RETRIEVAL_FAILURE    = "retrieval_failure"
    INSUFFICIENT_CONTEXT = "insufficient_context"
    HALLUCINATION        = "hallucination"
    PROMPT_CONSTRUCTION  = "prompt_construction"
    EVALUATOR_FAILURE    = "evaluator_failure"
    UNKNOWN              = "unknown"


# ---------------------------------------------------------------------------
# Gold dataset entry
# ---------------------------------------------------------------------------

class GoldAskQuery(BaseModel):
    """
    A single entry in the gold evaluation dataset.

    Fields
    ------
    id                  Unique identifier for this entry.
    question            Natural-language question sent to the Ask endpoint.
    expected_note_ids   DB note IDs whose content should inform the answer.
    reference_answer    Ground-truth reference answer for correctness scoring.
    category            One of: factual_lookup, reminders, appointments,
                        communication, shopping, study, ideas,
                        multi_note_synthesis, summarization, comparison.
    difficulty          easy | medium | hard
    eval_notes          Optional instructions for the judge (e.g. partial credit rules).
    """
    id: str
    question: str
    expected_note_ids: list[int] = Field(default_factory=list)
    reference_answer: str
    category: str
    difficulty: str = "medium"
    eval_notes: str = ""


# ---------------------------------------------------------------------------
# Judge output
# ---------------------------------------------------------------------------

class JudgeScores(BaseModel):
    """
    Structured evaluation output returned by the LLM judge.
    All scores are in [0.0, 1.0].
    """
    correctness: float = Field(ge=0.0, le=1.0)
    groundedness: float = Field(ge=0.0, le=1.0)
    faithfulness: float = Field(ge=0.0, le=1.0)
    hallucination: float = Field(ge=0.0, le=1.0)
    completeness: float = Field(ge=0.0, le=1.0)
    overall: float = Field(ge=0.0, le=1.0)
    justification: str
    hallucinated_claims: list[str] = Field(default_factory=list)
    ungrounded_claims: list[str] = Field(default_factory=list)

    @property
    def weighted_overall(self) -> float:
        """
        Weighted composite score (alternative to the judge's own 'overall').

        Weights are biased toward correctness and groundedness because
        these directly measure safety and usefulness.

          correctness   × 0.30
          groundedness  × 0.25
          faithfulness  × 0.20
          completeness  × 0.15
          hallucination × 0.10   (already 1.0 = no hallucination)
        """
        return (
            self.correctness   * 0.30
            + self.groundedness  * 0.25
            + self.faithfulness  * 0.20
            + self.completeness  * 0.15
            + self.hallucination * 0.10
        )


# ---------------------------------------------------------------------------
# Per-query evaluation result
# ---------------------------------------------------------------------------

class ChunkArtifact(BaseModel):
    """Serialisable snapshot of a single retrieved chunk."""
    note_id: int
    note_title: str
    chunk_text: str
    chunk_index: int
    score: float
    semantic_score: float
    intent_score: float
    intent_category: Optional[str] = None


class AskEvalResult(BaseModel):
    """
    Full evaluation result for a single gold query.

    Preserves all artifacts required for deterministic post-hoc debugging.
    """
    # Identity
    query_id: str
    question: str
    category: str
    difficulty: str

    # Answer artifacts
    answer: str
    reference_answer: str
    status: str                      # ok | no_results | degraded
    retrieval_only: bool

    # Retrieval artifacts
    retrieved_note_ids: list[int]
    expected_note_ids: list[int]
    retrieved_chunks: list[ChunkArtifact]
    filtered_chunk_count: int

    # Context
    prompt: str

    # Judge scores (None if evaluator failed)
    scores: Optional[JudgeScores] = None
    root_cause: Optional[FailureRootCause] = None

    # Retrieval quality (computed locally, no LLM)
    recall_at_expected: float        # fraction of expected_note_ids in retrieved top-8
    context_utilisation: float       # estimated fraction of chunks referenced in answer

    # Latency
    retrieval_ms: float
    llm_ms: float
    total_ms: float

    # Cost
    estimated_prompt_tokens: int
    estimated_completion_tokens: int
    estimated_cost_usd: float

    # Error from judge or pipeline
    error: Optional[str] = None


# ---------------------------------------------------------------------------
# Aggregate report
# ---------------------------------------------------------------------------

class CategorySummary(BaseModel):
    """Aggregated metrics for one question category."""
    category: str
    query_count: int
    avg_correctness: float
    avg_groundedness: float
    avg_faithfulness: float
    avg_hallucination: float
    avg_completeness: float
    avg_overall: float
    avg_total_ms: float


class AskEvalReport(BaseModel):
    """
    Top-level evaluation report for the Ask endpoint.
    """
    run_id: str
    created_at: str                  # ISO-8601
    total_queries: int

    # Overall averages
    avg_correctness: float
    avg_groundedness: float
    avg_faithfulness: float
    avg_hallucination: float
    avg_completeness: float
    avg_overall: float
    avg_retrieval_ms: float
    avg_llm_ms: float
    avg_total_ms: float
    total_estimated_cost_usd: float

    # Per-category breakdown
    category_summaries: list[CategorySummary]

    # Ranked lists
    hardest_queries: list[str]       # query IDs with lowest overall score
    easiest_queries: list[str]       # query IDs with highest overall score

    # Root-cause distribution
    root_cause_counts: dict[str, int]

    # All individual results
    results: list[AskEvalResult]
