# Design: Production-Grade Retrieval Evaluation Framework

**Status:** Proposed — awaiting approval before implementation  
**Sprint:** 2-C  
**Date:** 2026-07-28  
**Author:** Awane  

---

## 1. Current Benchmark Architecture

### What exists today

The framework has two separate evaluation pipelines that do not share infrastructure:

**Pipeline A — Retrieval evaluation** (`scripts/evaluate.py` + `app/evaluation/`)

```
BenchmarkLoader.load(benchmark.json)
    ↓
EvaluationRunner
    ├── SemanticAdapter   → EmbeddingService.search_notes()
    ├── IntentAdapter     → IntentCategoryService.find_categories_for_query()
    ├── HybridAdapter     → ChunkService.retrieve_hybrid()
    └── RerankAdapter     → ChunkService.retrieve_hybrid() + RerankingService.rerank()
    ↓
QueryEvaluation (per query, per strategy)
    ├── precision_at_k, recall_at_k, hit_rate, mrr, ndcg_at_k
    ├── intent_correct, category_correct
    └── latency_ms
    ↓
StrategySummary (aggregate per strategy)
    ↓
EvaluationReport → MarkdownReport, CSVReport, ConsoleReport
```

**Pipeline B — Ask / RAG evaluation** (`scripts/evaluate_ask.py` + `app/evaluation/ask/`)

```
gold_dataset.json
    ↓
AskEvaluationRunner
    ├── AskService.ask_with_context()    (live LLM call)
    ├── AskJudge (LLM-as-judge via Gemini)
    └── Root cause classification rules
    ↓
JudgeScores (correctness, groundedness, faithfulness, hallucination, completeness)
    ↓
AskEvalReport → AskMarkdownReport, AskCSVReport
```

### Source files

| File | Role |
|---|---|
| `app/evaluation/benchmark/benchmark.json` | 50 hand-crafted retrieval queries with `relevant_note_ids` |
| `app/evaluation/benchmark/loader.py` | Pydantic-validated JSON loader |
| `app/evaluation/models.py` | `BenchmarkQuery`, `RetrievalResult`, `QueryEvaluation`, `StrategySummary`, `EvaluationReport` |
| `app/evaluation/runner.py` | Orchestrates adapters; computes all metrics; exports CSV + MD |
| `app/evaluation/adapters/` | One per retrieval strategy; all extend `BaseRetrievalAdapter` |
| `app/evaluation/metrics/retrieval.py` | `precision_at_k`, `recall_at_k`, `reciprocal_rank`, `hit_rate`, `ndcg_at_k`, `mean_mrr` |
| `app/evaluation/metrics/classification.py` | `intent_accuracy`, `category_accuracy`, `canonicalize_category_name` |
| `app/evaluation/metrics/latency.py` | `average_latency`, `median_latency`, `p95_latency`, `max_latency` |
| `app/evaluation/reports/` | Markdown, CSV, Console renderers |
| `scripts/generate_benchmarks.py` | Programmatic generator using keyword matching over live notes |
| `app/evaluation/ask_benchmark/gold_dataset.json` | ~20 hand-written ask queries with reference answers |

### What the benchmark measures well today

- Recall@K, Precision@K, MRR, nDCG@K across four strategies on 50 queries
- Intent and category classification accuracy alongside retrieval accuracy
- Per-query latency with P95 and max tracking
- Per-query CSV output suitable for offline analysis in pandas/Excel
- Strategy comparison reports in Markdown for sprint-level review

---

## 2. Weaknesses in the Current Corpus

Evidence for each weakness is cited from repository artifacts.

### W1 — Corpus coverage is 4.6%

`benchmark.json` references 49 unique note IDs out of 1055 ingested notes (`sprint1_after/CATEGORY_ANALYSIS.md` line 9: "Total Notes: 1055"). That is 4.6% of the corpus. The 1,006 un-evaluated notes are invisible to every benchmark run. A regression that damages recall for notes in the "Questions - Python" cluster (23 notes, `sprint1_after/CATEGORY_ANALYSIS.md` line 57) would not be detected.

### W2 — Note reference concentration

Of the 49 referenced notes, 26 appear in 3 or more queries. Note 89 appears in 6 queries, notes 86, 87, 77, 91, 78, 79, 54, 106, 107 each appear in 4 queries. A retrieval change that specifically helps or hurts note 89 produces an outsized effect on the benchmark score (6/129 = 4.7% of all (query, note) pairs), masking whether the change is generally beneficial.

### W3 — Intent distribution is severely skewed

`benchmark.json` contains 17 `todo` queries (34%), 8 `study` queries (16%), 8 `reference` queries (16%), and only 1 `project` query and 0 `general` queries. The intent type with the most notes in the corpus (`general`: 38 notes in "General" category alone, plus hundreds in the "Tasks" catch-all) is under-represented. The `event` and `reminder` intents have 0 queries each.

### W4 — Difficulty is heavily skewed toward easy

33/50 queries are `easy` (66%), 15 are `medium` (30%), 2 are `hard` (4%). The two hard queries are ID 28 ("How to set up a kubernetes cluster") and ID 36 ("Redis and PostgreSQL reference notes"). There are no queries testing:
- Lexical gap (user phrase has no keyword overlap with note text)
- Disambiguation (multiple notes match superficially but only one is relevant)
- Negative retrieval (the correct answer is "no relevant notes")
- Cross-note synthesis (relevant information is distributed across 4+ notes)

