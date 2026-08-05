# KnowledgeVault Retrieval Pipeline — Engineering Audit
**Date:** 2026-08-03  
**Scope:** Full retrieval path from HTTP entry-point to LLM synthesis  
**Benchmark baseline:** v2.0.0 (205 verified queries, 50-query eval set)  
**Status:** Analysis only — no implementation

---

## PART 1 — COMPLETE PIPELINE ANATOMY

---

### Stage 1: HTTP Entry Point
`app/api/routes/ask.py`

**What is happening?**  
A POST request arrives at `/ask/` or `/ask/stream`. Auth is verified, a `Session` is injected, and control passes immediately to `AskService`. No preprocessing of the question occurs at this layer.

**Why was it designed this way?**  
Clean separation of concerns. The route is deliberately thin — auth + routing only.

**Weaknesses:**
- The question string is passed to the service completely raw. No normalization (whitespace collapse, unicode normalization, strip punctuation) occurs before caching, embedding, or intent extraction.
- The cache key (`_cache_key`) normalizes to lowercase before hashing, but the LLM sees the original string. A mismatch between cached and live queries is unlikely but possible.
- There is no request validation beyond Pydantic's required field. Empty string, single character, and 50,000-character queries all pass through identically.

**Measured by Benchmark?** No — the benchmark exercises the internal service methods, not HTTP.

**Theoretical only?** Yes for most weaknesses. Edge case production bugs only.

---

### Stage 2: Cache Check
`AskService.ask()`, `CacheService.get/set`, `app/services/cache_service.py`

**What is happening?**  
Cache key = SHA-256(`user_id + normalised_question + provider_priority`). Checks Redis. On hit, returns immediately. On miss, records a metric and continues.

**Why designed this way?**  
The full pipeline (embedding + ANN + intent + LLM) is expensive. A 1-hour TTL (configurable) avoids re-running identical questions.

**Weaknesses:**
- The cache is keyed on normalised question + provider signature only. A semantically equivalent but differently phrased question ("What startup ideas do I have?" vs "Show me startup ideas") produces a cache miss. This is correct but means latency savings are lower than expected for conversational users.
- Degraded (retrieval-only) responses are NOT cached. If the LLM is down, every request for a popular question re-runs retrieval and re-hits the LLM.
- `stream_ask()` is explicitly uncacheable. If the user switches between the streaming and blocking API for the same question, they re-run retrieval.
- No negative caching for "no results" queries. If a query returns empty every time, it still hits retrieval on every cache-miss.

**Measured by Benchmark?** No. The evaluation path (`ask_with_context`) bypasses the cache entirely.

**Theoretical only?** The per-question cache miss rate weakness is real in production. Others are theoretical.

---

### Stage 3: Embedding the Query
`ChunkService.retrieve_hybrid()` → `embedding_model.encode(query)`  
`app/core/embedding_model.py`

**What is happening?**  
`SentenceTransformer("all-MiniLM-L6-v2")` encodes the raw query string into a 384-dimensional float vector. This model runs locally in the same process. The call is synchronous and runs on CPU.

**Why designed this way?**  
`all-MiniLM-L6-v2` is a 22M-parameter model that runs fast on CPU (~15-35ms per query). It was chosen during initial prototyping as a reliable general-purpose sentence encoder.

**Weaknesses:**

1. **Vocabulary gap — the root cause of most benchmark misses.** `all-MiniLM-L6-v2` is trained on MS MARCO, NLI, and similar general-web corpora. Personal notes have a different vocabulary distribution: short jottings ("OOP revision"), technical shorthand ("K8s cluster"), and self-referential queries ("my AI research reading goals"). The model's training data did not include personal note-taking style, so it encodes personal queries poorly relative to how it encodes formal text.

2. **Query-document asymmetry.** Personal notes are often written imperatively or as fragments: "Tell Sid about the hackathon", "Redis LRU eviction policy notes". Queries are often phrased as natural language questions: "What should I tell Sid about?", "How does Redis eviction work?". The model is trained to bridge this gap, but struggles at the extremes of the personal-note vocabulary.

3. **No query preprocessing.** Stopwords, punctuation, and filler phrases ("Show my", "Show me", "Tell me about") are encoded as semantic signal. This pulls the query vector away from the note vector even when the core topic is identical.

4. **Single embedding per query.** A query like "Show my AI research reading goals" could equally be interpreted as about AI, research, reading, or goals. A single embedding averages these semantics into one vector that is the centroid of all interpretations — often worse than any single interpretation.

5. **Model dimension (384) is on the low end.** Larger models (768d, 1024d) capture finer-grained semantic distinctions, particularly for technical vocabulary.

**Measured by Benchmark?**  
Yes, directly. Benchmark queries 2, 10, 11, 26, 30, 38 all produce HitRate=0.0 under SEMANTIC strategy. The common pattern is a vocabulary mismatch between the query phrasing and the note content.

**Theoretical only?** No. This is the single most measurable source of quality loss.

---

### Stage 4: ANN Search (Semantic Arm)
`EmbeddingRepository.search_similar_notes_with_distance()`

**What is happening?**  
pgvector `<=>` (cosine distance) over note-level embeddings. Returns the top `pool_size = max(limit × 4, 20)` notes ordered by cosine distance. At pool=20 (the Pareto-optimal point chosen by the pool experiment), fetches top-80 note-level distances.

**Why designed this way?**  
ADR-003 chose note-level embeddings for the semantic arm of hybrid retrieval after observing that chunk-level retrieval returned multiple chunks from the same note, consuming top-K slots and lowering diversity. The note embedding is the mean of the note's content.

**Weaknesses:**

1. **Note-level embedding averages away specificity.** A 2,000-character note about Redis, PostgreSQL, and Nginx has an embedding that is the centroid of all three topics. A query specifically about Redis cosine-matches poorly if the Redis discussion is ⅓ of the note. This is the fundamental trade-off made in ADR-003 that needs re-examination.

2. **No HNSW index status visible.** The code uses pgvector's cosine distance but there is no evidence that HNSW indexes are configured on the embeddings tables. Without HNSW/IVFFlat, pgvector defaults to a full sequential scan. At 1,055 notes this is acceptable (~35ms), but at 10,000+ notes performance degrades linearly.

3. **Distance-to-score conversion.** `score = 1 - cosine_distance`. For cosine distance ∈ [0, 2], this can produce negative scores when distance > 1.0. The code clamps to [0, 1] via `max(0.0, min(1.0, ...))` which is correct but means all distances > 1.0 are collapsed to score 0.

