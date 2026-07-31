# ADR-003: Note-Level Embeddings as the Production Default for the Hybrid Semantic Arm

**Status:** Accepted — amended 2026-07-28 (cross-encoder reranking infrastructure built; flag remains OFF)  
**Date:** 2026-07-28  
**Sprint:** 2-B (Phase A analysis only — Phase B deferred)  
**Deciders:** Awane  
**References:** `chunk_service.py:147–153`, `evaluation_results/phase2_after/evaluation_report.md`,
`docs/design/cross-encoder-reranking.md`, `evaluation_results/sprint2b_fresh/`

---

## Context

KnowledgeVault stores two parallel embedding corpora:

| Table | Granularity | Indexed by | Used by |
|---|---|---|---|
| `embeddings` | One vector per note | `EmbeddingRepository` | Hybrid semantic arm |
| `chunk_embeddings` | One vector per sentence chunk | `ChunkEmbeddingRepository` | Pure-semantic `retrieve()` endpoint |

The `retrieve_hybrid()` method in `chunk_service.py` runs two arms:

1. **Semantic arm** — ANN search over `embeddings` (note-level), pool of `max(4×limit, 20)` candidates.
2. **Intent arm** — Fast keyword classifier → category match → note lookup.

Results are merged using additive confidence-gated boosting (max boost 0.12), then ranked and returned.

**Sprint 2-B Phase B** proposed switching the hybrid semantic arm from note-level embeddings (`embeddings` table) to chunk-level embeddings (`chunk_embeddings` table). The hypothesis was that finer-grained vectors would produce better relevance ranking.

Sprint 2-B was approved only for Phase A (analysis). Phase B was not approved.

---

## Decision

**Note-level embeddings remain the production default for the hybrid semantic arm.**

The hybrid semantic arm will continue to call `EmbeddingRepository.search_similar_notes_with_distance()` rather than `ChunkEmbeddingRepository.search_similar_chunks_with_distance()`.

---

## Benchmark Evidence

Evaluation run `c85f54c6` (2026-07-27), 50 queries, K=5, 1055-note corpus:

| Strategy | Precision@5 | Recall@5 | Hit Rate | MRR | Avg Latency (ms) |
|---|---:|---:|---:|---:|---:|
| SEMANTIC (chunk embeddings) | 0.244 | 0.547 | 0.760 | 0.612 | 34.66 |
| INTENT only | 0.052 | 0.099 | 0.220 | 0.161 | 32.16 |
| HYBRID (note embeddings) | 0.244 | 0.547 | 0.760 | 0.607 | 93.34 |

**Observations:**

1. HYBRID (note-level) matches SEMANTIC (chunk-level) exactly on Precision@5, Recall@5, and Hit Rate. MRR difference (0.607 vs 0.612) is within noise on 50 queries.
2. Chunk-level retrieval therefore does **not** outperform note-level retrieval on this corpus under the current configuration.
3. The note-level arm already achieves Hit Rate = 0.760 and MRR = 0.607 — switching to chunk-level would not improve these numbers and risks the regressions documented below.

**Historical regression (recorded in source):**

Prior to the current implementation, the hybrid semantic arm used chunk embeddings. The revert rationale is preserved in `chunk_service.py:147–153`:

```
# Use the same note embeddings as the standalone semantic path.  The
# previous implementation used a different chunk corpus, then
# truncated chunks before note de-duplication; the two strategies were
# therefore not comparable and repeated chunks consumed the top-K.
```

The two specific failure modes were:

- **Pool contamination:** Multiple chunks from the same note occupied several top-K slots, reducing candidate diversity.
- **Pre-dedup truncation:** Chunks were truncated before note-level deduplication ran, so the final result set was smaller than intended and the note coverage metric collapsed.

---

## Why Phase B Is Deferred

Switching the hybrid semantic arm to chunk embeddings would require resolving three open problems first:

### Problem 1 — Candidate diversity collapse

At K=8 (the current pool size passed to `retrieve_hybrid()`), a 1055-note corpus with an average of ~4 chunks per note means chunk ANN returns at most 2 distinct notes in a naively pooled top-8. Note-level ANN guarantees at most 1 slot per note, preserving diversity across the candidate set.

### Problem 2 — Incomparable benchmark baseline

