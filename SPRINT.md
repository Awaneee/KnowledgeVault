# KnowledgeVault Backend — Production Hardening Sprint
**Date:** 2026-08-03  
**Freeze date:** 2026-08-07 (4 days)  
**Purpose:** Complete engineering map for production hardening. No new features. No new retrieval research.

---

## 1. Evaluation Framework

### Entry Points and CLI Commands

**Primary evaluation script:**
```
python scripts/evaluate.py \
    --user-id <int>         (required)
    --benchmark <path>      (default: app/evaluation/benchmark/benchmark.json)
    --output <dir>          (default: evaluation_results)
    --k <int>               (default: 5)
    --gates <path>          (default: evaluation_results/gates.json)
    --check-confounds       (flag: run scripts/check_benchmark_confounds.py after eval)
    --no-dashboard          (flag: skip dashboard.html generation)
```

**Direct module runner** (minimal, user-id=1, no CSV/dashboard):
```
python -m app.evaluation.runner
```

**Dashboard only:**
```
python scripts/generate_dashboard.py \
    --results-dir <dir>     (required; contains manifest.json + evaluation_results.csv)
    --history-dir <dir>     (optional; parent dir for trend data; defaults to results-dir parent)
    --output <path>         (optional; defaults to <results-dir>/dashboard.html)
```

### Adapter List

All adapters live in `app/evaluation/adapters/`. They are all instantiated unconditionally by `EvaluationRunner.__init__()` and run in sequence.

| Adapter | Class | File | Production Method Called |
|---|---|---|---|
| SemanticAdapter | `SemanticAdapter` | `adapters/semantic.py` | `EmbeddingService.search_notes()` |
| IntentAdapter | `IntentAdapter` | `adapters/intent.py` | `IntentCategoryService.find_categories_for_query()` |
| HybridAdapter | `HybridAdapter` | `adapters/hybrid.py` | `ChunkService.retrieve_hybrid()` |
| RerankAdapter | `RerankAdapter` | `adapters/rerank.py` | `ChunkService.retrieve_hybrid()` + `RerankingService.rerank()` |
| BM25Adapter | `BM25Adapter` | `adapters/bm25.py` | `BM25Repository.search()` directly |
| HybridBM25Adapter | `HybridBM25Adapter` | `adapters/bm25.py` | `ChunkService._retrieve_rrf_hybrid()` directly (bypasses BM25_ENABLED flag) |

BM25Adapter and HybridBM25Adapter deliberately bypass the `BM25_ENABLED` production flag so evaluation always exercises the BM25 code path regardless of flag state.

### BenchmarkLoader

**File:** `app/evaluation/benchmark/loader.py`

**Format:** JSON array of objects validated against `BenchmarkQuery` (Pydantic model in `app/evaluation/models.py`).

Required fields per entry:
- `id` (str): unique benchmark identifier
- `query` (str): natural-language query
- `expected_intent` (str): one of `communication | todo | study | reminder | idea | reference | question | event | general`
- `expected_category` (str): human-readable category name
- `relevant_note_ids` (list[int]): ordered list of note IDs constituting a correct answer
- `difficulty` (str): `easy | medium | hard`

Optional fields:
- `tags` (list[str]): free-form filtering tags
- `graded_relevance` (dict[str, int]): note_id → relevance grade for graded nDCG
- `retrieval_challenge` (str): free-text description of why the query is hard

**Manifest:** `manifest.json` in the same directory as `benchmark.json`. Contains `{"version": "..."}`. Missing manifest → version reported as "unknown".

**Validation:** Pydantic `model_validate()` on each entry. Invalid entries raise `ValidationError` and crash the run.

### Bootstrap CI Implementation

**File:** `app/evaluation/metrics/statistics.py`

**`bootstrap_mean_ci(scores, ci=0.95, n_boot=1000, seed=42)`**
- Resamples `scores` with replacement 1000 times, computes mean each time.
- Sorts bootstrap means; takes percentiles at `alpha/2` and `1 - alpha/2`.
- Returns `(lower, upper)` floats.
- Edge cases: n=0 → (0.0, 0.0); n=1 → (v, v).

**`bootstrap_delta_ci(scores_a, scores_b, ci=0.95, n_boot=1000, seed=42)`**
- Paired bootstrap: resamples (a, b) pairs together.
- Computes `mean(a) - mean(b)` for each resample.
- Returns `(lower, upper, significant)` where `significant = True` if CI excludes zero.
- Requires `len(scores_a) == len(scores_b)`; raises `ValueError` otherwise.

### Wilcoxon Significance Testing

**Function:** `wilcoxon_p_value(scores_a, scores_b)`

Uses `scipy.stats.wilcoxon` when scipy is installed (two-sided signed-rank test on paired differences). Falls back to a normal approximation of the sign test when scipy is unavailable. Returns `None` when all differences are zero.

**Helper:** `is_statistically_significant(scores_a, scores_b, alpha=0.05)` — returns bool.

### Gate Checking

**Gate file:** `evaluation_results/gates.json`

**Current gates (established from Benchmark v2.0.0, run `2c80e257`, 205 queries, k=5, 2026-07-31):**

| Strategy | mrr_floor | hit_rate_floor | ndcg_at_k_floor | avg_latency_ms_ceiling |
|---|---|---|---|---|
| SEMANTIC | 0.5625 | 0.7239 | 0.3697 | 100.0 ms |
| HYBRID | 0.5851 | 0.7239 | 0.3737 | 300.0 ms |
| RERANK | null | null | null | 500.0 ms |

INTENT, BM25, HYBRID_BM25 have no gate entries in the current file.

**Gate check logic** (in `scripts/evaluate.py → _emit_run_manifest()`):
- Reads `gates.json`, extracts per-strategy floors from `strategies.<KEY>.mrr_floor`, `hit_rate_floor`, `avg_latency_ms_ceiling`.
- For each strategy: `mrr_pass = (floor is None) or (actual >= floor)`. Same for hit_rate_pass and latency_pass.
- Results written to `manifest.json` → `gate_check` block.
- **No hard failure on gate miss** — the evaluate.py script does not exit non-zero if gates fail. Gate results are informational only (displayed in dashboard as PASS/FAIL badges).

**`check_gate()` utility** in `statistics.py` takes `(metric_value, floor, ceiling)` and returns `(passed, reason_string)`. Called nowhere in the automated pipeline — it is a utility for manual use only.

### Dashboard Generation

**Triggered automatically** at the end of `scripts/evaluate.py` (unless `--no-dashboard` is passed). Runs as a subprocess:
```
python scripts/generate_dashboard.py --results-dir <output_dir>
```

**Output:** `<results-dir>/dashboard.html` — self-contained static HTML with no external dependencies.

**Contents:** (1) Run header (run_id, date, commit, benchmark version, corpus coverage), (2) Strategy comparison table with CI columns, (3) MRR trend SVG chart across historical runs, (4) Regression gates table (PASS/FAIL badges), (5) Per-query heatmap (colour-coded by reciprocal rank), (6) Failure analysis (15 worst-performing queries).

**History data:** Loaded by scanning `<results-dir-parent>/*/manifest.json` glob. Each subdirectory with a manifest.json becomes a historical data point on the trend chart.