4. **Tie-breaking by note_id ASC.** When two notes have the same ANN distance (which happens frequently in pgvector with quantized cosines), the older note wins. This systematically biases against recently created notes, which is counter to recency-preference intuitions for personal note-takers.

5. **The pool ceiling.** `pool_size = max(limit × 4, 20)`. At limit=8 (production default when RERANKING_DISABLED), pool=max(32, 20)=32. But the pool experiment shows recall plateaus at pool=20 (semantic pool=80). The constant `_SEMANTIC_POOL_MIN=20` is therefore the binding constraint, not the multiplier. This means regardless of the limit argument, the minimum fetch is always 20.

**Measured by Benchmark?**  
Indirectly. The SEMANTIC strategy measures exactly this path's quality: Hit Rate 0.760, MRR 0.612. 24% of queries (12/50) get zero relevant results from this path.

---

### Stage 5: Intent Arm (Fast Classifier + Category Search)
`IntentCategoryService.find_category_matches_for_query()` → `extract_query_intent_fast()`

**What is happening?**  
Two sub-stages:

**5a. Fast keyword classifier** (`extract_query_intent_fast`): Tokenizes query, checks word-set intersection against 8 keyword groups in priority order. Extracts pseudo-actor (for communication) and pseudo-topic. Returns `intent_type`, `confidence` (0.5-0.72), `actor`, `topic`. Takes ~microseconds. No LLM.

**5b. Category search**: Uses intent type + actor + a vector search over category centroids to find matching categories. Also does an exact name lookup and rule-based match. Merges results with scoring (canonical=0.96, exact_rule=0.92, vector=0.0-1.0+boosts).

**Why designed this way?**  
The LLM-based classifier would add 800-2,000ms latency per query. The fast classifier was designed to avoid blocking retrieval. Category matching provides an orthogonal evidence signal to semantic similarity.

**Weaknesses:**

1. **54% fast classifier accuracy.** The benchmark history shows the fast classifier measuring 54% on the 50-query gate. On the 152-query diagnostic set, accuracy is only ~29%. This means the intent arm has the wrong intent type roughly half the time. When wrong, it retrieves notes from the wrong category, which the fusion then promotes.

2. **First-match wins (no confidence weighting).** The keyword groups are checked in priority order and the first match terminates. "Show my AI research reading goals" contains "show" which isn't in any group, "research" is in STUDY keywords → classified as "study". But "Show my finance reminders" → "finance" not in any keyword → falls to "general" (misclassified as reminder by a different path). The classifier has no way to express mixed signals.

3. **Intent arm almost never wins over semantic.** The intent-only arm achieves Hit Rate=0.280, MRR=0.221 — far below semantic. In the fusion, intent-only notes get `semantic_score = _text_overlap_score()` (keyword overlap), which for most notes is 0.2-0.4. The maximum boost is `_MAX_INTENT_BOOST = 0.12`, bringing maximum intent-only fusion score to ~0.52. A strong semantic hit scores 0.7-0.9. Intent-only notes almost never displace semantic hits.

4. **Category fragmentation 65.7%.** Of 105 categories, 69 contain only 1 note. When the fast classifier correctly identifies the intent and category, there is only a 34.3% chance the category has more than 1 note. For singleton categories, intent retrieval returns at most 1 note (the founding member).

5. **6 duplicate category patterns.** "Docker" and "Reference - Docker" are separate categories. The same note could have been assigned to either, depending on creation order. Query-time intent routing to one category misses notes in the other.

6. **Intent arm contributes overhead without proportional recall gain.** Hybrid latency is 93-140ms vs semantic at 25-35ms. The intent arm adds ~70ms of overhead. Yet HYBRID Hit Rate (0.740) is LOWER than SEMANTIC (0.760) in the sprint2b_final report. The intent arm is currently net-negative on recall in most benchmark runs.

7. **Confidence gate set at 0.55 for intent influence.** `_MIN_CONFIDENT_INTENT = 0.55`. The fast classifier's maximum non-actor confidence is 0.65. The confidence factor therefore ranges from 0 to (0.65-0.55)/(1-0.55)=0.22. The maximum intent contribution is `0.22 × match_score × 0.12 = 0.026`. This means intent can add at most 2.6% to the fusion score — mathematically negligible.

**Measured by Benchmark?**  
Yes. Intent accuracy (34-46% depending on run), category accuracy (30-50%), and INTENT strategy Hit Rate (0.220-0.280) are directly measured.

---

### Stage 6: Candidate Fusion
`ChunkService.retrieve_hybrid()` — fused dict construction

**What is happening?**  
All notes from semantic arm are seeded into a `fused` dict. Intent-arm notes are then merged in. For notes appearing in both arms: intent_category, intent_score, and the source tag are updated; the score is recomputed as `semantic_score + boost`. The deterministic tie-break is: score DESC, semantic_score DESC, intent_score DESC, lower note_id first (older wins), lower chunk_index first.

**Why designed this way?**  
Early-fusion weighted by hand-tuned constants (0.65/0.35) — a pragmatic starting point. Note-level deduplication was a deliberate ADR-003 decision to prevent one note consuming multiple top-K slots.

**Weaknesses:**

1. **Fixed weights not evidence-based.** The 0.65/0.35 split was chosen intuitively. The benchmark shows the intent arm (at 0.35 weight) is net-negative. No A/B weight search was performed.

2. **No Reciprocal Rank Fusion (RRF).** RRF is the literature-standard method for combining multiple ranked lists. It is rank-position-based, not score-based, which makes it robust to scale differences between semantic cosine scores (0.0-1.0) and text-overlap scores (0.0-1.0). Score-based fusion suffers when the two arms produce scores on different effective scales.

3. **Older notes win ties.** The tie-break `note_id ASC` means that for queries where many notes are equidistant in embedding space (common when notes share vocabulary), older notes systematically appear first. Personal note-takers typically want recent notes first.

4. **`_best_chunk()` uses text overlap, not embedding.** After selecting which note to retrieve, the "best chunk" within that note is selected by `_text_overlap_score(query, chunk_text)` — simple keyword overlap. This is a different (and weaker) scoring function than the ANN used for note selection. The mismatch means:
   - The note was selected based on semantic relevance.
   - The chunk shown in context was selected by keyword frequency.
   - These two selectors can produce different top results.

5. **`_text_overlap_score` tie-break goes to lower chunk_index.** When two chunks have equal keyword overlap, the earlier chunk wins. For notes where the key content is in the middle or end (e.g., a long note with a conclusion section), this consistently returns the wrong chunk.

6. **No explicit deduplication of content at fusion stage.** Two semantically similar notes can both appear in the top-K, consuming slots. Content dedup only happens at context construction time (by 80-char fingerprint), but by then, slot allocation has already happened.