The SEMANTIC strategy in the current benchmark uses `ChunkEmbeddingRepository` (chunk-level). Switching the HYBRID semantic arm to chunk embeddings would make HYBRID and SEMANTIC share the same embedding table and pool, conflating two strategies that the benchmark is designed to measure independently.

### Problem 3 — Note-level granularity is appropriate for this corpus

KnowledgeVault notes are short personal notes (typically 100–500 tokens). Each note is semantically coherent. Splitting into sentence chunks does not increase semantic resolution — it fragments context. Note-level embeddings capture the full meaning of a note with a single vector, which is appropriate for the retrieval task (return the relevant note, not the relevant sentence).

---

## Prerequisites for Enabling Phase B

Phase B may be re-evaluated when **all** of the following are true:

1. **Chunk-level deduplication is implemented** before fusion: the candidate pool must be deduplicated to one chunk per note before score fusion runs, so multiple chunks of the same note cannot consume multiple result slots.

2. **Corpus size reaches the threshold where within-note diversity matters:** personal notes with ≥10 meaningful paragraphs per note (approximately 1000+ tokens) benefit from chunk-level granularity. Current notes are too short.

3. **Multi-document synthesis is the primary use case:** if the product evolves toward ingesting long-form documents (PDFs, books, transcripts), chunk-level retrieval becomes necessary. This is a prerequisite for the multi-document rationale below.

4. **A dedicated Phase B benchmark confirms improvement:** the benchmark must show ΔHit Rate ≥ +0.03 and ΔMRR ≥ +0.04 over HYBRID on the same query set to justify the added complexity.

---

## Benchmark Gate for Phase B Activation

| Metric | Current HYBRID Baseline | Required HYBRID+ChunkArm |
|---|---:|---:|
| Precision@5 | 0.244 | ≥ 0.270 |
| Recall@5 | 0.547 | ≥ 0.580 |
| Hit Rate@5 | 0.760 | ≥ 0.790 |
| MRR | 0.607 | ≥ 0.650 |

All four metrics must be met simultaneously. A regression on any single metric blocks activation.

---

## Future Multi-Document Rationale

The principal future scenario that would motivate Phase B is multi-document ingestion (PDFs, long articles, transcripts). When a single document contains 20–100 meaningful passages across a wide topic range:

- Note-level embeddings collapse the entire document to one vector, losing passage-level granularity.
- The top-K result for a specific factual query would return the document title at rank 1 but present the wrong passage as context, corrupting the LLM's answer.
- Chunk-level retrieval with within-document deduplication would return the correct passage.

Until multi-document ingestion ships, the note-level semantic arm remains correct and simpler.

---

## Consequences

### Positive

- Retrieval quality is maintained at the benchmarked baseline (Hit Rate 0.760, MRR 0.607).
- Implementation remains simple: one ANN call over `embeddings`, one over category-matched notes.
- No candidate diversity regression.
- No breaking change to the benchmark comparison baseline.

### Negative

- Chunk embeddings (stored in `chunk_embeddings`, computed and maintained by `ChunkService.process_note()`) are not used by the hybrid path. They are used only by `retrieve()` (the pure-semantic endpoint). This is a maintained but partially idle asset.
- When multi-document ingestion ships, Phase B becomes necessary rather than optional. The work is deferred, not cancelled.

### Neutral

- `RETRIEVAL_MIN_SCORE = 0.10` (configurable in `.env`) continues to gate results at the `AskService` level. This is independent of the embedding granularity decision.

---

## Addendum — 2026-07-28: Cross-Encoder Reranking Infrastructure (flag OFF)

### What was built

Cross-encoder reranking was designed and implemented as a second-pass retrieval stage
on top of the note-level hybrid arm described in this ADR.

**Implementation files:**
- `app/core/rerank_model.py` — lazy-loaded `CrossEncoder` singleton
- `app/services/reranking_service.py` — inference + Redis score cache
- `app/evaluation/adapters/rerank.py` — RERANK benchmark strategy
- `tests/test_reranking_service.py`, `tests/test_ask_reranking.py` — 34 new tests (767/767 total pass)

