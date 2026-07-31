# Design: Cross-Encoder Reranking for KnowledgeVault Retrieval

**Status:** Proposed — awaiting approval before implementation  
**Date:** 2026-07-28  
**Author:** Awane  
**Builds on:** ADR-003, `chunk_service.py`, `ask_service.py`

---

## 1. Current Retrieval Flow

The full query path is:

```
POST /ask/  (ask.py:35)
    └── AskService.ask()  (ask_service.py:75)
            │
            ├─ [1] CacheService.get(cache_key)                     ~1ms (cache hit → return)
            │
            ├─ [2] ChunkService.retrieve_hybrid(query, user_id, limit=8)  ~93ms
            │        ├─ embedding_model.encode(query)              ~2ms  (all-MiniLM-L6-v2)
            │        ├─ EmbeddingRepository                        ~20ms (note-level ANN, pool=20)
            │        ├─ IntentCategoryService.find_category_matches ~30ms (fast classifier + category ANN)
            │        └─ Score fusion + sort → top-8 note/chunk pairs
            │
            ├─ [3] AskService._filter_chunks()                     ~0ms  (drop score < 0.10)
            │
            ├─ [4] AskService._build_context_map()                 ~0ms  (dedup, 3000-char budget)
            │        └─ Ordered by hybrid score (semantic × 0.65 + intent boost ≤ 0.12)
            │
            ├─ [5] LLMService.generate(prompt)                     ~1500ms (Gemini / Groq)
            │        └─ Uses [1]–[4] context ordered by hybrid score
            │
            └─ [6] AskService._parse_citations()                   ~0ms
```

**Key bottlenecks and quality limits:**

| Step | Latency | Quality limit |
|---|---|---|
| Note-level ANN (step 2) | ~20ms | Scores computed by cosine distance; no query-passage interaction |
| Hybrid score fusion (step 2) | ~0ms | Additive boost, max 0.12 for intent — cannot reorder semantic ranking strongly |
| Context ordering (step 4) | ~0ms | Context is ordered by hybrid score, not by true relevance to the question |
| LLM synthesis (step 5) | ~1500ms | Quality depends on context order: most relevant passage should appear first |

The key insight: **the hybrid score is a retrieval approximation, not a fine-grained relevance judgment.** A bi-encoder score (dot product of independently embedded vectors) cannot model query-passage interaction. A cross-encoder jointly processes the (query, passage) pair and produces a calibrated relevance score.

---

## 2. Where Reranking Fits

Reranking is a second-pass operation that sits between step 2 and step 3:

```
POST /ask/
    └── AskService.ask()
            │
            ├─ [2] retrieve_hybrid() → 20 candidates           ← expand pool
            │
            ├─ [2B] RerankingService.rerank(query, candidates) ← NEW
            │        └─ CrossEncoder.predict([(query, text₁), (query, text₂), ...])
            │           → sorted by reranker score → top-8
            │
            ├─ [3] _filter_chunks()
            ├─ [4] _build_context_map()   ← now ordered by reranker score
            └─ [5] LLMService.generate()  ← sees best passage first
```

This is the **retrieve-then-rerank** pattern (also called two-stage retrieval). The first stage uses fast approximate search (bi-encoder) to recall a candidate pool. The second stage uses a slow but accurate cross-encoder to reorder that pool before context construction.

**Why this placement:**

- Reranking 20 candidates with a cross-encoder is fast (~30–80ms on CPU for the recommended model).
- Reranking 1055 notes with a cross-encoder would be prohibitively slow (~50s+).
- The first-stage recall (Hit Rate = 0.760) is good enough that the answer is almost certainly in the top-20. The cross-encoder then elevates it to rank 1 or 2.

**Effect on context construction (`_build_context_map`, ask_service.py:303):**  
The context string is built by iterating `chunks` in order. After reranking, chunk 0 is the most query-relevant passage rather than the highest-cosine-similarity note. The LLM is known to weight earlier context more heavily (primacy effect), so better ordering directly improves answer quality.

---

## 3. Cross-Encoder Model Selection

`sentence_transformers` is already installed at `venv/Lib/site-packages/sentence_transformers/` with `cross_encoder/` support present (confirmed at `venv/Lib/site-packages/sentence_transformers/cross_encoder/evaluation/reranking.py`).

### Candidate models