**Measured by Benchmark?**  
Indirectly. The gap between SEMANTIC and HYBRID precision/recall is the direct measurement of fusion quality.

---

### Stage 7: Optional Reranking
`RerankingService.rerank()` — currently DISABLED

**What is happening?**  
`RERANKING_ENABLED=False`. When disabled, `RerankingService.rerank()` returns candidates unchanged with `reranked=False`. The cross-encoder model (`ms-marco-MiniLM-L-6-v2`) is loaded but not invoked.

**Why disabled?**  
ADR-003 addendum: benchmark showed RERANK strategy (Precision=0.172, Recall=0.403, Hit Rate=0.640, MRR=0.483) worse than SEMANTIC on all metrics. The `ms-marco-MiniLM-L-6-v2` model was trained on MS MARCO web search, which has query-document pairs very different from personal note queries and personal note documents. Domain mismatch caused regressions.

**Weaknesses:**

1. **Domain mismatch is the core problem, not cross-encoding itself.** MS MARCO cross-encoders are trained on (web query, web document) pairs. Personal notes are structurally different: short, imperative, sometimes in first person, often incomplete sentences. A cross-encoder fine-tuned on personal note data would likely help.

2. **The model selection was limited.** `ms-marco-MiniLM-L-6-v2` is one specific architecture. `cross-encoder/nli-deberta-v3-small` or `BAAI/bge-reranker-base` have different training distributions and might perform differently.

3. **Currently the reranker rewrites scores but doesn't expand the pool.** At `RERANKING_ENABLED=True`, pool is fetched, then top_k=8 kept after reranking. Since the cross-encoder consistently demoted correct results, the effective recall was lower than the pool contained.

4. **No fallback to original ordering on score degradation.** If reranker scores are below a confidence threshold, the system has no way to detect "reranker was uncertain, revert to semantic ordering."

**Measured by Benchmark?**  
Yes. RERANK strategy is explicitly measured and confirmed net-negative.

**Theoretical only?** No — empirically confirmed regression.

---

### Stage 8: Score Filtering
`AskService._filter_chunks()` → `settings.RETRIEVAL_MIN_SCORE = 0.10`

**What is happening?**  
After retrieval and optional reranking, chunks with score < 0.10 are removed before context construction. At pool=20 returning 8 candidates, scores typically range from 0.6-0.9, so this filter almost never fires in practice.

**Why designed this way?**  
To prevent very low-confidence noise from entering the prompt. The 0.10 threshold was set conservatively to avoid filtering real results.

**Weaknesses:**

1. **Threshold is too low to be meaningful.** All scores from `1 - cosine_distance` are at least 0.5 for any plausible match. A threshold of 0.10 means nothing in practice — it only fires when distance > 0.90, which would mean a completely unrelated note.

2. **Filtering after returning from retrieval** is the wrong place. Low-quality results should be filtered before they take up pool slots, not after. The current approach fetches N, then discards, potentially returning fewer than the intended K.

3. **No dynamic thresholding.** A fixed threshold doesn't adapt to query difficulty. For a query with strong matches (scores 0.85-0.95), anything below 0.7 is noise. For a query with weak matches (scores 0.45-0.60), 0.10 keeps everything.

**Measured by Benchmark?**  
Indirectly. The benchmark sometimes produces 0 results for certain intent queries (e.g., Q3 "How can I improve my health?" via INTENT returns `[]`), likely because the intent category is empty after filtering.

**Theoretical only?** Mostly theoretical at current corpus size.

---

### Stage 9: Context Construction
`AskService._build_context_map()`, `_MAX_CONTEXT_CHARS = 3,000`

**What is happening?**  
Chunks are deduplicated by 80-char fingerprint (first 80 chars of normalised text). Entries are then greedily packed into a 3,000-character string. Each entry format: `[N] Category | Note Title\nChunk Text`. Reference numbers [1], [2], ... are assigned in order.

**Why designed this way?**  
Leaves "headroom for instructions + answer" within an assumed ~750-token budget. This was set conservatively when using smaller LLMs.

**Weaknesses:**

1. **3,000 chars is severely limiting.** 3,000 chars ≈ 750 tokens. The system prompt itself uses ~250 tokens, leaving only ~500 tokens for context. At 500 chars/chunk (one chunk per note), only ~4-5 chunks fit. For benchmark query Q32 "What are the project requirements for KnowledgeVault?" with 8 relevant notes, only 1-2 can appear in context.

2. **Gemini 2.0 Flash has 1,000,000 token context window.** Using only 500 tokens of context wastes 99.95% of available context. Even at 8,000 chars (2,000 tokens), the model sees 4× more evidence.

3. **Linear pack (no priority awareness).** Chunks are packed in the order they were retrieved (rank order). But if chunk 1 is 1,200 chars and chunks 2-5 are 200 chars each, chunk 1 consumes 40% of the budget and chunks 2-5 together consume another 26%, leaving room for only 6 entries total. A smarter strategy would allocate budget per-entry proportionally or truncate individual chunks.

4. **80-char fingerprint dedup can produce false positives.** Two distinct chunks that begin with the same 80 characters (e.g., two notes that both start with "Redis is an in-memory data structure store.") would be deduped, dropping the second even if it contains different subsequent content.

5. **Partial chunk truncation at budget boundary.** When the last chunk doesn't fit entirely, the code appends a truncated version with "…" if `remaining > 100`. This produces incomplete chunks in the LLM context, potentially cutting off the relevant information at the end of a large chunk.

**Measured by Benchmark?**  
Indirectly. Low precision scores (0.244) despite adequate recall (0.547) suggest context truncation is causing the LLM to cite fewer sources or miss multi-note information.

---

### Stage 10: Prompt Construction
`AskService._build_prompt()`, `AskService._parse_citations()`

**What is happening?**  
A single-shot prompt with XML tags: `<context>`, `<question>`, then numbered instructions. The LLM is asked to write 2-5 sentences, use [N] citations, and say "I could not find..." if no answer is found.

**Why designed this way?**  
Standard RAG prompt pattern. Single-shot avoids multi-turn complexity.

**Weaknesses:**

1. **No prompt versioning in the cache key.** If the prompt template is changed, cached answers from the old prompt are returned for up to 1 hour. The cache key includes `provider_sig` but not a prompt hash.

2. **The "2-5 sentence" instruction forces brevity on complex multi-note queries.** Q32 has 8 relevant notes; a 2-5 sentence answer cannot synthesize 8 sources well.

3. **Citation validation removes hallucinated refs but not all hallucinations.** The `_parse_citations()` method removes [N] where N > len(context_map), but cannot detect content hallucinations (facts stated without citation).