**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2` (22 MB)  
**Feature flag:** `RERANKING_ENABLED = False` (infrastructure shipped; flag stays OFF — see below)  
**Stage-1 pool:** `RERANK_CANDIDATE_POOL = 20` candidates from `retrieve_hybrid()`  
**Stage-2 output:** `RERANK_TOP_K = 8` candidates, reordered by cross-encoder score

### Benchmark results

**Run `sprint2b_fresh` (2026-07-28), cross-encoder actually executing, 50 queries, K=5:**

| Strategy | Precision@5 | Recall@5 | Hit Rate | MRR | Avg Latency (ms) |
|---|---:|---:|---:|---:|---:|
| SEMANTIC | 0.244 | 0.547 | 0.760 | 0.612 | 2.3 |
| INTENT | 0.068 | 0.129 | 0.280 | 0.221 | 55.4 |
| HYBRID (production baseline) | 0.240 | 0.527 | 0.740 | 0.602 | 126.9 |
| **RERANK (cross-encoder ON)** | **0.172** | **0.403** | **0.640** | **0.483** | **423.5** |

Errors: 0 (graceful degradation path not triggered — the model ran, it just ranked poorly).

**RERANK is materially worse than HYBRID on every quality metric.**

### What the intermediate benchmark actually measured

An intermediate run (`sprint2b_rerank_enabled`) appeared to show RERANK improving Hit Rate from
0.740 to 0.760 with 9ms latency overhead. Post-hoc analysis revealed this improvement came
entirely from the **expanded candidate pool (limit=20 vs limit=5 for HYBRID)**, not from the
cross-encoder. The cross-encoder did not run in that benchmark because the shell env-var
`RERANKING_ENABLED=true` set in WSL2 bash was not propagated to the Windows Python binary
(`venv/Scripts/python.exe`). With `rerank_model = None`, `RerankingService.rerank()` returned
`candidates[:top_k]` immediately — no inference, no cache write, just a larger pool.

The proof is the latency: an executing cross-encoder on 20 candidates costs ~300ms of
inference overhead. The intermediate run showed only 9ms overhead over HYBRID, matching
exactly what an expanded-pool-only path produces. The `sprint2b_fresh` run confirmed this
by flushing the Redis score cache and re-running: cross-encoder inference took 423ms average
and produced Hit Rate 0.640, well below HYBRID's 0.740.

### Gate evaluation (corrected)

| Metric | Design Gate | HYBRID Baseline | RERANK Actual | Status |
|---|---:|---:|---:|---|
| Precision@5 | ≥ 0.270 | 0.240 | 0.172 | **REGRESSION** |
| Recall@5 | ≥ 0.575 | 0.527 | 0.403 | **REGRESSION** |
| Hit Rate | ≥ 0.790 | 0.740 | 0.640 | **REGRESSION** |
| MRR | ≥ 0.650 | 0.602 | 0.483 | **REGRESSION** |
| Avg latency | ≤ 150ms | 126.9ms | 423.5ms | **FAILED** |

### Root cause and recommended path

The `ms-marco-MiniLM-L-6-v2` model is trained on MS MARCO web search passages. Personal notes
differ structurally: they are short, casual, first-person, and often use noun-phrase titles
rather than declarative sentences. The cross-encoder scores notes that read like web content
higher, which does not correlate with what the user actually wants to retrieve.

This matches **Risk R3** (domain mismatch) documented in `docs/design/cross-encoder-reranking.md`.
The design's stated mitigation was "the benchmark gate is the mitigation" — and the gate failed.

**Key finding: the expanded pool itself improves retrieval.**

With pool=20 and NO reranking, the RERANK adapter achieves Hit Rate 0.760 (matching SEMANTIC).
This suggests a lower-cost fix than cross-encoder reranking: expand the HYBRID pool from 5
to 20 directly, without adding cross-encoder overhead.

### Enabling decision

`RERANKING_ENABLED = False` remains the production default. The infrastructure is complete and
correct (graceful fallback, caching, feature flag, 34 tests). The flag should not be set to
`True` until one of the following prerequisites is met:

1. A domain-appropriate cross-encoder is identified (e.g. fine-tuned on personal knowledge
   base queries, or a zero-shot reranker that generalises better to short, casual text).
2. The retrieval benchmark shows ΔMRR ≥ +0.04 and ΔHit Rate ≥ +0.03 over HYBRID with the
   cross-encoder actually executing (verified by latency: inference overhead must be visible).

The `reranked: bool` field on `AskResponse` is retained for future use when a suitable model
is found.