| Model | Size | Speed (20 pairs, CPU) | Domain | Notes |
|---|---|---|---|---|
| `cross-encoder/ms-marco-MiniLM-L-6-v2` | 22 MB | ~25–40ms | MS MARCO (web search) | Recommended primary |
| `cross-encoder/ms-marco-MiniLM-L-12-v2` | 33 MB | ~45–70ms | MS MARCO | Better quality, ~2× cost |
| `cross-encoder/ms-marco-electra-base` | 134 MB | ~200–400ms | MS MARCO | Best quality, impractical on CPU |
| `cross-encoder/stsb-roberta-base` | 499 MB | ~400–800ms | STS-Benchmark | Wrong task type (semantic similarity, not relevance) |

### Recommendation: `cross-encoder/ms-marco-MiniLM-L-6-v2`

**Rationale:**

1. **Size:** 22 MB resident in memory for the lifetime of the server — negligible on any production host.
2. **Speed:** At batch size 20, this model runs in ~25–40ms on a single CPU core. Combined with current hybrid latency (~93ms), total retrieval + rerank ≈ 120–140ms.
3. **Domain fit:** MS MARCO is a passage retrieval dataset. Personal notes are short, factual passages — structurally similar to MS MARCO passages. The model's relevance judgment generalizes well.
4. **Integration:** `sentence_transformers.CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2").predict(pairs)` returns a float array. No additional dependencies.

**Rejected alternatives:**

- `ms-marco-MiniLM-L-12-v2`: Only marginally better quality but nearly 2× slower. Not justified unless benchmarking shows L-6 is insufficient.
- `electra-base`: 400ms latency on CPU makes the blocking ask endpoint unacceptable. Would require GPU or async execution.
- STS models: Semantic textual similarity is not relevance ranking. These models would score a note about Python vs a query about Python highly even if the note is entirely off-topic.

### Model loading

The model must be loaded once at startup (not per-request). The recommended approach mirrors how `embedding_model` is loaded at `app/core/embedding_model.py`:

```python
# app/core/rerank_model.py  (to be created at implementation time)
from sentence_transformers import CrossEncoder
rerank_model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
```

Cold-load time: ~200–500ms on first import. Subsequent calls are in-memory.

---

## 4. Candidate Pool Sizing

Current hybrid retrieval: `limit=8` passed from `AskService.ask()` (ask_service.py:95).

For reranking to improve upon pure hybrid ordering, the candidate pool must be meaningfully larger than the final K. If pool == K, the reranker merely re-orders 8 items; the benefit is small. If pool >> K, the reranker can promote highly relevant items that the bi-encoder ranked low.

### Pool size analysis

| Pool (N) | Reranker pairs | Expected cross-encoder time (L-6, CPU) | Recall@8 at stage-1 |
|---|---|---|---|
| 8 (current) | 8 | ~10ms | Baseline |
| 16 | 16 | ~20ms | +3–5% |
| 20 | 20 | ~28ms | +5–8% |
| 30 | 30 | ~45ms | +7–10% |
| 40 | 40 | ~65ms | Diminishing returns |

**Recommendation: pool N=20 for the ask path; N=10 for the retrieve API.**

Evidence from the benchmark: at K=5, Hit Rate = 0.760, meaning 24% of queries return zero relevant results. At K=8 (current ask pool), we can compute the implied Recall@8 from the existing report (sprint1/phase2 data). Expanding to N=20 at stage-1 captures more of the long-tail relevant notes for the reranker to elevate.

### Implementation change

In `AskService.ask()` and `AskService.stream_ask()`, the call at ask_service.py:95 becomes:

```python
# ask_service.py — conceptual change (do not implement yet)
chunks = self.chunk_service.retrieve_hybrid(
    query=question,
    user_id=user_id,
    limit=20,  # was 8; expanded for reranker input
)
# → RerankingService.rerank(question, chunks, top_k=8)
# → _filter_chunks(reranked[:8])
```

The `limit` parameter of `retrieve_hybrid` controls the ANN pool size indirectly: `pool_size = max(limit × _SEMANTIC_POOL_FACTOR(4), _SEMANTIC_POOL_MIN(20))` (chunk_service.py:143). At `limit=20`, pool_size = max(80, 20) = 80 notes from ANN. This is large enough that expanding to N=20 for the reranker incurs no additional ANN cost — the pool is already ≥80.