4. **No few-shot examples in the prompt.** The prompt has zero-shot instructions. Few-shot examples of good citation style would improve citation accuracy.

5. **"Do not explain your reasoning" instruction conflicts with multi-source synthesis.** For complex queries requiring synthesis across multiple notes, brief reasoning improves answer quality.

**Measured by Benchmark?**  
The evaluation framework judges retrieval (note IDs), not answer quality. Prompt weaknesses are not measured by the current benchmark.

---

### Stage 11: LLM Generation
`LLMService.generate()` → `GeminiProvider` → `GroqProvider` fallback

**What is happening?**  
Gemini 2.0 Flash is called first. On failure (429, 5xx, timeout, JSON error), falls through to Groq llama-3.3-70b-versatile. If both fail, returns `retrieval_only_response`.

**Why designed this way?**  
Provider redundancy without per-call cost overhead. Gemini is preferred for quality, Groq as a fast fallback.

**Weaknesses:**

1. **No streaming in the blocking path.** `ask()` blocks until LLM generates the full response (~5-50 seconds for long answers). `stream_ask()` fixes this for the frontend but returns no citations.

2. **Citations not parsed in the stream path.** "Citations are not parsed in the streaming path (Sprint 4-C)." This creates a permanent quality asymmetry between stream and blocking paths.

3. **No token count tracking.** The service sends prompts without knowing how many tokens are consumed. If the model truncates long prompts silently, quality degrades undetected.

4. **Temperature not controlled.** The Gemini and Groq calls use default temperature settings. For factual retrieval synthesis, temperature=0 is more appropriate for reproducibility.

---

### Stage 12: Indexing (Upstream of Retrieval)
`ChunkService.process_note()`, `ChunkingService.split()`

**What is happening?**  
Notes are split into chunks of ~500 chars with 50-char overlap. A naive regex sentence splitter (`(?<=[.!?])\s+`) is used. Chunks are individually embedded by `all-MiniLM-L6-v2` and stored in `ChunkEmbedding`. A separate note-level embedding (whole note concatenated) is stored in `Embedding`.

**Why designed this way?**  
Dual embedding: chunk-level for potential precise retrieval, note-level for hybrid's semantic arm (ADR-003).

**Weaknesses:**

1. **500-char chunk is ~100-125 tokens.** This is below the recommended 200-512 token range for semantic coherence. Chunks this small often lack enough context for the model to understand what they're about. A chunk like "Redis uses LRU eviction by default" has enough semantic signal, but "The configuration involves setting maxmemory-policy to" does not — it's incomplete without surrounding context.

2. **50-char overlap is ~10-12 tokens.** This is insufficient. Production RAG systems typically use 100-200 token overlap. Boundary-spanning sentences (split at exactly 500 chars) lose both sides of their context.

3. **Regex sentence splitter breaks on bullets, lists, headers.** A note formatted as a Markdown bullet list (`- Redis: in-memory\n- PostgreSQL: relational`) is not split by the sentence splitter (no `. `, `! `, or `? `) and becomes a single "sentence" — either one huge chunk or one that overflows into hard-split at arbitrary character positions.

4. **Hard split breaks tokens.** When a sentence exceeds 500 chars, `_hard_split()` cuts at byte boundaries, potentially splitting words or mid-sentence.

5. **Chunk embeddings are not used for retrieval.** Despite the infrastructure to embed and store chunks, the retrieval path (`retrieve_hybrid`) uses `search_similar_notes_with_distance()` (note-level), not `search_similar_chunks_with_distance()`. The chunk embeddings exist in the database but are unused in the hybrid path. The only time chunk-level search runs is in the legacy `retrieve()` endpoint, which is not used by production ASK.

6. **No note title in chunk text.** The chunk is stored as raw content text without the note title prepended. When the chunk is later displayed in context (`[N] Category | Title\nChunk text`), the title is added at display time. But the chunk embedding was trained on text without the title. This means chunk embedding does not benefit from the note title's semantic signal.

**Measured by Benchmark?**  
Indirectly. The chunk selection (`_best_chunk`) affects which text appears in the LLM context.

---

## PART 2 — WHERE QUALITY IS CURRENTLY BEING LOST

Based on the full pipeline audit, here is the loss budget:

| Source of Loss | Queries Affected | Estimated Metric Impact |
|---|---|---|
| **Vocabulary gap** (model/query style mismatch) | 12/50 complete misses | −0.15 Hit Rate, −0.12 MRR |
| **Note-level embedding averages away specificity** | ~8/50 partial misses | −0.08 Recall |
| **Intent arm net-negative** (wrong category injected) | ~6/50 queries harmed | −0.02 Hit Rate |
| **Context window too small** (3,000 chars) | All multi-note queries | −0.10 Precision (LLM synthesis only) |
| **Chunk-level embeddings unused** | All queries | −0.05 Recall (estimated) |
| **No lexical fallback** | Exact-match queries | −0.05 Hit Rate |
| **Small overlap (50 chars)** | Boundary-spanning queries | −0.03 Recall |
| **_best_chunk by keyword, not embedding** | All queries | −0.02 Recall (context quality) |

**The 24% complete miss rate (12/50 queries with Hit=False on SEMANTIC) is the most critical signal.** These are queries where the pipeline returns zero relevant documents — no amount of fusion, reranking, or prompt tuning can recover from this. The root cause is the vocabulary gap between queries and note embeddings.

---

## PART 3 — TOP 10 RETRIEVAL IMPROVEMENTS

---

### Improvement 1 — BM25 Sparse Retrieval Arm (Lexical Hybrid)
**Priority: 1 — Highest ROI**

**Description:** Add a BM25 (Best Match 25) keyword search arm alongside the existing semantic vector search. Use `rank_bm25` or implement via PostgreSQL's native full-text search (`tsvector/tsquery`). Merge BM25 ranks with ANN ranks using Reciprocal Rank Fusion (RRF): `score_rrf = 1/(k+r_semantic) + 1/(k+r_bm25)` where k=60 (standard), and r is rank position.

**Why it should improve retrieval:**  
BM25 is the gold standard for lexical recall. The benchmark's most consistent failures are exact vocabulary matches: "OOP revision" (notes about "Object-Oriented Programming"), "theory of relativity" (notes that contain those exact words), "Redis and PostgreSQL reference notes" (exact term match). BM25 would find all of these directly. Production RAG systems (BEIR benchmark, Elasticsearch RAG) consistently show hybrid BM25+dense outperforms either alone by 5-15pp on recall. Personal note corpora — where vocabulary is user-defined and idiosyncratic — benefit disproportionately from lexical search because they contain unusual exact phrases.

