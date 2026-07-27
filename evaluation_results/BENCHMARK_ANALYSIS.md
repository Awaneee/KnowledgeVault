
# KnowledgeVault — Benchmark Analysis Report

This report describes the benchmark datasets generated for evaluating KnowledgeVault's
retrieval and RAG pipeline quality. Benchmarks were generated from 1000 notes ingested through the production pipeline.

## 1. Retrieval Benchmark

| Metric | Value |
| --- | --- |
| Total Queries | 152 |
| Avg Relevant Notes per Query | 8.49 |
| Min Relevant Notes | 1 |
| Max Relevant Notes | 10 |
| Queries with No Matched Notes | 0 |


### By Difficulty

| Difficulty | Count | Percentage |
| --- | --- | --- |
| easy | 60 | 39.5% |
| hard | 33 | 21.7% |
| medium | 59 | 38.8% |

### By Expected Intent Type

| Intent | Count |
| --- | --- |
| study | 78 |
| reference | 38 |
| todo | 15 |
| idea | 6 |
| general | 6 |
| reminder | 4 |
| event | 3 |
| communication | 2 |

### Special Query Types

| Type | Count | Description |
| --- | --- | --- |
| exact | 5 | Exact phrase from note content |
| ambiguous | 4 | Queries with multiple valid interpretations |
| comparison | 5 | X vs Y comparative queries |
| temporal | 2 | Time-relative queries (this week, upcoming) |
| multi_hop | 0 | Require synthesizing multiple notes |

## 2. Ask / RAG Benchmark

| Metric | Value |
| --- | --- |
| Total Questions | 47 |
| Avg Expected Notes per Question | 7.43 |

### By Category

| Category | Count | Description |
| --- | --- | --- |
| factual_lookup | 20 | Direct fact retrieval from a single note |
| multi_hop | 5 | Requires combining information from 2+ notes |
| comparison | 5 | Asks to compare two technologies or approaches |
| synthesis | 5 | Requests a summary across multiple notes |
| temporal | 4 | Time-sensitive or date-relative questions |
| ambiguous | 4 | Underspecified — multiple valid interpretations |
| category | 4 | Category-browsing oriented |

### By Difficulty

| Difficulty | Count |
| --- | --- |
| easy | 8 |
| hard | 19 |
| medium | 20 |

## 3. Evaluation Results (if available)