---

## 5. Latency Analysis

### Blocking ask (POST /ask/)

| Component | Before reranking | After reranking |
|---|---:|---:|
| Cache lookup | ~1ms | ~1ms |
| Query embedding | ~2ms | ~2ms |
| Note-level ANN (pool=80) | ~20ms | ~20ms |
| Intent arm | ~30ms | ~30ms |
| Score fusion + sort | ~1ms | ~1ms |
| **Subtotal: retrieve_hybrid** | **~93ms** | **~93ms** |
| CrossEncoder.predict (N=20) | — | ~28ms |
| _filter_chunks + _build_context | ~1ms | ~1ms |
| LLM synthesis (Gemini) | ~1500ms | ~1500ms |
| **Total** | **~1595ms** | **~1623ms** |

**Net increase: ~28ms (+1.8%).** The LLM dominates latency; reranking cost is negligible in the blocking path.

### Streaming (POST /ask/stream)

Streaming begins yielding tokens as soon as the LLM starts generating. The current implementation calls `retrieve_hybrid` synchronously before streaming starts (ask_service.py:145). Adding ~28ms of reranking before the stream opens is acceptable for the same reason as the blocking path.

However, because `stream_ask` does not currently parse citations (ask_service.py:159: "Citations are not parsed in the streaming path"), the quality improvement from reranking in the stream path is limited to better context ordering. This is still valuable (primacy effect).

### /retrieve/ and /retrieve/hybrid endpoints

These endpoints (retrieve.py) call `ChunkService.retrieve()` and `ChunkService.retrieve_hybrid()` with `limit=5`. Adding reranking at N=10→K=5 costs ~12ms, acceptable. However, these endpoints are lower-latency targets used by clients who want raw retrieval results. **Reranking should be opt-in on these endpoints via a request parameter.**

### P99 concern

On a cold server start (model not yet loaded), the first request incurs ~300ms of model warm-up. Use eager model loading at application startup to eliminate this.

---

## 6. Cache Strategy

### Full response cache (existing)

`AskService._cache_key()` caches the full response by `SHA-256(user_id + question + provider_sig)` at TTL 3600s (ask_service.py:455). This already absorbs most repeated queries. No change needed here.

### Reranker score cache

The reranker is deterministic: same (query, passage) pairs always produce the same scores. A score-level cache avoids re-running the model on repeated queries within the TTL window, even if the full response cache has expired (e.g., notes were modified).

**Cache key:**
```
rerank:{user_id}:{SHA-256(query_normalised + sorted_chunk_ids)}
```

Sorted chunk IDs make the key stable regardless of the upstream ANN order. This is important because the ANN result order can differ slightly between runs if the vector index is rebuilt.

**Cache backend:** Use the existing `CacheService` (Redis, configured via `REDIS_URL`). The reranker score cache entry is a JSON-serialised list of `(chunk_id, score)` pairs.

**TTL:** `RERANK_CACHE_TTL_SECONDS = 900` (15 minutes). Shorter than the full response TTL (3600s) because new notes ingested by the user should surface quickly. If a note is added, the chunk_id set changes, busting the key naturally.

**Size estimate:** Each entry is ~20 × (8 bytes chunk_id + 8 bytes float) = ~320 bytes. At 1000 daily queries × 3 TTL windows, peak cache size is ~960 KB — negligible.

---

## 7. Prompt Interaction

### Context ordering effect

The system prompt built by `AskService._build_prompt()` (ask_service.py:273) requires the LLM to "Read all retrieved context carefully" and cite by bracket number. The context is assembled in `_build_context_map()` (ask_service.py:303) in the order the chunks appear in the input list.

After reranking, chunk 0 (ref [1] in the prompt) is the passage the cross-encoder considers most relevant to the query. Empirically, LLMs cite earlier passages more often and more accurately (primacy effect). This means:

- **Citation accuracy improves:** hallucinated `[N]` markers decrease because the most relevant passage is cited as `[1]` rather than requiring the LLM to search through 8 references.
- **Answer completeness improves:** the most relevant context is within the first ~500 characters of the context window, well before the 3000-char budget is exhausted.
- **Hallucination rate decreases:** when the answer is at ref [1] rather than ref [7], the LLM is less likely to generate a non-cited claim to fill the gap.

### Token budget interaction

