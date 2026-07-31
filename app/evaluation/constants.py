"""
Evaluation framework constants.

All values are derived directly from production source:
- IntentExtractionService.INTENT_TYPES
- IntentCategoryService (category names)
- EmbeddingService / ChunkService (model name)

Nothing here is invented; every constant has a reference.
"""

# --- Intent types ----------------------------------------------------------
# Source: IntentExtractionService.INTENT_TYPES
VALID_INTENT_TYPES: frozenset[str] = frozenset({
    "communication",
    "todo",
    "study",
    "reminder",
    "idea",
    "reference",
    "question",
    "event",
    "general",
})

# --- Embedding model -------------------------------------------------------
# Source: EmbeddingService.MODEL_NAME / ChunkService.MODEL_NAME
EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

# --- Retrieval defaults ----------------------------------------------------
# Source: ChunkService.retrieve_hybrid / EmbeddingService.search_notes
# DEFAULT_HYBRID_LIMIT raised from 5 to 20 after pool-size experiment (2026-07-29).
# Experiment showed pool=20 (ann_pool=80) yields Hit Rate@5=0.760 vs 0.740 at pool=5
# at only 1.04x latency cost. See evaluation_results/pool_experiment/ANALYSIS.md.
DEFAULT_RETRIEVAL_LIMIT: int = 5
DEFAULT_HYBRID_LIMIT: int = 20
DEFAULT_SEMANTIC_LIMIT: int = 5

DEFAULT_INTENT_LIMIT = 5
  # limit used by EmbeddingService.search_notes

# --- Evaluation defaults ---------------------------------------------------
DEFAULT_K: int = 5                  # K for Precision@K and Recall@K
LATENCY_P95_PERCENTILE: float = 95.0

# --- Benchmark file --------------------------------------------------------
BENCHMARK_FILE_NAME: str = "benchmark.json"

# --- Difficulty levels (used in benchmark.json) ----------------------------
DIFFICULTY_EASY: str = "easy"
DIFFICULTY_MEDIUM: str = "medium"
DIFFICULTY_HARD: str = "hard"
VALID_DIFFICULTY_LEVELS: frozenset[str] = frozenset({
    DIFFICULTY_EASY,
    DIFFICULTY_MEDIUM,
    DIFFICULTY_HARD,
})