### W5 — Relevance labels are unverified

`relevant_note_ids` in `benchmark.json` were assigned manually by the developer. There is no documentation of the labeling criteria, no second reviewer, and no inter-annotator agreement score. For 10 queries, only 1 note is labeled relevant (IDs: 8, 15, 17, 18, 21, 41, and others) — a single-note ground truth is fragile: if that note ID changes or the note is re-indexed, the query becomes unscoreable. The `gold_dataset.json` for pipeline B has the same issue.

### W6 — Relevance is binary, not graded

`BenchmarkQuery.relevant_note_ids` is a flat list — every listed note is treated as equally relevant. In practice, for a query like "What are the project requirements for KnowledgeVault?" (ID 32, 8 relevant notes), note 89 (which contains the original specification) is more relevant than note 96 (which mentions the project tangentially). Binary relevance conflates these, making nDCG meaningless as a graded metric and making it impossible to detect whether the system ranks the best result at position 1 vs position 5.

### W7 — No negative queries

There are zero benchmark entries where the correct answer is "no notes are relevant." The retrieval pipeline has a `RETRIEVAL_MIN_SCORE = 0.10` filter (`config.py:65`) specifically designed to handle this case, but that path is never exercised by any benchmark query. A change that lowers the threshold and causes noise to appear in results would be invisible to the current benchmark.

### W8 — The auto-generator uses heuristic relevance assignment

`generate_benchmarks.py` assigns `relevant_note_ids` via `find_notes()` which does simple substring keyword matching (`text.lower()` contains keyword, line 67). This produces false positives — a note about "Redis eviction policy" would be included in the relevant set for "What is LRU cache?" even if the note never actually explains LRU. The function's `min_match=1` default means a single incidental keyword mention qualifies a note. The generator is aware of this: its comment at line 154 says "keyword matching over 1000 notes produces very large candidate lists." The cap of `[:10]` is applied but the false positive problem remains.

### W9 — No paraphrase pairs for semantic robustness testing

Queries 22 and 29 both ask for "Things to tell Sid" in slightly different phrasing and point to the same relevant set. This is the only paraphrase pair in the benchmark. A truly robust retrieval system should return the same results regardless of surface phrasing. No systematic paraphrase coverage exists for the other 48 queries, making it impossible to measure semantic robustness.

### W10 — Category labels drift over time

`expected_category` in `benchmark.json` uses labels like "Things to Tell Sid", "Meetings", "Questions", "Reference Notes" which do not match the actual category names produced by the pipeline (e.g., "Communication - Sid", "Meetings - Social", "Questions - Python"). The `canonicalize_category_name()` function in `classification.py` compensates for this drift with 100+ lines of ad-hoc normalization, but that function itself is a smell: the benchmark ground truth is incorrect and being papered over at evaluation time.

### W11 — No cross-strategy significance testing

The benchmark runner in `runner.py` computes per-strategy means but performs no statistical significance test. In Sprint 2-B, RERANK was approved over HYBRID based on a 0.017 MRR difference on 50 queries. That difference is within expected noise for n=50 and was, as later discovered, not from the reranker at all. A Wilcoxon signed-rank test or bootstrap confidence interval on the per-query MRR distributions would have flagged this immediately.

### W12 — No stale note detection

The benchmark references note IDs that are encoded at the time the benchmark was written. The `Note.id` column is a database auto-increment integer (`models/notes.py`). If a user's database is re-seeded, the note IDs change and the benchmark becomes silently invalid — it will still run, but relevance labels no longer match the correct notes. The Sprint 2-B benchmark confusion (cross-encoder appearing to improve things) was partly caused by exactly this: the evaluation assumed note ID 89 was the "semantic search spec note" but after re-indexing it could be something entirely different.

---

## 3. Query Taxonomy

The proposed taxonomy organizes queries along three axes: **retrieval challenge**, **surface form**, and **information need type**. Every benchmark query should be tagged with one value from each axis.

### Axis A — Retrieval challenge

| Tag | Definition | Example |
|---|---|---|
| `lexical` | Surface keywords appear in the note | "Redis eviction policy" → note titled "Redis" |
| `semantic` | Meaning match but no keyword overlap | "What am I working on for health?" → note titled "Doctor appointment" |
| `lexical_gap` | User phrase shares no tokens with relevant note | "Things to remember for tomorrow" → note titled "Grocery list" |
| `ambiguous` | Multiple valid relevant sets; no single correct answer | "My project notes" |
| `negative` | No relevant notes exist for this query | "Notes about Rust programming" (if no Rust notes) |
| `multi_hop` | Relevant answer requires combining 3+ distinct notes | "Summarize my interview prep strategy" |
| `temporal` | Recency or date-relative phrasing | "What am I doing this week?" |
| `comparison` | Asks to contrast two entities from separate notes | "Redis vs Kafka" |
| `synthesis` | Category or theme summarization | "All my health notes" |
| `exact_phrase` | Contains a verbatim phrase from a note | "BRPOPLPUSH" |

### Axis B — Surface form