`_build_context_map()` applies a hard 3000-char context budget (ask_service.py:46). If the most relevant passage appears after lower-quality passages consume the budget, it may be truncated. After reranking, the most relevant passage is first and always included in full.

### Instruction alignment

No changes to the system prompt are needed. The instruction "Cite the source of every factual claim using its bracket number, e.g. [1] or [2]" already works correctly with reranked ordering.

---

## 8. API Changes

All changes are additive. No existing API contract is broken.

### `app/core/config.py` — new settings

```python
# Reranking (Phase B)
RERANKING_ENABLED: bool = False          # feature flag; False until benchmark verified
RERANK_CANDIDATE_POOL: int = 20          # stage-1 pool size when reranking is enabled
RERANK_TOP_K: int = 8                    # candidates passed to context after reranking
RERANK_CACHE_TTL_SECONDS: int = 900      # score cache TTL
RERANK_MODEL: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
```

`RERANKING_ENABLED = False` ensures zero behaviour change in production until the benchmark gate (Section 9) is met.

### `app/schemas/ask.py` — response field

```python
class AskResponse(BaseModel):
    # existing fields ...
    reranked: bool = False   # True when reranking was applied to this response
```

Clients can use this field to A/B attribute quality improvements to the reranker.

### `POST /ask/` and `POST /ask/stream`

No request schema change. The reranker is controlled by the server-side feature flag. This avoids exposing a complexity footgun to clients.

### `POST /retrieve/hybrid`

Optional: add `rerank: bool = False` to `RetrieveRequest` (retrieve.py:19). This lets debug clients observe reranked ordering without touching the ask path. Can be added independently.

---

## 9. Benchmark Plan

### Evaluation setup

- Use the existing benchmark harness at `scripts/evaluate_ask.py` with the 50-query benchmark dataset.
- Add a new `RERANK` strategy alongside `SEMANTIC`, `INTENT`, `HYBRID`.
- The `RERANK` strategy uses the full pipeline: `retrieve_hybrid(limit=20)` → `RerankingService.rerank()` → evaluate top-5.
- All four strategies run in the same session against the same database state.

### Metrics to collect

Same as existing benchmark (from `app/evaluation/metrics/retrieval.py`):

| Metric | Current HYBRID | Required RERANK |
|---|---:|---:|
| Precision@5 | 0.244 | ≥ 0.270 |
| Recall@5 | 0.547 | ≥ 0.575 |
| Hit Rate@5 | 0.760 | ≥ 0.790 |
| MRR | 0.607 | ≥ 0.650 |
| Avg Latency (ms) | 93.34 | ≤ 150.00 |

All five gate conditions must be met simultaneously.

### Additional ask-quality metrics (new)

Because cross-encoder reranking primarily improves context ordering (not raw recall), retrieval metrics alone understate the benefit. The benchmark should also measure:

| Metric | Measurement method |
|---|---|
| Citation accuracy | Count `[N]` markers where N is in valid_refs (`_parse_citations`) |
| Citation hallucination rate | Count removed hallucinated markers per query |
| Mean citation position | Average ref number of the first citation in the answer |

A lower mean citation position (e.g., more answers citing [1] rather than [4]) indicates better context ordering and should correlate with reduced hallucination.

### Sample size note

50 queries is sufficient to detect a ΔMRR of 0.04 at p≤0.05 (Wilcoxon signed-rank test). The existing benchmark harness already produces per-query MRR values that support this test.

---

## 10. Risks

### R1 — Latency regression on cold start (Medium)

**Risk:** The cross-encoder model (~22 MB) takes ~300ms to load from disk on first use. If the server restarts frequently or the model is not eagerly loaded, the first post-restart query will be slow.

**Mitigation:** Load `rerank_model` at application startup (in `app/core/rerank_model.py`, imported during the FastAPI lifespan). This ensures warm model by the time any request arrives.

### R2 — Token truncation in cross-encoder (Low)

**Risk:** `ms-marco-MiniLM-L-6-v2` has a max sequence length of 512 tokens. A `(query, chunk_text)` pair that exceeds 512 tokens will be silently truncated, degrading the relevance score for long notes.

**Mitigation:** KnowledgeVault chunks are sentence-split by `ChunkingService` with a target of ~200 tokens. A (query + chunk) pair is typically 230–270 tokens, well within the 512-token limit. Validate during testing: log the fraction of pairs that exceed 400 tokens.