### Feature Flags Involved in Evaluation

| Flag | Default | Effect on Evaluation |
|---|---|---|
| `RERANKING_ENABLED` | False | RerankAdapter degrades gracefully to HYBRID ordering when False |
| `BM25_ENABLED` | False | BM25Adapter and HybridBM25Adapter bypass this flag entirely |
| `BM25_RRF_K` | 60 | Used directly by HybridBM25Adapter |
| `BM25_CANDIDATE_POOL` | 20 | Used directly by HybridBM25Adapter |
| `RERANK_CANDIDATE_POOL` | 20 | Used directly by RerankAdapter as pool size |
| `RERANK_TOP_K` | 8 | Used directly by RerankAdapter |

---

## 2. Retrieval Selection

### Call Graph: HTTP Request → Retrieval Result

**SEMANTIC path (POST /retrieve):**
```
route: retrieve.retrieve_chunks()
  → ChunkService.retrieve()
    → embedding_model.encode(query)                   [all-MiniLM-L6-v2 singleton]
    → ChunkEmbeddingRepository.search_similar_chunks_with_distance()  [pgvector ANN]
    → ChunkService._apply_score_filter()              [drops < RETRIEVAL_MIN_SCORE]
    → returns list[dict] with semantic_score, chunk_text, note_title
```

**HYBRID path (POST /retrieve/hybrid and POST /ask/, POST /ask/stream):**
```
route: retrieve.retrieve_hybrid_chunks() -OR- ask.ask_question()
  → ChunkService.retrieve_hybrid()
    → embedding_model.encode(query)                   [singleton]
    → EmbeddingRepository.search_similar_notes_with_distance()  [note-level pgvector ANN]
    → IntentCategoryService.find_category_matches_for_query()   [intent arm]
    → IntentExtractionService.extract_query_intent_fast()       [rule-based, no LLM]
    → ChunkRepository.get_chunks_by_note_ids()        [fetches chunks for candidates]
    → weighted score fusion: score = semantic_score + optional_intent_boost
      (boost = MAX_INTENT_BOOST * intent_score * confidence_factor, max 0.12)
    → deterministic sort: score desc, semantic_score desc, intent_score desc, note_id asc, chunk_index asc
    → returns top limit results (no score filter applied here — filtering done by AskService)
  [AskService only]:
  → RerankingService.rerank()                         [no-op if RERANKING_ENABLED=False]
  → AskService._filter_chunks()                       [drops < RETRIEVAL_MIN_SCORE]
  → LLMService.generate()                             [Gemini → Groq fallback]
```

**HYBRID_BM25 path (not exposed via HTTP — evaluation only):**
```
ChunkService.retrieve_bm25_hybrid()
  if BM25_ENABLED=False → delegates to retrieve_hybrid() transparently
  if BM25_ENABLED=True  → ChunkService._retrieve_rrf_hybrid()
    → EmbeddingRepository.search_similar_notes_with_distance()  [dense arm, pool candidates]
    → BM25Repository.search()                         [PostgreSQL tsvector/ts_rank_cd, pool candidates]
    → RRF fusion: rrf_score = Σ 1/(BM25_RRF_K + rank_i)
    → sort by rrf_score desc, return top limit
```

### Feature Flags: Retrieval

| Flag | Type | Default | Effect |
|---|---|---|---|
| `BM25_ENABLED` | bool | False | Enables RRF hybrid; when False, retrieve_bm25_hybrid() aliases retrieve_hybrid() |
| `BM25_RRF_K` | int | 60 | RRF rank smoothing constant |
| `BM25_CANDIDATE_POOL` | int | 20 | Candidates drawn per arm before RRF fusion |
| `RERANKING_ENABLED` | bool | False | Enables cross-encoder reranking; model is cross-encoder/ms-marco-MiniLM-L-6-v2 |
| `RERANK_MODEL` | str | cross-encoder/ms-marco-MiniLM-L-6-v2 | HuggingFace model ID for cross-encoder |
| `RERANK_CANDIDATE_POOL` | int | 20 | Stage-1 pool size when reranking is active (replaces default 8 in AskService) |
| `RERANK_TOP_K` | int | 8 | Candidates kept after reranking |
| `RERANK_CACHE_TTL_SECONDS` | int | 900 | TTL for reranker score cache in Redis |
| `RETRIEVAL_MIN_SCORE` | float | 0.10 | Score threshold for chunk filtering |
| `CATEGORY_INGEST_THRESHOLD` | float | 0.28 | Cosine distance for category reuse at ingest |
| `CATEGORY_QUERY_THRESHOLD` | float | 0.55 | Cosine distance for category matching at query time |

### Config Variables: Retrieval-related (from config.py)

All listed in the Feature Flags table above plus:
- `CATEGORY_ADAPTIVE_CAP_ENABLED` (bool, True): adaptive max categories
- `CATEGORY_NOTES_PER_CAP` (int, 10): 1 category per N notes
- `CATEGORY_ADAPTIVE_CAP_MIN` (int, 50): minimum categories
- `CATEGORY_ADAPTIVE_CAP_MAX` (int, 2000): maximum categories
- `CATEGORY_FUZZY_COMPAT_ENABLED` (bool, True): fuzzy category reuse
- `CATEGORY_REUSE_THRESHOLD_PRECISE` (float, 0.30)
- `CATEGORY_REUSE_THRESHOLD_BROAD` (float, 0.40)
- `CATEGORY_CONSERVATIVE_GENERAL_ENABLED` (bool, True)

### Every Call Site of Retrieval Methods

| Method | Called From | File |
|---|---|---|
| `ChunkService.retrieve()` | `retrieve.retrieve_chunks()` | `app/api/routes/retrieve.py:51` |
| `ChunkService.retrieve_hybrid()` | `retrieve.retrieve_hybrid_chunks()` | `app/api/routes/retrieve.py:84` |
| `ChunkService.retrieve_hybrid()` | `AskService.ask()` | `app/services/ask_service.py:97` |
| `ChunkService.retrieve_hybrid()` | `AskService.stream_ask()` | `app/services/ask_service.py:161` |
| `ChunkService.retrieve_hybrid()` | `AskService.ask_with_context()` | `app/services/ask_service.py:514` (eval only) |
| `ChunkService.retrieve_hybrid()` | `HybridAdapter._retrieve()` | `app/evaluation/adapters/hybrid.py:69` |
| `ChunkService.retrieve_hybrid()` | `RerankAdapter._retrieve()` | `app/evaluation/adapters/rerank.py:43` |
| `ChunkService.retrieve_bm25_hybrid()` | NOT called from any route | — |
| `ChunkService._retrieve_rrf_hybrid()` | `ChunkService.retrieve_bm25_hybrid()` | `app/services/chunk_service.py:313` |
| `ChunkService._retrieve_rrf_hybrid()` | `HybridBM25Adapter._retrieve()` | `app/evaluation/adapters/bm25.py:86` |
| `EmbeddingService.search_notes()` | `NoteService.search_notes()` | `app/services/note_service.py:100` |
| `EmbeddingService.search_notes()` | `SemanticAdapter._retrieve()` | `app/evaluation/adapters/semantic.py:39` |
| `BM25Repository.search()` | `ChunkService._retrieve_rrf_hybrid()` | `app/services/chunk_service.py:353` |
| `BM25Repository.search()` | `BM25Adapter._retrieve()` | `app/evaluation/adapters/bm25.py:43` |