| Tag | Definition | Example |
|---|---|---|
| `natural_question` | Full grammatical question | "How does Redis eviction work?" |
| `keyword_phrase` | Noun phrase without verb | "Redis eviction" |
| `imperative` | Command form | "Show my finance reminders" |
| `paraphrase` | Rephrasing of another benchmark query | Same intent as an existing query, different words |

### Axis C — Information need type (from existing `expected_intent`)

`idea`, `study`, `reference`, `todo`, `communication`, `meeting`, `project`, `question`, `reminder`, `event`, `general`

### Coverage targets for a healthy benchmark

| Challenge tag | Minimum share |
|---|---|
| `lexical` | 20–30% |
| `semantic` | 25–35% |
| `lexical_gap` | 10–15% |
| `negative` | 5–10% |
| `multi_hop` | 10–15% |
| `comparison` | 5–10% |
| `synthesis` | 5–10% |
| `exact_phrase` | 5–10% |
| `ambiguous` + `temporal` | ≥ 5% each |

All 11 intent types should have at least 3 queries each. Difficulty should be approximately 25% easy / 50% medium / 25% hard.

---

## 4. Corpus Taxonomy

The 1055-note corpus is not random. Its structure determines what the benchmark can and cannot detect. Understanding corpus taxonomy is a prerequisite for designing evaluation queries that probe the system's actual weak points.

### Note taxonomy dimensions

**By content density** (evidence: `sprint1_after/CATEGORY_ANALYSIS.md`):

| Cluster | Example category | Notes | Evaluation gap |
|---|---|---|---|
| Task / reminder | "Tasks" (229 notes) | 21.7% | Notes are short, specific, often single-line |
| General catch-all | "General" (38 notes) | 3.6% | High conceptual overlap with other clusters |
| Reference cheat-sheet | "Reference - Redis", "Reference - Docker" | ~20 notes | Dense factual content, retrieval should be precise |
| Study notes | 20 study categories, mostly singletons | ~25 notes | Singleton categories create retrieval sparsity |
| Communication | "Communication - Sid" (3 notes) | <5 notes | Requires person/actor disambiguation |
| Ideas | "Ideas - AI" etc. (8 idea categories) | ~10 notes | Creative / open-ended intent, hard to benchmark |

**By note age** (not currently tracked): Notes have an `id` auto-increment that encodes rough insertion order. The benchmark does not account for temporal relevance — "recent notes" queries have no valid ground truth because recency is not a note attribute.

**By note length**: The corpus mixes single-line reminders ("Don't forget to buy milk") with multi-paragraph reference notes. The embedding model (`all-MiniLM-L6-v2`, 384d) compresses both to the same dimensionality. Length disparity affects retrieval quality but is not modeled in any current metric.

**By uniqueness**: Of 105 categories, 69 are singletons (one note) — `sprint1_after/CATEGORY_ANALYSIS.md` line 17. A singleton category represents a topic where no paraphrase or related-note retrieval is possible. Benchmark queries targeting singleton topics should be labeled `negative_if_note_absent` to prevent measurement artifacts if the specific note gets deleted or re-indexed.

### Corpus health metrics to track

The benchmark framework should record, alongside retrieval metrics, the following corpus health statistics per run:

- Total note count, organized note count, failed note count
- Category count, singleton category count, fragmentation rate
- Median note length (tokens), P95 note length
- Age of oldest / newest note in the DB (proxy for corpus staleness)

These metrics are already computed by `scripts/analyze_categories.py` and `analyze_categories.py` but are not included in the retrieval evaluation report.

---

## 5. Relevance Labeling Strategy

### Current approach and its failure mode

Relevance is currently assigned by one person (the developer) without documented criteria, secondary review, or graded relevance. For `generate_benchmarks.py`, relevance is assigned purely by keyword presence — a provably incorrect proxy. The existing `write_benchmark_analysis.py` (line 278) already acknowledges this: "keyword matching... may miss notes where the same concept is expressed differently."

### Proposed three-tier relevance model

Replace binary relevance with three-tier graded relevance to enable proper nDCG computation and separate recall errors from ranking errors:

| Grade | Label | Definition |
|---|---|---|
| 2 | `highly_relevant` | Note directly and completely answers the query; if a user asked this question this note is what they want |
| 1 | `partially_relevant` | Note contains related information that may help the user but is not a complete answer |
| 0 | `not_relevant` | Note does not address the query (implicit for all unlisted notes) |

**JSON schema change** (no backward-breaking change — extends existing `BenchmarkQuery`):

```json
{
  "id": "22",
  "query": "Things I need to tell Sid",
  "relevant_note_ids": [54, 55, 56, 57],
  "graded_relevance": {
    "54": 2,
    "55": 2,
    "56": 2,
    "57": 1
  }
}
```

The existing `relevant_note_ids` list is retained as the set of all non-zero grades for backward compatibility with all current adapters and metrics.

### Labeling procedure

**For human-authored benchmark entries** (the correct path for production use):