| Strategy | N | Precision@K | Recall@K | Hit Rate | MRR | Avg Latency (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| HYBRID | 152 | 0.3079 | 0.2090 | 0.7434 | 0.5874 | 98.66 |
| INTENT | 152 | 0.0053 | 0.0026 | 0.0132 | 0.0088 | 28.61 |
| SEMANTIC | 152 | 0.3066 | 0.2084 | 0.7434 | 0.5528 | 1.31 |

**Hybrid vs Semantic ΔMRR: +0.0346**

## 4. Benchmark Design Notes

### Query Type Coverage
The retrieval benchmark covers all major query types:
- **Factual lookup**: direct topic search (e.g., 'What is HNSW?')
- **Paraphrased**: same concept, different phrasing
- **Multi-hop**: combine multiple notes (e.g., 'KnowledgeVault RAG decisions and benchmark findings')
- **Temporal**: date/time relative (e.g., 'pending tasks this week')
- **Comparison**: X vs Y queries (e.g., 'Redis vs Kafka')
- **Synthesis**: summarize a category (e.g., 'all my AI notes')
- **Ambiguous**: underspecified intent (e.g., 'my project notes')
- **Exact keyword**: precise phrase from note content (e.g., 'HNSW index')
- **Semantic**: meaning-based, not keyword-based (e.g., 'strategies for improving code performance')
- **Category-oriented**: category browsing queries

### Known Limitations
1. `relevant_note_ids` are assigned by content keyword matching, which may miss notes where the same concept is expressed differently.
2. Temporal queries have inherently fuzzy ground truth — the expected set depends on what 'this week' means relative to note creation dates.
3. Multi-hop queries require the retrieval system to surface multiple notes; the current K=5 limit may prevent full recall for queries expecting 6+ notes.
4. The ask benchmark reference answers are written for the notes dataset and assume the notes contain the factual information. If a note was not correctly processed, the answer may be unreachable.
5. Expected set capping at 10 (retrieval) / 8 (ask) is a design choice. Keyword matching over 1055 notes produces very large candidate sets; capping focuses the evaluation on the most keyword-central notes. This means some genuinely relevant notes are excluded from the expected set.

## 5. Ask Benchmark — Retrieval Quality (no LLM required)

Measured by running `retrieve_hybrid(K=8)` on all 47 ask benchmark questions and comparing retrieved note IDs against expected note IDs. Gemini API quota was exhausted after 1000-note ingestion, so LLM-scored metrics (correctness, groundedness, hallucination) require re-running `evaluate_ask.py` when quota resets.

| Metric | Value |
| --- | --- |
| Mean Recall@expected | 0.233 |
| Median Recall | 0.167 |
| MRR (first expected note hit) | 0.558 |
| Hit Rate (≥1 expected note found) | 74.5% (35/47) |
| Avg retrieval latency | ~100ms (hybrid) |

### By Category

| Category | n | Recall@8 | MRR | Assessment |
| --- | --- | --- | --- | --- |
| factual_lookup | 20 | 0.388 | 0.832 | **Strong** — direct questions anchor to specific notes |
| temporal | 4 | 0.219 | 0.417 | Adequate — date-relative queries partially work |
| synthesis | 5 | 0.150 | 0.500 | Moderate — finds at least one relevant note half the time |
| multi_hop | 5 | 0.125 | 0.500 | Moderate — some cross-note queries succeed |
| category | 4 | 0.146 | 0.354 | Moderate |
| comparison | 5 | 0.050 | 0.200 | **Weak** — X vs Y queries need both halves; often gets neither |
| ambiguous | 4 | 0.031 | 0.125 | **Failing** — underspecified queries return arbitrary results |

### Key Findings

**Factual lookup is the system's strongest mode.** Queries like "What is HNSW?", "What is the walrus operator?", and "What is BRPOPLPUSH?" achieve MRR=1.0 — the exact note is ranked first. This confirms that the semantic embedding correctly places specific factual notes near their conceptual queries.

**Comparison and ambiguous queries fail consistently.** "What are the trade-offs between Python and Go?" returns recall=0.00 — the notes it finds are about Go or Python individually, but not the notes discussing the comparison explicitly. This is an architectural limitation of single-vector retrieval: it cannot simultaneously anchor to two concepts and their relationship.

**Synthesis queries partially succeed.** "Summarize all my AI and machine learning study notes" achieves MRR=0.500 — the system finds *some* relevant AI notes but not the specific 8 keyword-central ones used as ground truth. This reflects that synthesis ground truth is inherently fuzzy.

**12 queries return zero recall.** These are mostly synthesis, comparison, and ambiguous queries. The failures split into two causes: (1) the expected notes aren't the ones semantic search naturally ranks first (benchmark design issue), and (2) the query is genuinely too vague or multi-faceted for single-vector retrieval.

## 6. Retrieval Benchmark — Strategy Comparison

On the 152-query benchmark (K=5):

| Strategy | Precision@5 | Recall@5 | Hit Rate | MRR | Latency | ΔMRR vs Semantic |
| --- | --- | --- | --- | --- | --- | --- |
| SEMANTIC | 0.307 | 0.208 | 74.3% | 0.553 | 1.3ms | — |
| INTENT | 0.005 | 0.003 | 1.3% | 0.009 | 28.6ms | −0.544 |
| HYBRID | 0.308 | 0.209 | 74.3% | 0.587 | 98.7ms | **+0.034** |

**The hybrid ΔMRR of +0.034 is below the minimum detectable effect** (MDE = 0.069 at p<0.05, n=152, σ≈0.43). This replicates the 50-query benchmark finding: hybrid is not statistically distinguishable from semantic with the current system parameters.

**Intent alone is catastrophic.** Category cap at 50 was reached after 155 notes. All subsequent notes were force-assigned via `cap_fallback`, meaning 63.3% of assignments went to the nearest existing category regardless of semantic compatibility. The intent arm's effective accuracy on this benchmark is 14.5% (down from 34% on the original 50-query benchmark) — a larger, more diverse dataset exposes the fast classifier's keyword-matching fragility.

**Latency: hybrid costs +97ms (+7400%) for +0.034 MRR gain.** At current performance, the intent arm is not cost-effective.

## 7. To Run LLM-Scored Ask Evaluation

When Gemini API quota resets (midnight Pacific time), run:

```bash
python scripts/evaluate_ask.py \
    --user-id 1 \
    --dataset evaluation_results/benchmarks/ask_benchmark.json \
    --output evaluation_results/ \
    --no-artifacts
```

The evaluation runner sleeps 8 seconds between queries. With 47 queries requiring 2 Gemini calls each at 15 RPM, allow ~12 minutes. If 429 errors persist, increase the sleep in `app/evaluation/ask/runner.py` line ~297 from 8.0 to 16.0 seconds.

**Expected outcome based on retrieval quality:** Factual lookup questions (MRR=0.832) will produce high-quality answers. Comparison, synthesis, and ambiguous questions will likely produce degraded or low-quality answers — they cannot retrieve their expected notes, so the LLM has no relevant context to synthesize from.