### Mode Selection and Default Behaviour

**Mode selection is not explicit** — there is no `retrieval_mode` parameter. The mode is determined by which route/service method is called:
- `POST /retrieve` always calls `retrieve()` (pure semantic).
- `POST /retrieve/hybrid` always calls `retrieve_hybrid()`.
- `POST /ask/` and `POST /ask/stream` always call `retrieve_hybrid()` (never BM25 hybrid unless BM25_ENABLED=True, in which case retrieve_bm25_hybrid() would be the production choice — but AskService is hardcoded to call retrieve_hybrid()).
- `POST /notes/search` calls `EmbeddingService.search_notes()` (note-level semantic, no chunks).

**AskService default:** `retrieve_hybrid()` unconditionally, regardless of BM25_ENABLED. BM25 hybrid is only accessible via the evaluation adapters. This is intentional per the codebase — BM25 is gated and not yet wired into AskService.

---

## 3. Endpoint Inventory

All endpoints require Bearer JWT authentication unless noted. Pagination: NOT IMPLEMENTED on any endpoint. Format: `{"detail": "..."}` for all error responses (FastAPI default).

| Method | Path | Auth | Request Schema | Response Schema | Pagination | Streaming | Idempotency | File | Notes |
|---|---|---|---|---|---|---|---|---|---|
| POST | /auth/register | None | `UserRegister` (username, email, password) | `UserResponse` (id, username, email) | No | No | No (duplicates → 400) | auth.py | No password strength validation |
| POST | /auth/login | None | `UserLogin` (email, password) | `TokenResponse` (access_token, token_type) | No | No | Yes | auth.py | No rate limiting |
| GET | /auth/me | Bearer | — | `UserResponse` | No | No | Yes | auth.py | — |
| POST | /notes/ | Bearer | `NoteCreate` (content: str) | `NoteCreateResponse` | No | No | No | notes.py | Enqueues async processing; title = first 120 chars of content |
| POST | /notes/bulk | Bearer | `BulkNoteCreate` (notes: list[str]) | `list[NoteCreateResponse]` | No | No | No | notes.py | Silently skips failed notes; returns partial success |
| GET | /notes/ | Bearer | — | `list[NoteResponse]` | No | No | Yes | notes.py | No limit/offset; returns ALL user notes |
| GET | /notes/search | Bearer | `q: str` (query param) | `list[NoteSearchResponse]` | No | No | Yes | notes.py | Semantic search via EmbeddingService |
| GET | /notes/{note_id} | Bearer | — | `NoteResponse` | No | No | Yes | notes.py | 404 + 403 handled |
| GET | /notes/{note_id}/related | Bearer | — | `list[NoteSearchResponse]` | No | No | Yes | notes.py | Returns [] silently if note not owned |
| GET | /notes/{note_id}/attachments | Bearer | — | `list[AttachmentResponse]` (untyped) | No | No | Yes | notes.py | No response_model declared; returns raw ORM list |
| DELETE | — | — | — | — | — | — | — | — | **NOT IMPLEMENTED** — no note delete endpoint |
| PUT/PATCH | — | — | — | — | — | — | — | — | **NOT IMPLEMENTED** — no note update endpoint |
| POST | /categories/ | Bearer | `CategoryCreate` (name: str) | `CategoryResponse` | No | No | No | categories.py | — |
| GET | /categories/ | Bearer | — | `list[CategoryResponse]` | No | No | Yes | categories.py | — |
| GET | /categories/{category_id} | Bearer | — | `CategoryResponse` | No | No | Yes | categories.py | 404 + 403 handled |
| POST | /attachments/ | Bearer | `note_id: int` (query param) + multipart file | `AttachmentResponse` | No | No | No | attachment.py | No file type/extension validation; no size limit |
| GET | /attachments/ | Bearer | — | `list[AttachmentResponse]` | No | No | Yes | attachment.py | Returns all attachments for current user |
| GET | /attachments/{attachment_id} | Bearer | — | `AttachmentResponse` | No | No | Yes | attachment.py | 404 + 403 handled |
| POST | /uploads/file | Bearer | multipart file (.pdf, .txt, .docx only) | `PDFUploadResponse` (message, note_id) | No | No | No | upload.py | Extension validated; uuid4 filename; async processing via queue |
| GET | /topics/ | Bearer | — | Untyped (no response_model) | No | No | Yes | topics.py | No response_model declared |
| GET | /intents/categories | Bearer | — | `list[IntentCategoryResponse]` | No | No | Yes | intents.py | — |
| GET | /intents/categories/{intent_category_id}/notes | Bearer | — | `list[IntentNoteResponse]` | No | No | Yes | intents.py | No ownership check on intent_category_id |
| GET | /intents/notes/{note_id} | Bearer | — | `NoteIntentResponse` | No | No | Yes | intents.py | 404 if intent not found; ownership checked via user_id param |
| POST | /intents/backfill | Bearer | `limit: int = 100` (query param; clamped 1–500) | `IntentBackfillResponse` | No | No | No | intents.py | Triggers LLM intent extraction for up to 500 notes; can be slow |
| POST | /retrieve | Bearer | `RetrieveRequest` (query: str) | `list[ChunkResult]` | No | No | Yes | retrieve.py | Pure semantic; returns top 5 |
| POST | /retrieve/hybrid | Bearer | `RetrieveRequest` (query: str) | `list[ChunkResult]` | No | No | Yes | retrieve.py | Hybrid semantic+intent; returns top 5 |
| POST | /ask/ | Bearer | `AskRequest` (question: str) | `AskResponse` | No | No | No (cache-keyed) | ask.py | Hybrid retrieval + LLM; Redis-cached 3600s |
| POST | /ask/stream | Bearer | `AskRequest` (question: str) | `text/event-stream` token stream | No | Yes | No | ask.py | Not cached; sources not included in stream |

---

## 4. Authentication

### Login Flow (Step by Step)

1. Client sends `POST /auth/login` with JSON `{"email": "...", "password": "..."}`.
2. FastAPI validates body against `UserLogin` (Pydantic); invalid → 422.
3. `AuthService.login()` calls `UserRepository.get_by_email()` — SQLAlchemy query.
4. If user not found OR `verify_password(plain, hashed)` fails → `HTTPException(401, "Invalid email or password")`.
5. If valid: `create_access_token({"sub": str(user.id)})` — encodes HS256 JWT.
6. Returns `{"access_token": "<jwt>", "token_type": "bearer"}`.

### JWT Payload Fields

| Field | Value | Notes |
|---|---|---|
| `sub` | `str(user.id)` | String, not integer |
| `exp` | `datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)` | Expiry timestamp |