1. **Draft**: Developer writes the query and an initial `relevant_note_ids` list based on knowledge of the corpus.
2. **Blind retrieval check**: Run all four retrieval strategies against the query. Inspect the union of all retrieved note IDs. If any retrieved note that is NOT in `relevant_note_ids` looks relevant on inspection, add it.
3. **Criteria checklist** (must be documented in each benchmark entry's `labeling_notes` field):
   - Why is each grade-2 note highly relevant? (1–2 sentences)
   - Are there notes that might seem relevant but should NOT be included? (negative examples)
4. **Second-pass review**: Any entry with a `relevant_note_ids` list of size 1 must be reviewed by a second reader (even if that is the same developer returning to it 48 hours later) to detect single-point-of-failure brittleness.
5. **Staleness TTL**: Add `labeled_at` (ISO date) and `note_ids_verified_at` timestamps to each entry. Any entry older than 90 days must be re-verified before being used in a benchmark gate decision.

**For auto-generated entries** (`generate_benchmarks.py`):

The keyword-matching generator should be demoted to a **candidate generator only** — its output requires human review before any entry enters the primary benchmark. Introduce two benchmark tiers:

- `benchmark/verified.json` — human-reviewed, used for gate decisions
- `benchmark/candidates.json` — auto-generated candidates, used for exploratory runs only

The runner should log which tier each entry came from and exclude `candidates.json` from gate evaluation by default.

---

## 6. Automatic Benchmark Generation

### What `generate_benchmarks.py` does well

The generator (`scripts/generate_benchmarks.py`) has strong query type coverage: it produces factual, paraphrased, multi-hop, temporal, comparison, synthesis, ambiguous, exact-keyword, and category-oriented queries (lines 487–583). The query templates are thoughtful and cover real user patterns. The ask benchmark generator produces rich reference answers with eval notes.

### What it does wrong

1. **Relevance by keyword presence** (`find_notes` at line 61): substring match. Returns notes that mention a keyword incidentally.
2. **No relevance verification**: the generator emits entries immediately without any checking that the matched notes are actually responsive to the query.
3. **Counter-based IDs** (`RetrievalEntry._counter`): IDs are re-assigned every time the script runs. Re-running with a different note count produces different ID assignments, making run-to-run comparison impossible.
4. **Notes capped at [:10]** (line 157): relevant set is truncated to the first 10 keyword matches, which may not be the 10 best matches.
5. **No query deduplication**: the generator can produce near-duplicate queries if multiple topic clusters expand to the same note IDs.

### Proposed auto-generation pipeline

The generator should become a multi-stage pipeline with explicit quality gates:

**Stage 1 — Corpus sampling** (replaces raw keyword matching):

```
For each note n in the corpus:
  1. Retrieve top-5 similar notes using note-level embeddings
  2. Generate 2 query templates per note using an LLM:
     - One keyword-style query (imperative or noun phrase)
     - One semantic-style query (natural language question)
  3. Assign note n as the primary relevant note (grade 2)
  4. Assign the top-2 semantically similar notes as partially relevant (grade 1)
     IF their semantic similarity score > 0.6
```

This produces queries that are grounded in actual note content rather than assumed keywords.

**Stage 2 — Retrieval-based relevance expansion**:

```
For each auto-generated query:
  1. Run retrieve_hybrid(limit=20)
  2. For each retrieved note r:
     - If r is not in the relevant set and similarity to note n > 0.65:
       tentatively add r as grade 1 (needs human review)
     - If r is in the relevant set at grade 2 and it appears at rank > 10:
       flag the query as a "hard" difficulty candidate
```

**Stage 3 — Deduplication**:

```
For each pair of auto-generated queries (q_a, q_b):
  - If embed(q_a) · embed(q_b) > 0.90: mark the lower-priority one as duplicate, exclude
```

**Stage 4 — Quality filter** (before output):

Remove any candidate where:
- The relevant set has 0 grade-2 notes
- The query is fewer than 3 tokens
- All relevant notes are in the same singleton category

**Stage 5 — Export to `benchmark/candidates.json`**

The output uses stable IDs (`{corpus_hash}_{note_id}_{query_index}`) rather than a counter, ensuring re-runs produce the same ID for the same (note, query) pair.

The existing `scripts/generate_benchmarks.py` can be refactored to implement these stages rather than being replaced wholesale.

---

## 7. Human Evaluation Support

### The gap

There is currently no human evaluation path — every labeling decision has been made by the developer alone. For a personal knowledge base, the developer is also the user, which creates a structural advantage over real evaluation: the developer knows which notes exist and what they say.

### Proposed human evaluation CLI

A new `scripts/human_eval.py` CLI implements an interactive relevance review workflow:

```
Usage:
  python scripts/human_eval.py --mode review --input benchmark/candidates.json
                                              --output benchmark/verified.json

For each candidate entry:
  QUERY: "Things I need to tell Sid"
  ─────────────────────────────────
  Retrieved by: SEMANTIC, HYBRID, RERANK

  Note 54 — "Communication - Sid"
  Preview: "Tell Sid about the hackathon registration form..."
  Score: HYBRID=0.81, SEMANTIC=0.74
  Relevance? [2=high / 1=partial / 0=not / s=skip / q=quit]: 2

  Note 423 — "Things to do"
  Preview: "1. Renew library card 2. Pay hostel fees..."
  Score: HYBRID=0.52, SEMANTIC=0.48
  Relevance? [2=high / 1=partial / 0=not / s=skip / q=quit]: 0

  [Entry approved / rejected] → writes to verified.json
```

The CLI shows the note's preview (first 300 chars), the scores from each retrieval strategy, and whether the note was already in the auto-generated candidate set. Progress is checkpointed: if the reviewer quits midway, already-reviewed entries are not re-shown.

### Annotation protocol

Each session should record:
- `reviewer_id` (from env var `REVIEWER_EMAIL` or prompting)
- `session_date`
- Time spent per entry
- A `disagreement_notes` field for entries where the reviewer initially chose a different grade and then revised it

For entries where the label is uncertain (the reviewer used `s=skip`), those entries are excluded from `verified.json` and placed in `benchmark/uncertain.json` for deferred resolution.

### Sampling strategy for human review

Given a corpus of 1055 notes, the priority order for human review:

1. **All queries referencing only 1 relevant note** (fragile ground truth) — 10 such queries in the current benchmark
2. **All queries in intent types with < 3 benchmark entries** (`project`, `event`, `reminder` currently)
3. **All auto-generated candidates in the top 5% most-referenced note cluster** (notes 54–57, 77–79, 89, 91, 106, 107 which already appear in 4–6 queries each)
4. **A random 10% sample** from the auto-generated candidate pool for accuracy calibration

---

## 8. Metrics

### Current metrics and their limitations

| Metric | Current status | Limitation |
|---|---|---|
| Precision@K | Computed | K is hardcoded to 5 in the constant `DEFAULT_K`; no multi-K sweep |
| Recall@K | Computed | Binary relevance only |
| Hit Rate@K | Computed | Equivalent to Precision@1 when relevant set is size 1; misleading for multi-relevant queries |
| MRR | Computed | Aggregated mean; no confidence interval; no per-difficulty breakdown |
| nDCG@K | Computed | Computed but binary relevance makes it a weaker version of Recall@K |
| Intent accuracy | Computed | Conflates all 9 intent types into one number |
| Category accuracy | Computed | `canonicalize_category_name` masks real prediction errors |
| Latency avg/P95 | Computed | Per-strategy; not split by query difficulty or note count |

### Proposed metric additions

**R-Precision**: Precision at K = |relevant set|. For queries with 4 relevant notes, Precision@4 is more meaningful than Precision@5 (which always dilutes with a non-relevant slot). Formula: `|retrieved[:len(relevant)] ∩ relevant| / len(relevant)`. This is a single-number summary less affected by relevant-set-size variation.

**Mean Average Precision (MAP)**: Averages Precision@K at each rank where a relevant note appears. More sensitive than MRR for queries with multiple relevant notes. Currently missing from `app/evaluation/metrics/retrieval.py`.

**Graded nDCG**: Once three-tier relevance is implemented (Section 5), nDCG gains its intended power. A grade-2 hit at rank 1 should score better than a grade-1 hit at rank 1. The metric already exists in `retrieval.py:ndcg_at_k` but the gain function must be updated to use `(2^grade - 1) / log2(rank + 1)` rather than binary.

**Retrieval Recall Stratified by Difficulty**: The current runner computes one MRR per strategy. Splitting by difficulty reveals whether a retrieval change helps easy queries at the expense of hard queries — a pattern invisible in aggregates.

**Confidence intervals (bootstrap)**: For each strategy comparison, report a 95% bootstrap CI on the MRR difference. Implemented in `scripts/evaluate.py` post-processing. If the CI includes zero, the difference is not significant.

**Intent-stratified accuracy**: Instead of one intent accuracy number, report accuracy per intent type. In the current benchmark, the HYBRID strategy achieves 0.460 intent accuracy overall, but this masks that `communication` intent (4 queries) might be 100% while `todo` intent (17 queries) might be 30%.

**Cache hit rate for reranking**: When `RERANKING_ENABLED=True`, the `RERANK` adapter should report what fraction of queries were served from the Redis score cache vs. required fresh inference. Currently logged but not included in the `StrategySummary` or any report.

**Corpus coverage**: `len(set(all_retrieved_note_ids)) / total_note_count` across a full benchmark run. The current benchmark only exercises 4.6% of the corpus. This metric should be a first-class field in `EvaluationReport`.

### K-sweep protocol

All metrics should be reported at K ∈ {1, 3, 5, 10} rather than only K=5. The `EvaluationRunner` should accept a `k_values: list[int]` parameter and produce one `StrategySummary` per (strategy, K) combination. This immediately reveals whether a retrieval improvement helps top-1 ranking (user sees first result) vs. top-5 recall (AskService context window).

---

## 9. Evaluation Dashboard

### Current state

The current reporting system produces:
- A Markdown file (`evaluation_report.md`) with per-query detail tables
- A CSV file (`evaluation_results.csv`) with one row per (query, strategy) pair
- Console output during the run

There is no time-series tracking, no trend visualization, and no way to compare two runs without manually diffing two Markdown files.

### Proposed dashboard architecture

The dashboard does not require a web server. It should be a **static HTML file generated as part of every benchmark run**, committed alongside the results. This approach has zero runtime dependencies and is always available at the commit URL.

**Report directory structure after each run:**

```
evaluation_results/
  {run_id}/
    evaluation_report.md      (existing)
    evaluation_results.csv    (existing)
    dashboard.html            (new)
    manifest.json             (new — metadata for history tracking)
```

**`manifest.json` schema:**

```json
{
  "run_id": "c1df0566",
  "created_at": "2026-07-28T20:10:32Z",
  "git_commit": "8316c96",
  "git_branch": "main",
  "corpus_note_count": 1055,
  "k": 5,
  "strategies": ["semantic", "hybrid", "rerank"],
  "summaries": {
    "hybrid": {"mrr": 0.602, "hit_rate": 0.740, "avg_latency_ms": 126.9},
    "rerank": {"mrr": 0.483, "hit_rate": 0.640, "avg_latency_ms": 423.5}
  }
}
```

**`dashboard.html` content** (generated by a new `scripts/generate_dashboard.py`):

1. **Header**: run ID, git commit, date, corpus size
2. **Strategy comparison table**: current run metrics side-by-side
3. **Trend chart**: MRR and Hit Rate for HYBRID over the last N runs (read from historical `manifest.json` files)
4. **Regression detector**: if current HYBRID MRR < previous HYBRID MRR - 0.03, display a red banner
5. **Per-query heat map**: 50 rows × 4 strategy columns, colored by reciprocal rank (green = rank 1, yellow = rank 3, red = miss)
6. **Failure analysis**: queries sorted by lowest MRR across all strategies (the hardest queries)
7. **Intent breakdown**: bar chart of hit rate per intent type

The dashboard uses only vanilla JavaScript + inline CSS — no external dependencies, no build step. It can be opened directly in a browser from the file system.

**Historical tracking**: The `scripts/generate_dashboard.py` script reads all `manifest.json` files found in `evaluation_results/*/manifest.json` and generates the trend chart from them. This requires no database — the filesystem is the history store.

---

## 10. Regression Testing

### The problem

The Sprint 2-B benchmark demonstrated the core regression problem: a retrieval change appeared to improve Hit Rate from 0.740 to 0.760, but the improvement was from an unintended side effect (expanded candidate pool from the benchmark adapter's `limit=20`), not from the intended change (cross-encoder reranking). This was detected only by post-hoc latency analysis.

### Proposed regression test contract

A **retrieval regression test** runs automatically after every pull request merge and blocks deployment if it fails. It must:

1. Run the full 50-query verified benchmark against all strategies
2. Report HYBRID MRR and Hit Rate
3. Fail if HYBRID MRR < `REGRESSION_GATE_MRR` or HYBRID Hit Rate < `REGRESSION_GATE_HIT_RATE`

These gate values are stored in a new file `evaluation_results/gates.json`:

```json
{
  "established_at": "2026-07-28",
  "established_from_run": "c1df0566",
  "HYBRID": {
    "mrr_floor": 0.580,
    "hit_rate_floor": 0.720
  },
  "SEMANTIC": {
    "mrr_floor": 0.590,
    "hit_rate_floor": 0.740
  }
}
```

The floor values are set at 3% below the best observed value for that strategy. This permits natural variance without false alarms while catching genuine regressions. When a strategy improvement clears a higher baseline, the gates file is updated manually with a PR — this forces a deliberate conversation about raising the bar.

### Latency gate

Every strategy must report average latency within its approved envelope:

| Strategy | Max avg latency | Evidence for cap |
|---|---|---|
| SEMANTIC | 100ms | Current avg: 2.7ms (warm DB), P95: ~50ms |
| HYBRID | 300ms | Current avg: 126.9ms |
| RERANK | 500ms | Current avg: 423.5ms (fresh inference) |

The latency caps include generous headroom because benchmark latencies run on a shared development machine and vary significantly between runs (SEMANTIC averaged 67ms in one run, 2.7ms in another due to model warm-up). The cap catches pathological regressions (new code adding a blocking DB query per chunk) rather than normal variance.

### Adapter isolation test

Each adapter must be independently runnable via `scripts/test_adapter.py --strategy hybrid --query "test query" --user-id 1`. This tests that the production service wiring is intact without running the full 50-query benchmark. It should run in < 5 seconds and be included in the pre-commit test suite.

### Confound detection

A new post-benchmark script `scripts/check_benchmark_confounds.py` should verify:

1. **Pool-latency consistency**: If the RERANK strategy shows latency within 50ms of HYBRID, warn that the cross-encoder may not have executed (latency of a no-op pool expansion vs. real inference).
2. **Note ID validity**: Every `relevant_note_id` in the benchmark must exist in the database. Report any stale IDs immediately.
3. **Strategy dominance check**: If RERANK results are identical to HYBRID across all 50 queries, warn that the reranker may be disabled or returning early.

The confound detection script directly codifies the lessons from Sprint 2-B.

---

## 11. Benchmark Versioning

### Current versioning state

`benchmark.json` has no version field, no schema version, no changelog, and no reference to the corpus version it was designed for. The file has been modified multiple times since initial creation, but git diff is the only historical record. There is no way to know which benchmark run used which version of the benchmark queries.

### Proposed versioning scheme

**Semantic version for the benchmark dataset** (`MAJOR.MINOR.PATCH`):

- **MAJOR**: query set changes that break backward compatibility (note IDs changed, relevance grades changed)
- **MINOR**: new queries added, or query text refined without changing the relevant set
- **PATCH**: labeling notes, tag corrections, metadata updates

The version is stored in a new `benchmark/manifest.json` (distinct from the run-level `manifest.json`):

```json
{
  "version": "2.0.0",
  "created_at": "2026-07-28",
  "corpus_version": "sprint2b",
  "note_count_at_labeling": 1055,
  "query_count": 200,
  "labeler": "awane",
  "changelog": [
    {
      "version": "2.0.0",
      "date": "2026-07-28",
      "change": "Migrated to three-tier relevance; added 150 verified queries; corpus baseline sprint2b"
    },
    {
      "version": "1.0.0",
      "date": "2026-07-01",
      "change": "Initial 50-query benchmark"
    }
  ]
}
```

Every benchmark run records the benchmark version in its `manifest.json`:

```json
{
  "run_id": "...",
  "benchmark_version": "2.0.0",
  ...
}
```

**Cross-version comparison rule**: Two runs with different benchmark versions must not be compared on absolute metric values. The dashboard trend chart draws a vertical dashed line at version boundaries. When a version bump changes the relevant set for a query, the MRR for that query is not comparable across the boundary.

### Corpus snapshot pinning

The benchmark version references a `corpus_version` string. This string should match a git tag on the main branch (e.g., `sprint2b`) that was committed when the database snapshot was taken. The benchmark is only valid against a corpus that matches this snapshot — if the database is re-seeded or notes are bulk-added, the corpus version should increment and affected benchmark entries must be re-verified.

For development use, add a `scripts/verify_corpus_version.py` that checks:
- Does the note count match `note_count_at_labeling`?
- Do all `relevant_note_ids` still exist in the database?
- For a random sample of 10 entries, does the top note title still match what was expected at labeling time?

---

## 12. Dataset Growth Strategy

### Current trajectory

The benchmark has been at 50 queries since its initial creation. In Sprints 1 and 2, the same 50 queries were reused for every benchmark decision, including enabling/blocking production feature flags. 50 queries is too few to reliably detect a 3% MRR improvement at p < 0.05 (requires n ≈ 150 using a one-sample Wilcoxon test at 80% power).

### Target size: 200 verified queries

For the benchmark to support statistically valid conclusions with 80% power and p < 0.05, it requires:
- Detecting ΔMRR = 0.04: n ≈ 120 queries
- Detecting ΔMRR = 0.03: n ≈ 200 queries
- Detecting ΔMRR = 0.02: n ≈ 450 queries

Target: **200 verified queries for gate decisions**, with an additional 100 auto-generated candidates maintained for exploratory runs. The 200 target is achievable with 2–4 hours of annotation work.

### Growth principles

**1. Coverage-first sampling**: New queries should target note IDs not yet covered by the benchmark. Use corpus coverage metric (Section 8) to identify the un-evaluated 95.4% of notes and sample from there first.

**2. Hard query injection**: For every 5 medium queries added, add 1 hard query. Hard queries are those where the system currently scores MRR = 0 (complete misses). These are identified from the per-query CSV output in `evaluation_results.csv`.

**3. Paraphrase pairs**: For each of the 10 most important queries (highest-coverage topics), add 2 paraphrase variants. This tests semantic robustness without requiring new note coverage.

**4. Negative queries**: Add 10 guaranteed-negative queries (queries about topics not in the corpus). Source from `RETRIEVAL_MIN_SCORE` filter behavior — if the system returns results for a negative query, the threshold is too low.

**5. Corpus-version locking**: New queries added to the `verified.json` batch are stamped with the corpus version and note count. When the corpus grows by > 100 notes, the entire `verified.json` goes through a stale-check pass (Section 5 `labeled_at` TTL).

### Growth cadence

| Sprint | Verified query target | Focus |
|---|---|---|
| 2-C | 50 (current) | Baseline migration to graded relevance |
| 3 | 100 | Fill intent gaps (project, event, reminder, general); add hard queries |
| 4 | 150 | Paraphrase pairs; negative queries |
| 5 | 200 | Full target; initiate statistical gate protocol |

---

## 13. Acceptance Criteria

### For the evaluation framework itself

A benchmark run against the new framework is considered valid when all of the following pass:

**Data integrity**
- [ ] All `relevant_note_ids` exist in the database (verified by `check_benchmark_confounds.py`)
- [ ] Benchmark version matches the corpus version (`verify_corpus_version.py` exits 0)
- [ ] No query has an empty relevant set
- [ ] At least 5 queries of each difficulty level (easy/medium/hard) in the verified set
- [ ] At least 3 queries per intent type

**Coverage**
- [ ] At least 150 unique note IDs referenced across the full benchmark (current: 49)
- [ ] Corpus coverage ≥ 15% (current: 4.6%)
- [ ] At least one query per retrieval challenge tag (Section 3, Axis A)

**Statistical validity**
- [ ] Benchmark has ≥ 100 verified queries (for gate decisions)
- [ ] Bootstrap 95% CI on HYBRID vs SEMANTIC MRR delta is computable (requires n ≥ 100)
- [ ] Each strategy run completes with 0 errors

**Correctness of gates**
- [ ] `gates.json` exists with floors ≤ current best values for each strategy
- [ ] `check_benchmark_confounds.py` reports no confounds for the current run
- [ ] Latency gate passes for each strategy

### For a retrieval feature to be approved

A retrieval change is approved for production when:
- [ ] Benchmark version ≥ 2.0.0 (graded relevance enabled)
- [ ] ≥ 100 verified queries used
- [ ] Proposed strategy MRR > baseline HYBRID MRR, with bootstrap CI not including zero
- [ ] Hit Rate ≥ baseline HYBRID Hit Rate (no regression)
- [ ] Latency within the approved envelope (Section 10)
- [ ] `check_benchmark_confounds.py` reports no confounds for the proposal run
- [ ] The latency difference between the proposed strategy and HYBRID is ≥ 50ms if inference is claimed (prevents the Sprint 2-B false positive where RERANKING_ENABLED was not actually True)

---

## 14. Migration Plan

### Phase 0 — Baseline preservation (no code changes, 1 day)

1. Tag the current `benchmark.json` as version `1.0.0` by adding a `benchmark/manifest.json`
2. Archive all existing benchmark run outputs in `evaluation_results/archive/sprint2b/`
3. Record current HYBRID baselines in `gates.json` as the initial floor values
4. Commit all existing `evaluation_results/` output to git as a versioned snapshot

Nothing breaks. All existing scripts and tests continue to work.

### Phase 1 — Schema migration (2 days)

1. Add `graded_relevance: dict[str, int]` as an optional field to `BenchmarkQuery` in `models.py`
2. Update `BenchmarkLoader` to parse the new field (backward-compatible: field is optional)
3. Update `ndcg_at_k` in `retrieval.py` to accept an optional `grade_map` parameter; when provided, use `2^grade - 1` gain; when absent, fall back to binary
4. Update the CSV report to include the new field
5. Add `corpus_coverage` to `EvaluationReport` and `StrategySummary`
6. All 767 existing tests must continue to pass

### Phase 2 — Human review tooling (3 days)

1. Implement `scripts/human_eval.py` with the interactive review CLI (Section 7)
2. Implement `scripts/verify_corpus_version.py`
3. Implement `scripts/check_benchmark_confounds.py` with the three confound checks (Section 10)
4. Create `benchmark/candidates.json` from `generate_benchmarks.py` output (unreviewed)
5. Create `benchmark/verified.json` initially by migrating `benchmark.json` with human review pass

Deliverable: `benchmark/verified.json` with all 50 current queries given graded relevance labels and `labeling_notes` per entry.

### Phase 3 — Auto-generation refactor (4 days)

1. Refactor `generate_benchmarks.py` to implement the five-stage pipeline (Section 6)
2. Add LLM-based query generation (Stage 1) using the Gemini provider already wired in `llm_service.py`
3. Add embedding-based deduplication (Stage 3) using `embedding_model` from `app/core/embedding_model.py`
4. Output to `benchmark/candidates.json` with stable IDs
5. Add `scripts/review_candidates.py` that wraps `human_eval.py` filtered to just new candidates

### Phase 4 — Dashboard and versioning (3 days)

1. Implement `scripts/generate_dashboard.py` producing `dashboard.html`
2. Add `manifest.json` emission to `EvaluationRunner.run()`
3. Update `scripts/evaluate.py` to call `generate_dashboard.py` at the end of every run
4. Add trend chart reading historical manifests from `evaluation_results/*/manifest.json`

### Phase 5 — Benchmark growth to 100 queries (5 days annotation)

1. Use `human_eval.py` to review auto-generated candidates for:
   - 30 queries covering intent types with < 3 current entries
   - 10 hard queries (current system MRR = 0)
   - 10 paraphrase pairs for the top-5 query topics
   - 10 negative queries (no relevant notes exist)
2. Update `benchmark/manifest.json` to version `2.0.0`
3. Recompute `gates.json` from the 100-query baseline run
4. All gate decisions from Sprint 3 onward use the 100-query benchmark

### Phase 6 — Regression test integration (2 days)

1. Implement `scripts/test_adapter.py --strategy hybrid` for smoke testing (Section 10)
2. Add a `make benchmark-gate` target to run the 100-query benchmark and check `gates.json`
3. Document the gate protocol in a single page at `docs/BENCHMARK_GATE.md`

### Total estimated effort: 20 working days (annotation time excluded from code estimate)

The annotation work in Phase 5 (5 days) is the bottleneck. All other phases are pure engineering and can be developed in parallel with other sprint work.

---

## Summary of Key Decisions

| Decision | Rationale | Repository evidence |
|---|---|---|
| Graded relevance (3-tier) | Binary relevance makes nDCG meaningless | `retrieval.py` binary implementation |
| 200-query target | Statistical power analysis: n=150 needed for ΔMRR=0.04 at 80% power | Sprint 2-B MRR delta = 0.017 was noise |
| Two-tier benchmark files (verified/candidates) | Generator relevance is heuristic only | `generate_benchmarks.py` line 67: substring match |
| Semantic version for benchmark | Metrics are not comparable across corpus changes | No version field in current `benchmark.json` |
| Confound detection script | False positive in Sprint 2-B from pool expansion | Latency 108ms vs 423ms revealed the confound |
| Static HTML dashboard | Zero runtime dependencies, always reviewable | No existing visualization infrastructure |
| Bootstrap CI requirement | Point estimate alone is not statistically valid | n=50 was insufficient to detect signal vs. noise |
| `gates.json` floor at best-3% | Catches regressions without flagging normal variance | SEMANTIC latency: 2.7ms vs 67ms between runs |
