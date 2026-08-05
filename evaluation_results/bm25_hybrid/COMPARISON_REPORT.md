# BM25 + Reciprocal Rank Fusion: Evaluation Report

**Date:** 2026-08-03  
**Benchmark:** v2.0.0 (50 queries, K=5)  
**Baseline:** HYBRID (semantic + intent, production pipeline)  
**Candidate:** HYBRID_BM25 (semantic + BM25 sparse, RRF fusion)

---

## Results at a Glance

| Metric | SEMANTIC | HYBRID (baseline) | HYBRID_BM25 (candidate) | Δ (candidate − baseline) |
|--------|:--------:|:-----------------:|:-----------------------:|:------------------------:|
| Hit Rate@5 | 0.760 | 0.760 | 0.760 | **0.000** |
| MRR@5 | 0.612 | 0.620 | 0.609 | **−0.011** |
| Recall@5 | 0.547 | 0.543 | 0.537 | −0.006 |
| Precision@5 | 0.244 | 0.240 | 0.240 | 0.000 |
| MAP@5 | 0.421 | 0.418 | 0.405 | −0.013 |
| nDCG@5 | 0.503 | 0.500 | 0.489 | −0.011 |
| R-Precision | 0.385 | 0.383 | 0.367 | −0.016 |
| Avg Latency | 2.2 ms | 82.5 ms | 25.5 ms | **−57 ms (3.2× faster)** |

### Statistical Significance

| Comparison | ΔMRR | 95% CI | Significant | Recommendation |
|-----------|-----:|:------:|:-----------:|:--------------|
| HYBRID_BM25 vs HYBRID | −0.012 | [−0.027, 0.000] | ✗ | `insufficient_evidence` |

---

## Verdict: Do Not Promote BM25 as Primary Retrieval

The candidate does not beat the baseline on any retrieval quality metric.  
All differences are within noise — the 95% bootstrap CI on ΔMRR includes zero.

**BM25_ENABLED remains False (default).** The infrastructure is shipped and ready; the flag is the only gate.

---

## Why BM25 Does Not Help on This Corpus

### 1. Personal notes are lexically sparse and informal

The benchmark queries ("Things I need to tell Sid", "Don't forget to buy milk", "Flutter improvements") use
everyday language that is semantically rich but lexically divergent from the note text.  
BM25's term-matching model cannot bridge this gap.

**Evidence:** Pure BM25 achieves only 14% Hit Rate vs. 76% for semantic — a 5.4× gap.
This means 86% of queries return **no relevant note at all** from BM25 alone.

### 2. English FTS stop-word removal hurts short notes

PostgreSQL's `'english'` dictionary discards common words ("my", "the", "to", "how").  
For a query like *"What is the theory of relativity?"*, the resulting tsquery is
`'theori' & 'relat'` — two stemmed tokens.  
The note titled *"Theory of Relativity — Physics Notes"* may not match if the chunk
text uses different phrasing.

### 3. RRF amplifies noise when one arm is weak

RRF is symmetric: each arm's rank-1 result contributes `1/(60+1) ≈ 0.0164`.  
When BM25 returns mostly irrelevant notes (86% miss rate), those spurious
results displace semantically correct notes from the top-5 window.

This is the same phenomenon documented for cross-encoder reranking on this corpus
(see ADR-003 addendum): a second retrieval signal that is weakly correlated with
relevance hurts more than it helps when merged with a strong primary signal.

### 4. The intent arm already covers lexical cases

The existing HYBRID pipeline includes an intent/category arm that handles
deterministic lexical matches (canonical names, actor-based rules).  
BM25 would be redundant for lexically-identifiable queries ("tell Sid",
"Docker commands") and harmful for semantically-oriented ones.

---

## What Was Built (Still Useful)

Even though BM25 is gated off, the implementation is production-ready:

| Artifact | Description |
|---------|-------------|
| Migration `c8d9e0f1a2b3` | `search_vector tsvector` + GIN index + auto-update trigger |
| `BM25Repository` | `websearch_to_tsquery` + `ts_rank_cd`, error-safe |
| `ChunkService._retrieve_rrf_hybrid()` | Pure RRF fusion, flag-free, usable by eval and future callers |
| `ChunkService.retrieve_bm25_hybrid()` | Public API, gated by `BM25_ENABLED` |
| `BM25Adapter`, `HybridBM25Adapter` | Evaluation adapters that bypass the production flag |
| 18 unit tests | BM25 repo, RRF math, feature-flag branches |
| `BM25_ENABLED`, `BM25_RRF_K`, `BM25_CANDIDATE_POOL` | Config flags with sensible defaults |

**Latency win:** HYBRID_BM25 averages 25.5 ms vs. 82.5 ms for HYBRID.  
If the corpus shifts toward technical documentation (longer notes, precise terminology),
enabling `BM25_ENABLED=True` becomes the only required change.

---

## Latency Profile

| Strategy | Avg (ms) | Median (ms) | P95 (ms) | Max (ms) |
|---------|:--------:|:-----------:|:--------:|:--------:|
| BM25 (pure) | 1.76 | 1.56 | 2.14 | 5.84 |
| HYBRID_BM25 | 25.49 | 23.34 | 48.26 | 100.68 |
| HYBRID | 82.46 | 80.28 | 108.26 | 155.88 |
| RERANK | 82.13 | 78.97 | 111.04 | 152.74 |

HYBRID_BM25 is 3.2× faster than HYBRID because it skips the intent/category
lookup chain (LLM-free) and runs only two parallel DB queries (pgvector + GIN FTS).

---

## Production Decision

```
BM25_ENABLED=False   ← current default, correct for this corpus
BM25_RRF_K=60        ← Cormack et al. standard, no change needed
BM25_CANDIDATE_POOL=20
```

Re-evaluate if:
- Corpus shifts to include technical reference notes (CS papers, docs, code)
- Average note length grows significantly (FTS improves on longer text)
- A domain-tuned text configuration (e.g., custom stop-words, synonym dictionaries)
  is available for the `to_tsvector` call