### R3 — Domain mismatch for personal-notes queries (Medium)

**Risk:** MS MARCO is trained on web search queries. Personal notes use a different register: shorthand ("tell Sid about hackathon"), intent-based queries ("things I need to do"), and named entities ("Siddhant"). The cross-encoder may mis-rank because it expects natural-language questions.

**Mitigation:** The benchmark (Section 9) directly tests this. If MRR fails to reach 0.650, it confirms domain mismatch and the reranker is not activated. A future mitigation would be fine-tuning on a sample of KnowledgeVault queries, but this is out of scope for this design.

### R4 — Intent arm becomes redundant (Low)

**Risk:** If the cross-encoder correctly elevates intent-relevant notes (e.g., "things to tell Sid" → communication notes), the intent arm's 0.340 accuracy provides no additional signal.

**Assessment:** This is acceptable. If reranking subsumes the intent arm's benefit at lower complexity, the intent arm weight can be reduced in a future cleanup sprint. This is not a blocking risk.

### R5 — Cache invalidation complexity (Low)

**Risk:** The reranker score cache key includes chunk IDs. If a note is re-indexed (chunks deleted and recreated, as happens in `ChunkService.process_note()` at chunk_service.py:84), chunk IDs change and the cache key changes naturally. No explicit invalidation is needed.

**Assessment:** Key busting is implicit and correct.

---

## 11. Testing

### Unit tests

| Test | File | What to assert |
|---|---|---|
| `test_reranking_service.py` | `tests/` | Mock `CrossEncoder.predict`; verify output is sorted by reranker score descending |
| `test_reranking_service.py` | `tests/` | Verify top_k truncation: input 20 candidates → output 8 |
| `test_reranking_service.py` | `tests/` | Verify cache hit: same (query, chunk_ids) returns cached scores without calling predict |
| `test_ask_service_reranking.py` | `tests/` | Patch `RERANKING_ENABLED=True`; verify `reranked=True` in response |
| `test_ask_service_reranking.py` | `tests/` | Patch `RERANKING_ENABLED=False`; verify `reranked=False` and original ordering preserved |

### Integration tests

| Test | What to check |
|---|---|
| `test_ask_integration_rerank.py` | End-to-end: `POST /ask/` with `RERANKING_ENABLED=True` returns `reranked: true` and a valid answer |
| Latency smoke test | Average retrieval+rerank time ≤ 150ms over 10 consecutive requests (warm model) |

### Evaluation benchmark

Run `scripts/evaluate_ask.py` with the `RERANK` strategy. Compare to `HYBRID` baseline. All five gate conditions in Section 9 must pass before `RERANKING_ENABLED` is set to `True` in production `.env`.

### Regression tests

The existing test suites (`test_ask_citations.py`, `test_ask_judge.py`, `test_ask_models.py`, `test_ask_runner.py`) must pass unchanged with `RERANKING_ENABLED=False`. This is the default and must remain the default until the benchmark gate clears.

---

## 12. Definition of Done

A PR implementing cross-encoder reranking is considered complete when:

- [ ] `app/core/rerank_model.py` exists and eagerly loads `cross-encoder/ms-marco-MiniLM-L-6-v2` at startup.
- [ ] `app/services/reranking_service.py` exists with a `rerank(query, candidates, top_k)` method and a Redis-backed score cache.
- [ ] `AskService.ask()` and `AskService.stream_ask()` call `RerankingService.rerank()` when `settings.RERANKING_ENABLED is True`.
- [ ] `AskResponse` carries `reranked: bool`.
- [ ] `RERANKING_ENABLED = False` is the default in `config.py` and `.env.example`.
- [ ] All unit tests in `tests/test_reranking_service.py` pass.
- [ ] All existing ask tests pass with `RERANKING_ENABLED=False`.
- [ ] Benchmark run with `RERANK` strategy shows:
  - Precision@5 ≥ 0.270
  - Recall@5 ≥ 0.575
  - Hit Rate ≥ 0.790
  - MRR ≥ 0.650
  - Avg retrieval+rerank latency ≤ 150ms
- [ ] Mean citation position is lower than HYBRID baseline (better context ordering).
- [ ] `RERANKING_ENABLED = True` set in production `.env` after all benchmark gates clear.