**Expected metric improvement:**
- Hit Rate: +0.10 to +0.15 (recovering 5-7 of the 12 complete misses)
- Recall@5: +0.06 to +0.12
- MRR: +0.04 to +0.08
- Precision: minimal change (same K=5 window)

**Expected latency impact:** +5-15ms (PostgreSQL `@@` operator with `GIN` index is extremely fast; `rank_bm25` in-process is also fast). Negligible relative to current 93ms hybrid baseline.

**Engineering complexity:** Medium. Requires: (a) building a BM25 corpus at index time (note text → BM25 index), (b) adding a query-time BM25 search call, (c) implementing RRF merging, (d) replacing the current score-based fusion with rank-based fusion. PostgreSQL `tsvector` variant is lower complexity since no new dependency is needed.

**Risk:** Low. BM25 is additive — if it returns nothing (empty query, no vocabulary overlap), RRF gracefully falls back to pure semantic ranking. Cannot regress below current SEMANTIC baseline.

**Should be A/B benchmarked?** Yes. Run full Benchmark v2.0.0 against SEMANTIC baseline.

**Estimated implementation time:** 3-4 days (PostgreSQL tsvector variant), 5-7 days (standalone BM25 with offline index).

---

### Improvement 2 — Increase Context Window from 3,000 to 12,000 Characters
**Priority: 2 — Immediate win, zero retrieval risk**

**Description:** Increase `_MAX_CONTEXT_CHARS` from 3,000 to 12,000. No other changes needed. Gemini 2.0 Flash supports 1M token context.

**Why it should improve retrieval:**  
This does not improve retrieval recall (notes in top-K do not change) but dramatically improves answer synthesis quality. Currently only 4-5 chunks fit in context. At 12,000 chars (~3,000 tokens for context), 20+ chunks fit. For benchmark queries with 4-8 relevant notes (Q32, Q33, Q38, Q46), the LLM now sees all relevant notes, improving both citation density and answer completeness. This directly targets the Precision gap (0.244 Precision vs 0.547 Recall — only ~45% of retrieved relevant notes are effectively used).

**Expected metric improvement:**
- The current benchmark measures retrieval, not answer quality. This improvement affects the answer synthesis stage.
- For retrieval metrics: no change.
- For a future answer-quality benchmark: expected +0.15-0.25 answer accuracy.
- Immediately visible improvement in end-user perceived quality.

**Expected latency impact:** Gemini 2.0 Flash processes the longer context in ~same time due to its efficient attention implementation. LLM generation may increase by 1-3 seconds for longer answers. Overall latency change: +1-3s for LLM, negligible for retrieval.

**Engineering complexity:** Trivially low. One integer constant change.

**Risk:** None for retrieval. Slight risk of LLM hallucinating more with more context ("lost in the middle" problem). Mitigation: keep the instruction "only cite from provided context."

**Should be A/B benchmarked?** No — this does not change retrieval metrics measured by the current benchmark. Defer to a future answer-quality benchmark.

**Estimated implementation time:** 15 minutes.

---

### Improvement 3 — HyDE: Hypothetical Document Embedding for Query Expansion
**Priority: 3 — High impact on vocabulary gap**

**Description:** Before embedding the user query, use a fast LLM call to generate a hypothetical note that would answer the query. Embed the hypothetical note instead of (or in addition to) the raw query. This is the "Hypothetical Document Embeddings" technique (Gao et al., 2022). Example: "Show my AI research reading goals" → hypothetical: "AI and machine learning reading list: papers on transformers, BERT, GPT, research goals for 2024 including survey papers and tutorial books." → embed this → ANN search. The hypothetical document's embedding is far closer to actual study notes about AI than the raw query embedding.

**Why it should improve retrieval:**  
HyDE has shown 5-10pp recall improvements on knowledge-base retrieval tasks (BEIR). It is particularly effective when queries are short and use vocabulary ("Show my...", "What are my...") that doesn't appear in the indexed documents. The personal note vocabulary issue is exactly the use case HyDE is designed for. The hypothetical document is generated in query-style familiar to the LLM but embedding-style familiar to the indexed corpus.

**Expected metric improvement:**
- Hit Rate: +0.06 to +0.12 (targeting the "vocabulary gap" misses)
- Recall@5: +0.04 to +0.09
- MRR: +0.03 to +0.07

**Expected latency impact:** +300-800ms for the Gemini HyDE generation call. This is significant. Mitigation: (a) use a fast lightweight LLM call (Groq llama-3.1-8b with max_tokens=100), reducing to +100-200ms; (b) use cached hypothetical documents for repeated queries; (c) implement async — run HyDE in parallel with the main semantic search, then merge results when both complete.

**Engineering complexity:** Medium. Requires: (a) a new HyDE LLM call in the retrieval path, (b) a second `embedding_model.encode()` call, (c) modified ANN search or secondary ANN search, (d) score merging from two query embeddings (take max per note, or average scores).

**Risk:** Medium. If the LLM generates a misleading hypothetical document, recall degrades. Mitigation: run HyDE in parallel with original query embedding and take the union/max-score, so the original query always contributes evidence.

**Should be A/B benchmarked?** Yes. Full Benchmark v2.0.0 with HyDE vs SEMANTIC baseline.

**Estimated implementation time:** 4-6 days.

---

### Improvement 4 — Chunk-Level ANN Search with Chunk Deduplication
**Priority: 4 — Architectural fix for note-level averaging problem**

**Description:** Replace `search_similar_notes_with_distance()` with `search_similar_chunks_with_distance()` in the hybrid retrieval path's semantic arm. After chunk-level ANN, deduplicate to one chunk per note (keeping the highest-scoring chunk). This gives the ANN search access to the specific section of a note that is most relevant, rather than the whole-note average.

**Why it should improve retrieval:**  
A note about Redis, PostgreSQL, and Nginx has three different embedding attractors. At note-level, the embedding is the average of all three — far from any individual query about just Redis. At chunk level, the Redis-specific chunk has an embedding very close to a query about Redis. This is the standard RAG architecture (chunk-first ANN, then note-level dedup). The current "note-first" approach was adopted to avoid slot consumption, but chunk-level + dedup achieves the same diversity guarantee while using more specific embeddings.

**Expected metric improvement:**
- Hit Rate: +0.04 to +0.08 (particularly for multi-topic notes)
- Recall@5: +0.05 to +0.10
- MRR: +0.03 to +0.06

**Expected latency impact:** Chunk-level ANN searches a larger table (~5× more rows — one chunk table entry per 500-char chunk per note). At 1,055 notes with avg 3-5 chunks each, that's ~4,000 chunk embeddings. ANN over 4,000 vs 1,055 rows adds ~5-10ms. With HNSW indexing, the difference is negligible.