**Algorithm:** HS256 (from `settings.JWT_ALGORITHM`, default "HS256")  
**Secret source:** `settings.JWT_SECRET` — must be set in `.env`; no default  
**Token lifetime:** `settings.ACCESS_TOKEN_EXPIRE_MINUTES` = 30 minutes (default)

### Refresh Tokens

**NOT IMPLEMENTED.** There is no `POST /auth/refresh` endpoint and no refresh token issued at login. After 30 minutes the access token expires and the user must re-login.

### Logout

**NOT IMPLEMENTED.** There is no `POST /auth/logout` endpoint, no token blacklist, and no Redis-based token invalidation. JWT tokens remain valid until expiry.

### Password Hashing

**Library:** `passlib[bcrypt]` version 1.7.4 + `bcrypt` 4.1.3  
**Algorithm:** bcrypt via `passlib.context.CryptContext(schemes=["bcrypt"])`  
**Config:** `truncate_error=False` (prevents bcrypt's 72-byte password truncation from silently succeeding with truncated input — it errors instead)

**Password validation at registration:** NONE. No minimum length, no complexity requirements, no maximum length.

### Auth Middleware / Depends() Chain

```
get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()), db: Session = Depends(get_db))
  → decode_access_token(token)          [jose.jwt.decode with HS256]
  → if None: HTTPException(401, "Invalid or expired token", headers={"WWW-Authenticate": "Bearer"})
  → payload.get("sub")                  [string user ID]
  → UserRepository.get_by_id(int(user_id))
  → if None: HTTPException(401, "User not found")
  → return User ORM object
```

**File:** `app/api/dependencies/auth.py`

### 401 Response Format

```json
{"detail": "Invalid or expired token"}
```
with `WWW-Authenticate: Bearer` header on the first 401. Subsequent 401s (bad payload, user not found) use the same format without the header.

---

## 5. Error Handling

### Global Exception Handlers

**NONE.** `main.py` registers no `@app.exception_handler()` decorators. There is no global 500 handler, no global validation error override, and no request ID middleware.

FastAPI's built-in exception handlers apply:
- `RequestValidationError` → 422 with Pydantic error detail
- `HTTPException` → status code + `{"detail": "..."}` body
- Unhandled Python exceptions → 500 with generic body (no stack trace to client)

### HTTPException Patterns Across Routes

All error responses use `{"detail": "..."}` (FastAPI default).

| Route | Status | Detail | Notes |
|---|---|---|---|
| POST /auth/register | 400 | "Email already registered" | — |
| POST /auth/register | 400 | "Username already taken" | — |
| POST /auth/login | 401 | "Invalid email or password" | — |
| GET /notes/{note_id} | 404 | "Note not found" | — |
| GET /notes/{note_id} | 403 | "Access forbidden" | — |
| GET /notes/{note_id}/attachments | 404 | "Note not found" | — |
| GET /notes/{note_id}/attachments | 403 | "Access forbidden" | — |
| POST /attachments/ | 404 | "Note not found" | — |
| POST /attachments/ | 403 | "Access forbidden" | — |
| GET /attachments/{id} | 404 | "Attachment not found" | — |
| GET /attachments/{id} | 403 | "Access forbidden" | — |
| GET /categories/{id} | 404 | "Category not found" | — |
| GET /categories/{id} | 403 | "Access forbidden" | — |
| GET /intents/notes/{note_id} | 404 | "Intent not found for note" | — |
| POST /uploads/file | 400 | "Unsupported file type" | — |
| POST /uploads/file | 400 | "Could not read file..." | On extraction error |
| All protected routes | 401 | "Invalid or expired token" | Via get_current_user |

### Pydantic Validation Error Format (422)

```json
{
  "detail": [
    {
      "type": "...",
      "loc": ["body", "field_name"],
      "msg": "...",
      "input": "...",
      "url": "..."
    }
  ]
}
```

### Inconsistencies and Missing Error Handling

1. **`GET /notes/{note_id}/attachments`** — response_model is missing; returns raw ORM `note.attachments` list. No serialisation schema enforced.
2. **`GET /topics/`** — no `response_model` declared. Returns raw service output without schema enforcement.
3. **`GET /intents/categories/{intent_category_id}/notes`** — no ownership check on `intent_category_id`. Any authenticated user can enumerate notes in any intent category if they know the ID.
4. **`POST /ask/`** — never raises HTTP exceptions even on total failure. Always returns 200 with `{"retrieval_only": true, "status": "degraded"}` when LLM fails. The AskResponse schema includes `retrieval_only` and `status` fields specifically for this.
5. **`POST /notes/bulk`** — silently skips failed notes. Caller cannot distinguish partial success from full success without inspecting response length.
6. **`CacheService`** — no try/except around Redis calls. A Redis failure in `AskService.ask()` propagates as an unhandled exception, returning 500. Same risk in `EmbeddingService.search_notes()`.
7. **`EmbeddingService.search_notes()`** — uses `print("CACHE HIT")` / `print("CACHE MISS")` instead of logger. Not a correctness issue but a logging anti-pattern.
8. **`scripts/evaluate.py`** — prints `DATABASE URL: engine.url` to stdout unconditionally, including in any CI/CD pipeline run. This leaks the credentials in the connection string.

---

## 6. External Services

### Gemini API

- **Implementation:** `app/services/llm_providers.py` → `GeminiProvider`
- **HTTP client:** `requests` (synchronous)
- **Timeout:** `settings.LLM_TIMEOUT_SECONDS` = 60 seconds (configurable)
- **Retry policy:** Up to 5 retries for 429 rate limit responses, with exponential backoff starting at 2.0 s (doubles each retry). For non-429 `RequestException`: retry up to `max_retries` attempts with same backoff. For `Timeout`: raises immediately with no retry.
- **Exponential backoff:** Implemented for 429 (backoff starts at 2.0 s, doubles: 2→4→8→16→32). Also used for `RequestException` on the same schedule.
- **Circuit breaker:** NOT IMPLEMENTED
- **Rate limiting (client-side):** NOT IMPLEMENTED beyond the 429 retry
- **Graceful degradation:** On all retries exhausted → raises `LLMProviderError`. `LLMService` catches this and falls back to Groq. If Groq also fails → `AllProvidersExhausted`. `AskService` catches `AllProvidersExhausted` and returns a retrieval-only response (never 500).
- **Intent extraction:** Gemini-only; uses `responseMimeType: application/json` + `responseSchema` for schema-enforced JSON. Includes JSON repair + one retry before raising `AllProvidersExhausted`.
- **Streaming:** Separate `streamGenerateContent` endpoint; parses SSE JSON lines. No retry on stream failure.

### Groq API

- **Implementation:** `app/services/llm_providers.py` → `GroqProvider`
- **HTTP client:** `requests` (synchronous)
- **Timeout:** `settings.LLM_TIMEOUT_SECONDS` = 60 seconds
- **Retry policy:** NOT IMPLEMENTED — single attempt only
- **Exponential backoff:** NOT IMPLEMENTED
- **Circuit breaker:** NOT IMPLEMENTED
- **Rate limiting:** NOT IMPLEMENTED
- **Graceful degradation:** On any exception → raises `LLMProviderError`. `LLMService` moves to next provider. Used for answer generation only (never intent extraction).

### Sentence Transformers (Embedding Model)

- **Implementation:** `app/core/embedding_model.py` — module-level singleton
- **Model:** `all-MiniLM-L6-v2`
- **Loading:** Loaded once at import time. Pre-downloaded in Dockerfile Layer 3 via BuildKit cache.
- **Timeout:** NOT APPLICABLE (local inference; no network call)
- **Retry policy:** NOT APPLICABLE
- **Circuit breaker:** NOT APPLICABLE
- **Graceful degradation:** If `SentenceTransformer()` fails at startup → Python import error; container fails to start. No graceful degradation.
- **Reranking model:** `app/core/rerank_model.py` — conditional singleton. Only loaded when `RERANKING_ENABLED=True`. Load failure → logs error, sets `rerank_model = None`. All callers check for None and fall back to original ordering.

### Redis

- **Implementation:** `app/core/redis_client.py` → `redis.Redis.from_url()` singleton with `health_check_interval=30`
- **Connection pool:** Uses redis-py default pool (not configured explicitly)
- **Timeout:** NOT CONFIGURED — uses redis-py defaults (socket connect/read timeout = None = blocking)
- **Retry policy:** NOT IMPLEMENTED
- **Circuit breaker:** NOT IMPLEMENTED
- **Graceful degradation:**
  - `CacheService` has NO try/except. Redis errors propagate up.
  - `AskService.ask()` calls `CacheService.get()` without try/except → Redis failure causes 500.
  - `QueueService.enqueue_note_processing()` (called on note create) has no try/except → Redis failure on note creation causes 500.
  - `EmbeddingService.search_notes()` calls `CacheService.get/set()` without try/except → Redis failure causes 500 on `/notes/search`.
  - **Only `BM25Repository.search()`** wraps its DB call in try/except (returns [] on error). Redis has no equivalent.

### PostgreSQL / pgvector

- **Implementation:** `app/database/session.py` via SQLAlchemy engine
- **Pool config:** pool_size=10, max_overflow=20, pool_timeout=30s, pool_recycle=1800s, echo=False
- **Timeout:** pool_timeout=30s (wait for connection). No statement timeout configured.
- **Retry policy:** NOT IMPLEMENTED
- **Circuit breaker:** NOT IMPLEMENTED
- **Graceful degradation:** Unhandled SQLAlchemy exceptions propagate as 500. `BM25Repository.search()` is the only exception: wraps in try/except and returns [].
- **pgvector:** Used for ANN search via `<=>` operator (cosine distance). Requires `pgvector/pgvector:pg16` Docker image (docker-compose.yml).
- **Migrations:** Run via `alembic upgrade head` in the `migrate` service before API starts. API depends on `migrate: service_completed_successfully`.
- **Startup migration check:** NOT IMPLEMENTED in the API process itself. Relies solely on the compose `migrate` service.

### Ollama

- **Implementation:** `app/services/llm_providers.py` → `OllamaProvider`
- **Enabled by:** `settings.OLLAMA_ENABLED=True` (default False)
- **HTTP client:** `requests` (synchronous)
- **Timeout:** `settings.LLM_TIMEOUT_SECONDS` = 60 seconds
- **Retry policy:** NOT IMPLEMENTED
- **Graceful degradation:** Excluded from provider chain when `OLLAMA_ENABLED=False`. When enabled and fails → `LLMProviderError`, next provider tried.

---

## 7. Observability

### Logging

- **Library:** Python stdlib `logging` module. No structlog, no JSON formatter.
- **Format:** `"%(asctime)s [%(levelname)s] %(name)s — %(message)s"` (configured in `app/workers/note_worker.py` only via `logging.basicConfig`). The FastAPI/uvicorn API process has NO `logging.basicConfig` call. Log format in the API process is whatever uvicorn's default handler uses (plaintext to stdout).
- **Log levels:** The worker sets `level=logging.INFO`. The API process inherits uvicorn's default (INFO).
- **Logger instances** (`logging.getLogger(__name__)`) in:
  - `app/core/rerank_model.py`
  - `app/services/ask_service.py`
  - `app/services/chunk_service.py`
  - `app/services/intent_category_service.py`
  - `app/services/intent_extraction_service.py`
  - `app/services/llm_service.py`
  - `app/services/llm_providers.py`
  - `app/services/note_processing_service.py`
  - `app/services/note_service.py`
  - `app/services/reranking_service.py`
  - `app/repositories/bm25_repository.py`
  - `app/evaluation/ask/runner.py`
  - `app/evaluation/ask/judge.py`
- **Anti-pattern:** `app/services/embedding_service.py` uses `print()` instead of logging for cache hit/miss. This bypasses the logging framework entirely.
- **Secret in logs:** `scripts/evaluate.py` line 36 prints `DATABASE URL: engine.url` to stdout unconditionally, exposing credentials if they are embedded in the URL.

### Request IDs

**NOT IMPLEMENTED.** No middleware injects a request ID header or correlates log lines to individual requests. Log lines from concurrent requests are interleaved without correlation.

### Health Endpoints

**NOT IMPLEMENTED.** There is no `/health`, `/healthz`, `/readiness`, or `/liveness` endpoint in any route file. Docker Compose uses native `pg_isready` and `redis-cli ping` healthchecks for the data services, but the API container itself exposes no health endpoint.

### Metrics

**NOT IMPLEMENTED** in the production sense. `app/services/llm_metrics.py` provides in-process counters (`metrics.record_cache_hit()`, `metrics.record_cache_miss()`, `metrics.track()` context manager, `metrics.record_fallback()`) but these are in-memory only and not exposed via any endpoint or push mechanism. No Prometheus, StatsD, or OpenTelemetry integration.

### Tracing

**NOT IMPLEMENTED.** No distributed tracing (OpenTelemetry, Jaeger, Zipkin, etc.).

### Startup Logs

When the API container starts via `uvicorn main:app --host 0.0.0.0 --port 8000`:
- Uvicorn prints: `INFO:     Started server process`, `INFO:     Waiting for application startup.`, `INFO:     Application startup complete.`
- If `RERANKING_ENABLED=True`: rerank_model.py logs `INFO: Loading reranking model: ...` and `INFO: Reranking model loaded successfully` (or error).
- Embedding model (`all-MiniLM-L6-v2`) is loaded at first request, NOT at startup. No startup log for it.
- `main.py` has no startup event; `@app.on_event("startup")` is NOT implemented.

---

## 8. Deployment Readiness Audit

### CRITICAL

**C1: No health endpoint — zero Kubernetes/load-balancer readiness signal**
- Why: Without `/health`, no load balancer or orchestrator can detect that the API is up, the DB is reachable, or Redis is available. A failed DB connection would cause all requests to 500 silently while the container appears healthy.
- Affected: `main.py`, all routes
- Effort: 2 hours
- Risk if left: Container stays in rotation after DB/Redis failure; users get 500s with no visibility.

**C2: Redis failures cause 500 on core user paths**
- Why: `CacheService.get()` and `CacheService.set()` have no try/except. Redis failure on `POST /ask/` causes 500 instead of graceful degradation. Same for `POST /notes/` (via QueueService) and `GET /notes/search`.
- Affected: `app/services/cache_service.py`, `app/services/queue_service.py`
- Effort: 2 hours (add try/except with logging; cache get → return None on error; cache set → log and continue; queue enqueue → log and return partial response or 503)
- Risk if left: Any Redis blip takes down the entire ask pipeline.

**C3: No CORS configuration**
- Why: FastAPI defaults to blocking all cross-origin requests. There is no `CORSMiddleware` registered in `main.py`. If the frontend is on a different origin, all requests fail in browsers.
- Affected: `main.py`
- Effort: 1 hour
- Risk if left: Frontend completely unable to call the API from a browser (unless same-origin deployment).

**C4: JWT_SECRET has no minimum-length validation; `.env.example` uses `change-me-in-production`**
- Why: config.py declares `JWT_SECRET: str` with no validator. If deployed with the example value, all tokens are forgeable.
- Affected: `app/core/config.py`, `.env.example`
- Effort: 1 hour (add Pydantic validator requiring >= 32 chars; add startup assertion)
- Risk if left: Complete authentication bypass if the example secret is used in production.

**C5: Dockerfile runs as root**
- Why: No `USER` directive in the Dockerfile. The application runs as root inside the container. If there is any path traversal or code execution vulnerability, an attacker gets root in the container.
- Affected: `Dockerfile`
- Effort: 1 hour (add `RUN useradd -m appuser && chown -R appuser /app`, add `USER appuser`)
- Risk if left: Container escape risk; violates security best practices; will fail PCI/SOC2 audits.

**C6: No rate limiting on `/auth/login` or `/auth/register`**
- Why: Unlimited brute-force attempts on login. No IP-based throttling, no account lockout.
- Affected: `app/api/routes/auth.py`
- Effort: 4 hours (add `slowapi` middleware with `@limiter.limit("10/minute")` on login)
- Risk if left: Credential stuffing and brute-force attacks succeed silently.

### HIGH

**H1: No refresh token — 30-minute session forces re-login**
- Why: Access tokens expire in 30 minutes (default). No refresh token issued. Mobile/SPA users must re-authenticate constantly.
- Affected: `app/api/routes/auth.py`, `app/services/auth_service.py`, `app/core/security.py`
- Effort: 1 day
- Risk if left: Poor UX; users log out constantly; can be worked around by increasing ACCESS_TOKEN_EXPIRE_MINUTES (security trade-off).

**H2: No note update or delete endpoints**
- Why: There are no `PUT /notes/{id}`, `PATCH /notes/{id}`, or `DELETE /notes/{id}` routes. Users cannot edit or remove notes. Ask cache is never invalidated on content change because content never changes through the API.
- Affected: `app/api/routes/notes.py`
- Effort: 1 day (CRUD endpoints + cache invalidation in AskService and EmbeddingService)
- Risk if left: Stale answers from Ask cache if notes were created incorrectly; users cannot correct their data.

**H3: Ask cache never invalidated**
- Why: `CacheService.set()` uses TTL (3600s default). There is no explicit cache invalidation on any event. If a user's notes change (currently impossible via API — see H2), the cache would serve stale answers.
- Affected: `app/services/ask_service.py`, `app/services/cache_service.py`
- Effort: 2 hours (implement `CacheService.delete_pattern(f"ask:{user_id}:*")` called on note modification/deletion — only relevant after H2 is implemented)
- Risk if left: Stale cached answers once note update/delete is added.

**H4: No input validation on question/query field length**
- Why: `AskRequest.question` and `RetrieveRequest.query` are `str` with no `min_length` or `max_length` constraint. Empty string or 100KB payload goes to the embedding model and LLM.
- Affected: `app/schemas/ask.py`, `app/api/routes/retrieve.py`
- Effort: 1 hour
- Risk if left: Malformed requests can cause silent failures or waste LLM tokens.

**H5: No password strength requirements**
- Why: `UserRegister.password` is `str` with no constraints. Single-character passwords are accepted.
- Affected: `app/schemas/auth.py`
- Effort: 30 minutes (add `Field(min_length=8)` or a validator)
- Risk if left: Weak passwords; trivially guessable credentials.

**H6: `GET /intents/categories/{intent_category_id}/notes` has no ownership check on intent_category_id**
- Why: Any authenticated user can enumerate notes in another user's intent category by guessing the integer ID. The ownership is checked at the note level implicitly by the service query, but category IDs are sequential and guessable.
- Affected: `app/api/routes/intents.py:40-53`
- Effort: 1 hour (add ownership check: verify `intent_category.user_id == current_user.id` before returning notes)
- Risk if left: Information disclosure — users can discover note content through category membership.

**H7: `/attachments/` upload has no file type or size validation**
- Why: `POST /attachments/` accepts any file type without extension or MIME type validation (unlike `/uploads/file` which validates extension). No maximum file size. An attacker can upload executables or very large files.
- Affected: `app/api/routes/attachment.py`
- Effort: 2 hours (add allowed_extensions set; add file size check with `file.file.seek(0, 2)`)
- Risk if left: Arbitrary file storage; potential server disk exhaustion; stored executable risk.

**H8: DATABASE_URL logged in plain text in evaluate.py**
- Why: `scripts/evaluate.py` line 36: `print("DATABASE URL:", engine.url)`. If credentials are in the URL (standard for PostgreSQL), they are logged to stdout in any CI pipeline.
- Affected: `scripts/evaluate.py:36`
- Effort: 15 minutes (replace with `print("DATABASE URL:", engine.url.render_as_string(hide_password=True))`)
- Risk if left: Database credentials leak in CI logs.

### MEDIUM

**M1: No logging configuration in the API process**
- Why: `main.py` has no `logging.basicConfig()` call. The API process relies on uvicorn's default handler. Log format is inconsistent with the worker. No log level is explicitly set.
- Affected: `main.py`
- Effort: 1 hour (add `logging.basicConfig(level=logging.INFO, format="...")` to main.py)
- Risk if left: Log output is inconsistent and unstructured; difficult to parse in production.

**M2: `GET /notes/` returns all notes with no pagination**
- Why: No `limit` / `offset` / cursor parameter. For a user with thousands of notes, this query fetches everything, causing high DB memory usage and slow responses.
- Affected: `app/api/routes/notes.py`, `app/repositories/note_repository.py`
- Effort: 3 hours (add `limit` and `offset` query params; update repository query)
- Risk if left: Performance degradation and potential OOM for power users.

**M3: `POST /intents/backfill` is an unbounded LLM operation**
- Why: Accepts `limit` up to 500 (clamped). Each note triggers a Gemini API call. 500 sequential LLM calls can take several minutes and exhaust quota.
- Affected: `app/api/routes/intents.py:81-94`
- Effort: 2 hours (add background task or queue this instead of running synchronously; or reduce hard cap to 50)
- Risk if left: Request timeout; Gemini quota exhaustion for large backfills.

**M4: No statement timeout on PostgreSQL**
- Why: The SQLAlchemy engine has no `connect_args={"options": "-c statement_timeout=30000"}`. A slow query (e.g., full table scan on large note corpus) blocks indefinitely.
- Affected: `app/database/session.py`
- Effort: 30 minutes
- Risk if left: One slow query can hold a DB connection from the pool indefinitely.

**M5: `EmbeddingService.search_notes()` uses bare `print()` for cache logging**
- Why: `print("CACHE HIT")` / `print("CACHE MISS")` go to stdout but bypass the logging framework. They cannot be filtered by log level and are indistinguishable from other print output.
- Affected: `app/services/embedding_service.py:47, 51`
- Effort: 15 minutes (replace with `logger.debug(...)`)
- Risk if left: Log noise; cannot be suppressed in production.

**M6: Redis client has no explicit socket timeout configured**
- Why: `redis.Redis.from_url()` with default `socket_timeout=None` and `socket_connect_timeout=None`. A network partition to Redis blocks the calling thread indefinitely.
- Affected: `app/core/redis_client.py`
- Effort: 30 minutes (add `socket_timeout=5, socket_connect_timeout=5` to from_url)
- Risk if left: Thread pool starvation under Redis network issues.

**M7: No `/auth/logout` endpoint or token blacklist**
- Why: Tokens cannot be invalidated before expiry. If a token is compromised, there is no way to revoke it for 30 minutes.
- Affected: `app/api/routes/auth.py`
- Effort: 4 hours (add Redis-based token blacklist with TTL matching token expiry; add `POST /auth/logout`)
- Risk if left: Compromised tokens remain valid until expiry.

### LOW

**L1: `GET /topics/` and `GET /notes/{note_id}/attachments` missing `response_model`**
- Why: Without `response_model`, FastAPI does not validate or filter the response. Internal fields could leak.
- Affected: `app/api/routes/topics.py`, `app/api/routes/notes.py:132`
- Effort: 1 hour (define and apply response schemas)
- Risk if left: Schema drift; potential internal field exposure.

**L2: No request ID / correlation ID in logs**
- Why: Concurrent requests produce interleaved log lines with no way to correlate them to a specific user request.
- Affected: `main.py`
- Effort: 3 hours (add middleware that generates UUID per request and sets it in logging context via `contextvars`)
- Risk if left: Debugging production issues is very difficult with high concurrency.

**L3: Embedding model loaded at first request, not at startup**
- Why: `embedding_model` is a module-level singleton but Python modules import lazily. The first request to any embedding endpoint triggers the SentenceTransformer load (~1–2 seconds), causing a spike in first-request latency.
- Affected: `app/core/embedding_model.py`, `main.py`
- Effort: 1 hour (add a startup event in main.py that calls `embedding_model.encode("")` to warm the model)
- Risk if left: First-request latency spike of 1–2 seconds visible to users.

**L4: No `.dockerignore` verified; `COPY . .` in Dockerfile may include evaluation results and dev artifacts**
- Why: `Dockerfile` Layer 4 does `COPY . .` which includes everything not in `.dockerignore`. If `.dockerignore` is missing or incomplete, large directories like `evaluation_results/` and dev scripts get copied into the image.
- Affected: `Dockerfile`
- Effort: 30 minutes (verify/create `.dockerignore` with `evaluation_results/`, `*.csv`, `*.md`, `.env`, `__pycache__/`)
- Risk if left: Bloated Docker image; potential dev data exposure in production image.

---

## 9. Hardening Sprint Plan

**Guiding principle:** CRITICAL items first, then HIGH by user-impact and security severity, then highest-ROI MEDIUM items. 4 days, 8-hour days. No research tasks.

---

### Day 1 — Security and Reliability Foundation (8 hours)

**Goal:** Eliminate all CRITICAL security and reliability gaps before any other work.

**Task 1.1 — C5: Add non-root user to Dockerfile** (1 hour)
- File: `Dockerfile`
- Add after pip install layer:
  ```
  RUN useradd -m -u 1001 appuser && chown -R appuser /app
  USER appuser
  ```
- Test: `docker build && docker run --rm <image> whoami` → should print `appuser`.

**Task 1.2 — C3: Add CORS middleware to main.py** (1 hour)
- File: `main.py`
- Add `CORSMiddleware` with environment-configurable origins. Add `CORS_ALLOWED_ORIGINS` to `config.py` (default `["*"]` for dev; require explicit list for prod).
- Add `CORS_ALLOWED_ORIGINS` to `.env.example`.

**Task 1.3 — C4: Validate JWT_SECRET length at startup** (30 minutes)
- File: `app/core/config.py`
- Add Pydantic `@field_validator('JWT_SECRET')` that raises `ValueError` if `len(v) < 32`.
- Update `.env.example` to show a properly generated secret (with generation command comment).

**Task 1.4 — C2: Wrap CacheService in try/except for graceful Redis degradation** (2 hours)
- File: `app/services/cache_service.py`
- `get()`: wrap in try/except; on exception log `WARNING` and return `None`.
- `set()`: wrap in try/except; on exception log `WARNING` and return without raising.
- File: `app/services/queue_service.py`
- `enqueue_note_processing()`: wrap in try/except; log `ERROR` on failure. Return flag so caller can warn user.
- Outcome: Redis failure degrades gracefully instead of causing 500.

**Task 1.5 — C1: Add `/health` endpoint** (1.5 hours)
- File: new `app/api/routes/health.py`; update `main.py`
- Endpoint: `GET /health` (no auth)
- Checks: DB query (`SELECT 1`), Redis ping. Returns `{"status": "ok", "db": "ok", "redis": "ok"}` (200) or `{"status": "degraded", "db": "error", "redis": "ok/error"}` (503).
- Register in `main.py`: `app.include_router(health.router)`.

**Task 1.6 — H8: Fix DATABASE_URL log leak in evaluate.py** (15 minutes)
- File: `scripts/evaluate.py:36`
- Change to: `print("DATABASE URL:", engine.url.render_as_string(hide_password=True))`

**Task 1.7 — H5: Add password minimum length validation** (30 minutes)
- File: `app/schemas/auth.py`
- Change `password: str` to `password: str = Field(..., min_length=8, max_length=128)`

**Buffer:** 1.25 hours

---

### Day 2 — Security Hardening and Route Fixes (8 hours)

**Goal:** Fix remaining HIGH-severity security and API correctness issues.

**Task 2.1 — C6: Add rate limiting to auth endpoints** (3 hours)
- Add `slowapi` to `requirements.txt`
- File: `main.py` — add `SlowAPIMiddleware` and `Limiter`
- File: `app/api/routes/auth.py` — add `@limiter.limit("10/minute")` to `/login`, `@limiter.limit("5/minute")` to `/register`
- Add 429 handler in `main.py`
- Test: confirm 429 after threshold exceeded.

**Task 2.2 — H6: Fix intent category ownership check** (1 hour)
- File: `app/api/routes/intents.py:40-53`
- In `list_notes_for_intent_category()`: fetch the `IntentCategory` first, verify `intent_category.user_id == current_user.id`, raise 403 if mismatch.
- Update `IntentCategoryService.get_notes_for_category()` to accept and enforce `user_id`.

**Task 2.3 — H7: Add file type validation and size limit to attachment upload** (2 hours)
- File: `app/api/routes/attachment.py`
- Add `ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".png", ".jpg", ".jpeg"}` (define allowed set)
- Check `ext.lower() in ALLOWED_EXTENSIONS`; raise 400 if not
- Add size check: read file, check `len(content) <= MAX_ATTACHMENT_BYTES` (e.g., 10 MB); raise 413 if too large
- Add `MAX_ATTACHMENT_BYTES` to `config.py`.

**Task 2.4 — H4: Add input length validation on question/query** (1 hour)
- File: `app/schemas/ask.py`
- `AskRequest.question`: `Field(..., min_length=1, max_length=2000)`
- File: `app/api/routes/retrieve.py` (local `RetrieveRequest`)
- `query`: `Field(..., min_length=1, max_length=2000)`
- File: `app/schemas/note.py`
- `NoteCreate.content`: `Field(..., min_length=1, max_length=50000)`

**Task 2.5 — L1: Add response_model to untyped routes** (1 hour)
- File: `app/api/routes/topics.py` — define `TopicResponse` schema (or use `dict`), add `response_model`
- File: `app/api/routes/notes.py:132` — define `AttachmentResponse` schema (already exists at `app/schemas/attachment.py`); add `response_model=list[AttachmentResponse]`

**Buffer:** 0 hours (tight day — adjust scope if needed)

---

### Day 3 — Observability, Logging, and Startup Hardening (8 hours)

**Goal:** Make the production system observable and eliminate silent failure modes.

**Task 3.1 — M1: Add logging configuration to the API process** (1.5 hours)
- File: `main.py`
- Add at the top (before `app = FastAPI(...)`):
  ```python
  import logging
  logging.basicConfig(
      level=logging.INFO,
      format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
      handlers=[logging.StreamHandler()]
  )
  ```
- Verify uvicorn does not double-configure by checking its default handler.

**Task 3.2 — L2: Add request ID middleware** (3 hours)
- File: new `app/middleware/request_id.py`
- Middleware that generates `uuid4()` per request, stores in `contextvars.ContextVar`, adds to response headers as `X-Request-ID`
- Add a logging filter that injects the request ID into every log record for that request
- Register in `main.py`

**Task 3.3 — M5: Replace print() with logger in EmbeddingService** (15 minutes)
- File: `app/services/embedding_service.py:47, 51`
- Add `logger = logging.getLogger(__name__)` at top
- Replace `print("CACHE HIT")` with `logger.debug("CACHE HIT semantic_search user_id=%s", ...)`
- Replace `print("CACHE MISS")` with `logger.debug("CACHE MISS semantic_search")`

**Task 3.4 — M6: Add socket timeout to Redis client** (30 minutes)
- File: `app/core/redis_client.py`
- Add `socket_timeout=5, socket_connect_timeout=5` to `redis.Redis.from_url()` call

**Task 3.5 — M4: Add PostgreSQL statement timeout** (30 minutes)
- File: `app/database/session.py`
- Add `connect_args={"options": "-c statement_timeout=30000"}` to `create_engine()`

**Task 3.6 — L3: Warm embedding model at startup** (1 hour)
- File: `main.py`
- Add a `@app.on_event("startup")` (or lifespan context manager) that calls:
  ```python
  from app.core.embedding_model import embedding_model
  _ = embedding_model.encode("")
  logging.getLogger(__name__).info("Embedding model warmed up")
  ```

**Task 3.7 — L4: Verify and update .dockerignore** (30 minutes)
- Check if `.dockerignore` exists at repo root; if not, create it
- Ensure it includes: `evaluation_results/`, `*.csv`, `.env`, `__pycache__/`, `*.pyc`, `scripts/data/`, `uploads/`, `.git/`

**Task 3.8 — M3: Limit /intents/backfill concurrency risk** (1 hour)
- File: `app/api/routes/intents.py:81-94`
- Reduce hard cap from 500 to 50 for synchronous path: `limit=min(max(limit, 1), 50)`
- Add a comment explaining why (synchronous LLM calls; each call takes ~1-2s; 50 = ~60-100s max)
- Future: move to background task (out of scope for this sprint given frozen codebase)

**Buffer:** 45 minutes

---

### Day 4 — Final Hardening, Testing, and Smoke Check (8 hours)

**Goal:** Note CRUD completeness, cache correctness, final checks, and deployment smoke test.

**Task 4.1 — H2 (partial): Add DELETE /notes/{note_id} endpoint** (3 hours)
- File: `app/api/routes/notes.py`
- Add `@router.delete("/{note_id}", status_code=204)`
- Verify ownership (404/403 as per existing pattern)
- Delete: note embeddings, chunks, chunk embeddings, intent, then note
- File: `app/services/note_service.py` — add `delete_note()` method
- File: `app/repositories/note_repository.py` — add `delete_note_by_id()`
- After deletion, invalidate cache: call `CacheService.delete_pattern(f"ask:{user_id}:*")` and `CacheService.delete_pattern(f"semantic_search:{user_id}:*")`
- NOTE: `CacheService.delete_pattern()` needs to be implemented (uses `redis_client.scan_iter()` + `delete()`)

**Task 4.2 — H3: Implement CacheService.delete_pattern()** (1 hour)
- File: `app/services/cache_service.py`
- Add:
  ```python
  @staticmethod
  def delete_pattern(pattern: str) -> int:
      """Delete all keys matching pattern. Returns count deleted."""
      try:
          keys = list(redis_client.scan_iter(pattern))
          if keys:
              return redis_client.delete(*keys)
          return 0
      except Exception:
          logger.warning("Cache delete_pattern failed: pattern=%s", pattern)
          return 0
  ```

**Task 4.3 — Regression gate enforcement in CI** (2 hours)
- File: `scripts/evaluate.py`
- After `_emit_run_manifest()`, read the written `manifest.json`, check `gate_check` for any `False` values
- If any gate fails, `sys.exit(1)` so CI pipelines can detect regressions
- Add `--strict-gates` flag to make this opt-in (do not break existing scripts immediately)

**Task 4.4 — Deployment smoke test** (2 hours)
- Build Docker image: `docker build -t knowledgevault-backend:hardened .`
- Spin up full stack: `docker compose up -d`
- Verify: `GET /health` returns 200, DB and Redis both "ok"
- Verify: `POST /auth/register`, `POST /auth/login`, `POST /notes/`, `POST /ask/` all work end-to-end
- Verify: rate limit on `POST /auth/login` triggers 429 after 10 requests
- Verify: `DELETE /notes/{id}` works and cache is cleared
- Verify: container runs as non-root: `docker exec kv_api whoami` → `appuser`
- Verify: embedding model warm-up log appears at container start

**Buffer:** 0 hours (scope is tight; Task 4.1 note update endpoint is deferred to post-freeze if needed)

---

## Summary of Remaining Gaps After Sprint (Not Addressable in 4 Days)

The following items are identified but explicitly deferred beyond the freeze:
- `PUT/PATCH /notes/{id}` (note edit) — no current route
- Refresh tokens — full auth flow change
- Redis-based token blacklist / logout
- Pagination on `GET /notes/`
- Distributed tracing / metrics export
- BM25 hybrid wired into AskService (currently evaluation-only)