**Engineering complexity:** Medium. `ChunkEmbeddingRepository.search_similar_chunks_with_distance()` already exists and is unused in the hybrid path. Requires: (a) switching the semantic arm call, (b) implementing note-level deduplication (keep max-score chunk per note_id), (c) updating `_best_chunk()` to return the already-selected chunk rather than re-running keyword overlap.

**Risk:** Low-medium. The existing chunk-level infrastructure already works. The main risk is a latency regression at larger corpus sizes (mitigated by HNSW index).

**Should be A/B benchmarked?** Yes. Full Benchmark v2.0.0 comparison.

**Estimated implementation time:** 3-4 days.

---

### Improvement 5 — Embedding Model Upgrade: all-MiniLM-L6-v2 → BAAI/bge-small-en-v1.5 or all-mpnet-base-v2
**Priority: 5 — Highest potential but requires re-indexing**

**Description:** Replace `all-MiniLM-L6-v2` (22M params, 384d, general-purpose) with a retrieval-optimized model. Two candidates:
- `BAAI/bge-small-en-v1.5` (33M params, 384d, retrieval-tuned on MTEB, instruction-aware)
- `all-mpnet-base-v2` (110M params, 768d, stronger general-purpose)

**Why it should improve retrieval:**  
`all-MiniLM-L6-v2` ranks 136th on the MTEB retrieval benchmark. `bge-small-en-v1.5` ranks 27th (same parameter count, 3× better retrieval). `bge-small-en-v1.5` supports instruction prefixes: "Represent this sentence for searching relevant passages: {query}". Adding instruction prefixes further reduces the query-document asymmetry problem. In production RAG benchmarks (BEIR, MTEB), model upgrades within the same size class typically yield 5-12pp recall improvement.

**Expected metric improvement:**
- Hit Rate: +0.06 to +0.12
- MRR: +0.05 to +0.10
- Recall@5: +0.05 to +0.12

**Expected latency impact:**
- `bge-small-en-v1.5`: same latency as `all-MiniLM-L6-v2` (same size)
- `all-mpnet-base-v2`: ~3× slower encoding (110M vs 22M params), +30-60ms per query

**Engineering complexity:** High (infrastructure) but low (code). Requires: (a) changing `SentenceTransformer("all-MiniLM-L6-v2")` to the new model, (b) a database migration to widen the vector column if switching from 384d to 768d, (c) **re-embedding all existing notes** — all embeddings must be regenerated with the new model.

**Risk:** High operationally. Re-indexing 1,055 notes is a one-time offline job, but in production, embedding model changes require careful coordination (old queries during the transition use mismatched embeddings). The new model's behavior may regress on specific query types that the old model happened to handle well.

**Should be A/B benchmarked?** Yes — this is a hard requirement before deployment, since re-indexing is irreversible without the old model.

**Estimated implementation time:** 6-10 days (including migration planning, execution, and full benchmark run).

---

### Improvement 6 — Title-Weighted Note Embeddings
**Priority: 6 — Easy win for title-query alignment**

**Description:** When computing note-level embeddings at index time, prepend the note title 2-3 times: `"{title}\n{title}\n{content}"`. This increases the title's weight in the final embedding vector, making note-level embeddings more responsive to title-matching queries.

**Why it should improve retrieval:**  
Many benchmark queries are effectively title lookups: "Kubernetes cluster setup" → note titled "Kubernetes Cluster Setup Guide". "OOP revision" → note titled "Object-Oriented Programming Revision Notes". The note embedding is currently computed over the full content, where the title's information is diluted. Prepending the title increases its cosine contribution. This is a well-documented technique (title weighting) used in production document retrieval at scale (documented in Amazon Kendra and Elasticsearch documentation).

**Expected metric improvement:**
- Hit Rate: +0.02 to +0.05
- MRR: +0.03 to +0.06 (primarily for easy "title matching" queries)

**Expected latency impact:** No query-time latency impact. Indexing takes slightly longer (longer text to encode).

**Engineering complexity:** Low. One-line change to `ChunkService.process_note()` in the note-level embedding section. Requires re-embedding all notes.

**Risk:** Low-medium. Title repetition may over-index on title words, causing vocabulary mismatch for notes whose content diverges from their title. Mitigated by 2× repetition (moderate weight increase) rather than 10×.

**Should be A/B benchmarked?** Yes (alongside Improvement 4 — chunk-level ANN).

**Estimated implementation time:** 1 day (implementation) + re-indexing time.

---

### Improvement 7 — Chunk Size and Overlap Tuning: 500→800 chars, 50→200 chars
**Priority: 7 — Moderate impact, low risk**

**Description:** Increase chunk size from 500 to 800 characters and overlap from 50 to 200 characters. This increases semantic coherence per chunk (more context for the embedding model) and reduces boundary-spanning loss (more content is carried across chunk boundaries).

**Why it should improve retrieval:**  
The research consensus (Anthropic, OpenAI, LlamaIndex documentation) recommends 256-512 token (1,000-2,000 char) chunks for note-taking style documents. At 500 chars (~125 tokens), chunks often contain incomplete sentences. At 800 chars (~200 tokens), the model sees 1-2 full paragraphs of context, dramatically improving embedding quality. Overlap at 200 chars ensures that a sentence spanning a boundary appears in both adjacent chunks — neither chunk is information-incomplete.

**Expected metric improvement:**
- Recall@5: +0.02 to +0.05
- Hit Rate: +0.01 to +0.03 (for boundary-spanning queries)

**Expected latency impact:** Fewer chunks per note (800 chars vs 500 → ~40% fewer chunks). ANN search over a smaller chunk table is slightly faster.

**Engineering complexity:** Low. Two constant changes in `ChunkingService`. Requires re-chunking and re-embedding all notes.

**Risk:** Low. Larger chunks are more robust; the main risk is including less-relevant context for specific queries, but this is bounded by the chunk-level ANN deduplication (Improvement 4) which selects the best chunk.

**Should be A/B benchmarked?** Yes (best tested in conjunction with Improvement 4).

**Estimated implementation time:** 1 day (implementation) + re-indexing.

---

### Improvement 8 — Intent Arm Confidence-Based Weight Decay
**Priority: 8 — Fix the intent arm regression**

**Description:** Modify the fusion weight to be dynamic based on fast classifier confidence. When confidence < 0.65 (near the bottom of the classifier's range), set intent weight to 0.0 (pure semantic). When confidence = 0.72 (actor identified), use intent weight 0.25. This replaces the fixed 0.65/0.35 split.

**Why it should improve retrieval:**  
The intent arm is currently net-negative (HYBRID Hit Rate 0.740 < SEMANTIC 0.760). The core problem is that when the fast classifier is wrong (46% of the time), it promotes notes from the wrong category. When classifier confidence is low (0.5 — the "general" fallback), the intent arm has no signal and only adds noise. Dynamic weighting based on classifier confidence would preserve semantic quality when intent is uncertain and boost with intent evidence only when confident.

**Expected metric improvement:**
- Hit Rate: +0.02 to +0.04 (by eliminating intent arm regressions)
- MRR: +0.01 to +0.03

**Expected latency impact:** Zero — this is a score arithmetic change.

**Engineering complexity:** Low. Modify `retrieve_hybrid()` fusion section.

**Risk:** Low. Cannot regress below SEMANTIC baseline since at confidence ≤ 0.55, `confidence_factor = 0` and `boost = 0`. The existing confidence gate already provides this protection mathematically, but the fixed 0.35 weight still applies intent_score to the final score. This improvement makes the gate explicit.

**Should be A/B benchmarked?** Yes — specifically track HYBRID vs SEMANTIC gap.

**Estimated implementation time:** 1-2 days.

---

### Improvement 9 — Multi-Query Retrieval (Query Variation without LLM)
**Priority: 9 — Moderate impact, zero LLM cost**

**Description:** For each user query, generate 2-3 lightweight variations using template-based rules, embed each, run ANN for each, and merge results via RRF. Variations: (1) strip common filler words ("Show my", "Tell me about", "What are my"), (2) expand abbreviations/acronyms from a known map ("OOP" → "Object-Oriented Programming"), (3) add/remove question framing ("How does X work?" → "X explanation").

**Why it should improve retrieval:**  
A query like "OOP revision" and "Object-Oriented Programming revision" produce different embeddings but should retrieve the same notes. Multi-query retrieval creates an ensemble of query interpretations, each contributing recall. This is cheaper than HyDE (no LLM call) and addresses a different failure mode (lexical abbreviation mismatch vs. vocabulary gap).

**Expected metric improvement:**
- Hit Rate: +0.02 to +0.05 (primarily for abbreviation/stopword queries)
- Recall@5: +0.02 to +0.04

**Expected latency impact:** 2-3× embedding calls (+15-70ms per additional query). Three embedding calls would add ~60ms.

**Engineering complexity:** Low-medium. Template rules are deterministic and require no model. Requires: (a) a query expansion module with the TECH_MAP and acronym tables already in `IntentExtractionService.TECH_MAP`, (b) multiple ANN calls (or batched), (c) RRF merging.

**Risk:** Low. Additive approach — worst case is no improvement (all variants produce identical ANN results).

**Should be A/B benchmarked?** Yes.

**Estimated implementation time:** 3-4 days.

---

### Improvement 10 — Recency Bias in Tie-Breaking
**Priority: 10 — Quality-of-life improvement for active users**

**Description:** Change tie-break from `note_id ASC` (older wins) to `note_id DESC` (newer wins) or add a recency decay factor: `adjusted_score = score × (1 + 0.05 × recency_factor)` where `recency_factor = 1 - days_since_creation/365`.

**Why it should improve retrieval:**  
Personal note-takers are more likely to care about recently created notes. If two notes are equally relevant (same semantic score), the user probably wants the more recent one. The current tie-breaking is counter-intuitive. This does not improve recall but improves the rank position of recent relevant results, which improves MRR.

**Expected metric improvement:**
- MRR: +0.01 to +0.03
- Hit Rate: No change (same notes in top-K)

**Expected latency impact:** Zero — tie-break is in Python sort.

**Engineering complexity:** Trivially low.

**Risk:** Low. May reduce MRR for some queries where older notes are more foundational/authoritative. Configurable via a flag.

**Should be A/B benchmarked?** No — effect size too small to be statistically significant on 50-query benchmark. Monitor in production via user engagement signals.

**Estimated implementation time:** 30 minutes.

---

## PART 4 — RANKED IMPROVEMENTS (BY ROI)

| Rank | Improvement | Expected Benchmark Gain | Engineering Effort | Risk | Resume Impact |
|------|-------------|------------------------|-------------------|------|---------------|
| 1 | **BM25 Sparse Retrieval + RRF** | +0.10 Hit Rate, +0.06 Recall, +0.05 MRR | Medium (3-7 days) | Low | Very High — lexical-dense hybrid is the production RAG standard |
| 2 | **Context Window 3K→12K** | Answer quality only | Trivial (15 min) | None | Medium — shows understanding of LLM constraints |
| 3 | **HyDE Query Expansion** | +0.08 Hit Rate, +0.06 Recall | Medium (4-6 days) | Medium | Very High — state-of-the-art query expansion technique |
| 4 | **Chunk-Level ANN in Hybrid** | +0.06 Hit Rate, +0.07 Recall | Medium (3-4 days) | Low | High — architecturally correct RAG design |
| 5 | **Embedding Model Upgrade** | +0.09 Hit Rate, +0.08 MRR | High (6-10 days) | High (re-index) | Very High — shows model selection expertise |
| 6 | **Title-Weighted Embeddings** | +0.04 Hit Rate, +0.04 MRR | Low (1 day) | Low | Medium |
| 7 | **Chunk Size 500→800, Overlap 50→200** | +0.03 Recall | Low (1 day) | Low | Medium |
| 8 | **Intent Confidence-Based Weight Decay** | +0.03 Hit Rate | Low (1-2 days) | Low | High — shows data-driven fusion design |
| 9 | **Multi-Query Retrieval (Templates)** | +0.03 Hit Rate | Low-Medium (3-4 days) | Low | Medium |
| 10 | **Recency Bias Tie-Break** | +0.02 MRR | Trivial (30 min) | Low | Low |

---

## PART 5 — SPRINT 4 ROADMAP

Ordered by expected benchmark improvement on Benchmark v2.0.0. Each sprint is atomic (complete-able independently) and produces a measurable delta.

---

### Sprint 4A — Lexical Foundation (Weeks 1-2)
**Target: +0.10 Hit Rate, +0.06 Recall**

**Objective:** Add BM25 sparse retrieval as a parallel arm to the existing semantic arm and merge via Reciprocal Rank Fusion. This is the single highest-ROI change because it recovers complete misses that no amount of tuning to the existing pipeline can fix.

**Tasks:**
1. Implement PostgreSQL full-text search via `tsvector` on the `notes` table. Add a `GIN` index on the `tsvector` column. Add an `update_note_tsvector()` trigger. (~1 day)
2. Implement `NoteRepository.search_bm25(query, user_id, limit)` using `plainto_tsquery()` with `ts_rank_cd` scoring. (~1 day)
3. Implement RRF merger: `rrf_score(r) = 1/(k + r)` for k=60, with configurable k. Merge semantic and BM25 ranked lists by RRF sum per note_id. (~1 day)
4. Integrate into `retrieve_hybrid()`: run BM25 in parallel with ANN, merge via RRF, preserve chunk selection logic. (~1 day)
5. Increase `_MAX_CONTEXT_CHARS` from 3,000 to 12,000. (15 minutes)
6. Run full Benchmark v2.0.0. Compute statistical significance vs baseline.

**Expected output:** +0.10 Hit Rate (0.76 → 0.86), +0.06 Recall (0.547 → 0.61), HYBRID now exceeds SEMANTIC on all metrics.

**Risk:** Low. Additive change. If BM25 finds nothing, RRF falls back to semantic.

---

### Sprint 4B — Embedding Architecture Overhaul (Weeks 3-4)
**Target: +0.06 Hit Rate, +0.07 Recall (cumulative)**

**Objective:** Fix the architectural mismatch where the hybrid semantic arm uses note-level averaged embeddings instead of chunk-level specific embeddings. Also upgrade chunking parameters for better semantic coherence.

**Tasks:**
1. Change `ChunkingService.CHUNK_SIZE = 800`, `ChunkingService.OVERLAP = 200`. (~30 min, code change)
2. Modify `ChunkService.process_note()` to prepend note title twice when computing **note-level** embeddings: `f"{title}\n{title}\n{content}"`. (~30 min)
3. Switch `retrieve_hybrid()`'s semantic arm from `search_similar_notes_with_distance()` to `search_similar_chunks_with_distance()`. Add note-level deduplication (keep highest-scoring chunk per note_id). Update `_best_chunk()` to return the already-selected chunk directly. (~2 days)
4. Re-chunk and re-embed all existing notes (one-time migration script). (~1 day)
5. Run Benchmark v2.0.0. Compare to Sprint 4A baseline.

**Expected output:** Cumulative +0.06 Hit Rate, +0.07 Recall beyond Sprint 4A. Particularly strong improvement on multi-topic notes and boundary-spanning queries.

**Risk:** Medium. Re-indexing is irreversible without rollback plan. Mitigation: keep old embeddings until benchmark confirms improvement.

---

### Sprint 4C — Query Expansion (Weeks 5-6)
**Target: +0.06 Hit Rate (cumulative)**

**Objective:** Close the remaining vocabulary gap between query phrasing and note content by generating an alternative query representation. Implement HyDE (lightweight version using Groq for speed) alongside multi-query template expansion.

**Tasks:**
1. Implement `QueryExpander` class with:
   - Template-based expansion (strip "show my/tell me/what are my", expand from `TECH_MAP` + acronym table)
   - Optional HyDE: Groq llama-3.1-8b, max_tokens=80, prompt: "Write a personal note that would answer this query: {query}". Parse the hypothetical note text.
2. Modify retrieval to embed 2-3 query variants. Run ANN for each variant (or batch). Merge per-note scores by max.
3. Add `QUERY_EXPANSION_ENABLED: bool = False` and `HYDE_ENABLED: bool = False` feature flags.
4. Benchmark HyDE alone, templates alone, and combined vs Sprint 4B baseline.

**Expected output:** Cumulative +0.06 Hit Rate. HyDE expected to recover queries like "Show my AI research reading goals" (complete misses due to vocabulary mismatch) that BM25+chunk-ANN still miss.

**Risk:** Medium. HyDE adds +200ms latency (mitigated by async). Template expansion is zero-risk (purely additive).

---

### Sprint 4D — Embedding Model Upgrade + Calibration (Weeks 7-8)
**Target: +0.08 Hit Rate, +0.07 MRR (cumulative)**

**Objective:** Replace `all-MiniLM-L6-v2` with `BAAI/bge-small-en-v1.5` (same size, 3× better MTEB retrieval score) and add instruction prefixes to query embeddings. Calibrate intent arm weights.

**Tasks:**
1. Benchmark `BAAI/bge-small-en-v1.5` and `all-mpnet-base-v2` offline against the benchmark corpus. Select based on Hit Rate and latency.
2. If vector dimension changes (384→768), add PostgreSQL migration for `embedding_vector` column width.
3. Update `embedding_model.py` to load the new model.
4. Add query instruction prefix: `encode("Represent this query for searching personal notes: " + query)`.
5. Re-embed all notes and chunks with the new model.
6. Implement confidence-based intent weight decay (Improvement 8): intent weight = 0.0 when classifier confidence ≤ 0.60, linear scale to 0.25 at confidence = 0.72.
7. Run full Benchmark v2.0.0. This is the final benchmark run of Sprint 4.

**Expected output (cumulative across all sprints):**

| Metric | v2.0.0 Baseline | Sprint 4D Target | Change |
|--------|-----------------|------------------|--------|
| Hit Rate | 0.760 | 0.88 | +0.12 |
| Recall@5 | 0.547 | 0.68 | +0.13 |
| MRR | 0.612 | 0.72 | +0.11 |
| Precision@5 | 0.244 | 0.30 | +0.06 |
| HYBRID vs SEMANTIC gap | −0.020 Hit Rate | HYBRID > SEMANTIC +0.04 | full reversal |

**Risk:** High operationally (model migration). Mitigation: deploy with feature flag, run shadow comparisons before cutover.

---

## CRITICAL OBSERVATIONS FOR IMPLEMENTATION

1. **Sprint 4A (BM25) can be implemented without disrupting any existing indexes or embeddings.** It should be prioritized first because it is additive, low-risk, and recovers the most benchmark misses.

2. **Sprints 4B-4D all require note re-indexing.** They should be batched together if possible to minimize the number of full corpus re-embedding operations.

3. **The cross-encoder reranker should NOT be revisited in Sprint 4** unless a domain-appropriate training set (personal note queries × personal note documents) becomes available. The MS MARCO model is definitively domain-mismatched for this corpus per empirical evidence.

4. **The intent arm needs a structural decision**: either fix the fast classifier (sprint investment ≥ 3-4 weeks for meaningful improvement) or reduce its weight to near-zero and treat it as an optional tiebreaker only. Sprint 4D's confidence-decay approach takes the latter position, which is the lower-risk path.

5. **Benchmark v2.0.0 has 50 queries in the eval set.** The confidence intervals on improvement estimates are wide (±0.02-0.06). Each sprint change should be evaluated against the full 205-query verified pool if statistical significance is needed for claims above +0.05 Hit Rate.
