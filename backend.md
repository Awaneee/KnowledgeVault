# KnowledgeVault Backend — Complete Technical Reference

> Everything you need to answer any interview question about this backend.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [Architecture Overview](#3-architecture-overview)
4. [Application Entry Point](#4-application-entry-point)
5. [Configuration System](#5-configuration-system)
6. [Database Models](#6-database-models)
7. [Authentication & Security](#7-authentication--security)
8. [Note Lifecycle — End to End](#8-note-lifecycle--end-to-end)
9. [Chunking Service](#9-chunking-service)
10. [Embedding Service](#10-embedding-service)
11. [Intent Extraction Service](#11-intent-extraction-service)
12. [Intent Category Service](#12-intent-category-service)
13. [Background Worker & Queue](#13-background-worker--queue)
14. [Retrieval Systems](#14-retrieval-systems)
15. [Reranking Service](#15-reranking-service)
16. [LLM Service & Providers](#16-llm-service--providers)
17. [Ask / RAG Pipeline](#17-ask--rag-pipeline)
18. [Caching (Redis)](#18-caching-redis)
19. [API Routes Reference](#19-api-routes-reference)
20. [Document Ingestion (PDF / DOCX / TXT)](#20-document-ingestion-pdf--docx--txt)
21. [Evaluation Framework](#21-evaluation-framework)
22. [AI & CS Concepts Explained](#22-ai--cs-concepts-explained)
23. [Key Design Decisions & Trade-offs](#23-key-design-decisions--trade-offs)

---

## 1. Project Overview

KnowledgeVault is an AI-powered personal knowledge management backend. Users save notes (text, PDF, DOCX). The backend processes them asynchronously — generating vector embeddings, chunking long notes, extracting intent (study / todo / reference / communication …), and assigning them to smart categories. Users can then ask natural-language questions and the system retrieves the most relevant note chunks, builds context, and sends it to an LLM to produce a sourced answer.

**Core capability loop:**
```
Create Note → Queue → Worker → [Embed + Chunk + Classify] → DB
                                                            ↓
                     Ask Question → Retrieve Chunks → LLM → Answer with citations
```

---

## 2. Tech Stack

| Layer | Technology | Why |
|---|---|---|
| API Framework | FastAPI | Async-ready, automatic OpenAPI, Pydantic validation |
| ORM | SQLAlchemy + Alembic | Type-safe queries, migration management |
| Database | PostgreSQL 16 + pgvector | Relational + vector similarity in one DB |
| Cache / Queue | Redis 7 | Low-latency cache + reliable FIFO job queue |
| Embeddings | `all-MiniLM-L6-v2` (Sentence Transformers) | 384-dim, runs on CPU, fast, high-quality English embeddings |
| Cross-encoder | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Query-document relevance re-scoring |
| Primary LLM | Google Gemini 2.0 Flash | Schema-enforced JSON for intent, fast answer generation |
| Secondary LLM | Groq — Llama 3.3 70B | Free-tier fallback for answer generation |
| Local LLM | Ollama (optional) | Dev-only fallback, no internet required |
| Rate Limiting | SlowAPI | Per-route request throttling |
| Password Hashing | bcrypt via passlib | Adaptive cost factor, proven standard |
| JWT | python-jose | HS256 tokens for stateless auth |
| PDF parsing | PyMuPDF | Fast, lightweight PDF text extraction |
| DOCX parsing | python-docx | Native DOCX paragraph/table extraction |
| Containerisation | Docker + Docker Compose | Reproducible multi-service deployment |

---

## 3. Architecture Overview

```
Client (HTTP)
      │
      ▼
FastAPI App (main.py)
  ├── CORS Middleware
  ├── Rate Limit Middleware (SlowAPI)
  ├── Request ID Middleware (trace every request)
  └── Routers: /auth /notes /ask /retrieve /categories /topics /intents /upload /attachments
                    │                    │
                    ▼                    ▼
              PostgreSQL            Redis
           (pgvector + FTS)     ┌──────────────────┐
                                │  Cache (JSON TTL) │
                                │  Job Queue (FIFO) │
                                └──────────────────┘
                                         │
                                         ▼
                                  Background Worker
                                  (note_worker.py)
                                         │
                              ┌──────────┴───────────┐
                              │  NoteProcessingService │
                              └──────────┬───────────┘
                      ┌─────────────────┼─────────────────┐
                      ▼                 ▼                  ▼
             EmbeddingService    ChunkService     IntentCategoryService
             (note-level vec)  (chunk+embed)    (LLM classify → category)

ASK QUERY FLOW:
  POST /ask/ → AskService.ask()
    → ChunkService.retrieve_hybrid()   (semantic + intent fusion)
    → RerankingService.rerank()        (optional cross-encoder)
    → AskService._filter_chunks()      (min score gate)
    → AskService._build_context_map()  (dedup + token budget)
    → LLMService.generate()            (Gemini → Groq → Ollama → retrieval-only)
    → AskService._parse_citations()    (validate [N] references)
    → Response with answer + citations
```

---

## 4. Application Entry Point

**File:** `main.py`

### What it does:
- Creates the FastAPI app with `title="KnowledgeVault"`.
- Attaches **three middleware layers** in order:
  1. `RequestIDMiddleware` — injects a `X-Request-ID` UUID into every request; attached to log records via `RequestIDFilter` so all log lines for a request share the same ID.
  2. `SlowAPIMiddleware` — enforces per-route rate limits declared with `@limiter.limit(...)`.
  3. `CORSMiddleware` — allows configurable origins. If `CORS_ALLOWED_ORIGINS=["*"]`, credentials are disabled (browser security: wildcard + credentials is forbidden).
- Registers all routers with their prefix paths.
- `@app.on_event("startup")` — calls `embedding_model.encode("")` to warm the Sentence Transformers model into memory before the first real request (avoids cold-start latency spike).

### Rate limiting:
- Implemented with **SlowAPI** (FastAPI port of Flask-Limiter).
- Uses the client's IP address as the key.
- `POST /auth/register` → 5 requests/minute.
- `POST /auth/login` → 10 requests/minute.
- Prevents brute-force and abuse.

---

## 5. Configuration System

**File:** `app/core/config.py`

Uses **Pydantic Settings** (`pydantic-settings`). Reads from environment variables and `.env` file.

### Key settings and what they control:

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | required | SQLAlchemy connection string |
| `JWT_SECRET` | required (≥32 chars) | HMAC key for JWT signing |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Token lifetime |
| `REDIS_URL` | `redis://redis:6379/0` | Redis connection |
| `LLM_PROVIDER_PRIORITY` | `gemini,groq` | Ordered fallback chain for answers |
| `GEMINI_API_KEY` | — | Google AI Studio key |
| `GROQ_API_KEY` | — | Groq Console key |
| `OLLAMA_ENABLED` | `false` | Include Ollama in chain |
| `RETRIEVAL_MIN_SCORE` | `0.10` | Minimum chunk score for Ask context |
| `CATEGORY_QUERY_THRESHOLD` | `0.55` | Cosine similarity cutoff for query-time category match |
| `RERANKING_ENABLED` | `false` | Toggle cross-encoder reranking |
| `BM25_ENABLED` | `false` | Toggle BM25 sparse retrieval arm |
| `ASK_CACHE_TTL_SECONDS` | `3600` | Redis TTL for cached Ask responses |

### Validation:
`JWT_SECRET` has a `@field_validator` that enforces minimum 32 characters — prevents accidentally using a weak secret.

---

## 6. Database Models

All models inherit from `Base` (SQLAlchemy declarative base).

### `User` (`users`)
- `id`, `email` (unique), `hashed_password`, `created_at`
- Relationships: `notes`, `categories`, `intent_categories`

### `Note` (`notes`)
- `id`, `title`, `content` (nullable), `source_type` (`manual_note` / `pdf` / `docx` / `txt`), `organization_status` (`pending` / `processing` / `organized` / `failed`), `auto_title_source`, `user_id`, `category_id`, `created_at`, `updated_at`
- Relationships: `user`, `category`, `attachments`, `embedding` (1:1), `chunks` (1:many), `intent` (1:1), `intent_assignments`

### `Embedding` (`embeddings`)
- `id`, `note_id` (FK → notes), `embedding_model`, `embedding_vector` (pgvector `Vector(384)`)
- Stores the **note-level** vector for semantic search.

### `DocumentChunk` (`document_chunks`)
- `id`, `note_id`, `chunk_text`, `chunk_index`, `search_vector` (`tsvector` — maintained by DB trigger for BM25)
- Stores fixed-size text slices of a note.

### `ChunkEmbedding` (`chunk_embeddings`)
- `id`, `chunk_id` (FK → document_chunks), `embedding_model`, `embedding_vector` (Vector(384))
- Chunk-level vectors (used by chunk-level semantic retrieval paths in evaluation).

### `IntentCategory` (`intent_categories`)
- `id`, `user_id`, `name` (e.g. "Study - PostgreSQL"), `intent_type`, `actor`, `topic`, `embedding_vector`, `created_at`
- One row per discovered category per user.

### `NoteIntent` (`note_intents`)
- `id`, `note_id`, `intent_type`, `action`, `actor`, `topic`, `subtopic`, `object`, `due_date`, `temporal_text`, `urgency`, `confidence`, `model_name`, `prompt_version`, `raw_llm_json`, `extraction_quality_score`
- The full extracted intent for a note.

### `NoteIntentAssignment` (`note_intent_assignments`)
- `id`, `note_id`, `intent_category_id` — many-to-many join linking notes to intent categories.

### `Category` (`categories`)
- `id`, `name`, `user_id` — legacy user-defined categories (different from AI-assigned `IntentCategory`).

### `Attachment` (`attachments`)
- `id`, `note_id`, `filename`, `file_path`, `mime_type`, `file_size`, `created_at`

---

## 7. Authentication & Security

### Password storage (`app/core/security.py`)
- **bcrypt** via `passlib.CryptContext`.
- `hash_password(plain)` → bcrypt hash (cost factor auto-managed by passlib).
- `verify_password(plain, hashed)` → bool. Uses constant-time comparison to prevent timing attacks.

### JWT tokens
- `create_access_token(data, expires_delta)` — encodes `{"sub": user_id, "exp": ...}` with HS256 and `JWT_SECRET`.
- `decode_access_token(token)` — decodes + verifies signature and expiry. Returns `None` on any `JWTError`.

### Auth dependency (`app/api/dependencies/auth.py`)
- `get_current_user(credentials, db)` — FastAPI `Depends()`.
- Extracts `Bearer` token from `Authorization` header via `HTTPBearer`.
- Calls `decode_access_token`. Raises `401` if invalid or expired.
- Reads `sub` claim as user ID, queries DB. Raises `401` if user not found.
- Injected into every protected route.

### Auth routes (`POST /auth/register`, `POST /auth/login`, `GET /auth/me`)
- **Register:** creates user, hashes password, stores in DB.
- **Login:** verifies password with bcrypt, returns JWT.
- **Me:** returns current user via the `get_current_user` dependency.

---

## 8. Note Lifecycle — End to End

### Step 1: API receives note
`POST /notes/` → `NoteService.create_note(data, user_id)`
- Stores note in `notes` table with `organization_status="pending"`.
- Calls `QueueService.enqueue_note_processing(note_id, user_id)` — pushes a JSON job to Redis.
- Returns immediately with the note ID (non-blocking).

### Step 2: Worker picks up the job
`note_worker.py` → `QueueService.dequeue_note_processing(timeout=5)` → `NoteProcessingService.process_note(note_id, user_id)`

### Step 3: Pipeline execution (NoteProcessingService)
Sets `organization_status = "processing"`, then runs three sequential stages:

**Stage 1 — Note-level embedding**
- Concatenates `title + "\n" + content`.
- Calls `embedding_model.encode(text)` → 384-dim float vector.
- Stores in `Embedding` table (upsert: update if exists, insert if not).
- Used for: semantic note search, related notes, hybrid retrieval semantic arm.

**Stage 2 — Chunking + chunk embeddings**
- Calls `ChunkingService.split(text)` (see §9).
- Deletes existing chunks for this note (idempotency — safe to re-run).
- Bulk-inserts `DocumentChunk` rows.
- Batch-encodes all chunk texts in one `embedding_model.encode(chunk_texts)` call.
- Bulk-inserts `ChunkEmbedding` rows.

**Stage 3 — Intent extraction + category assignment**
- Calls `IntentCategoryService.process_note(note_id, user_id, title, content)`.
- Inside: calls `IntentExtractionService.extract(title, content)` → LLM → structured intent dict.
- Creates or reuses an `IntentCategory` for the user.
- Saves `NoteIntent` record with all extracted fields.
- Creates `NoteIntentAssignment` linking the note to its category.

Sets `organization_status = "organized"` on success. On any exception: rolls back DB, sets `organization_status = "failed"`.

---

## 9. Chunking Service

**File:** `app/services/chunking_service.py`

### Why chunking?
A full note can be thousands of characters. Embedding the whole note as one vector averages all the meaning together — specific details get diluted. Smaller chunks let the embedder capture focused semantics, and retrieval returns the exact relevant slice rather than the whole note.

### Algorithm: `ChunkingService.split(text)`

```
CHUNK_SIZE = 500 characters
OVERLAP    = 50 characters
```

1. **Sentence split** — `re.split(r'(?<=[.!?])\s+', text)` splits on sentence boundaries (keeps punctuation attached to preceding sentence).
2. **Greedy accumulation** — accumulates sentences into a `current` buffer until adding the next sentence would exceed 500 chars.
3. **Emit chunk** — when threshold crossed, join current buffer into a chunk string.
4. **Overlap carry** — take the last 50 characters of the emitted chunk and start the next buffer with them. This ensures a sentence that spans two chunks is partially represented in both → no cold context cuts.
5. **Hard split** — if a single sentence is itself > 500 chars (e.g. a URL or code block), slice it into 500-char pieces with overlap applied between pieces.

### Why overlap?
Without overlap, a concept expressed across the chunk boundary (e.g. "…the key insight is X. X works because…") would be split: chunk 1 ends with "…key insight is X." and chunk 2 starts fresh. Neither chunk gives enough context to answer "why does X work?". Overlap ensures both chunks contain some of that boundary content.

---

## 10. Embedding Service

**File:** `app/services/embedding_service.py`  
**Model:** `all-MiniLM-L6-v2` (Sentence Transformers)

### What is `all-MiniLM-L6-v2`?
- A distilled, fine-tuned BERT model for **sentence embeddings**.
- Produces **384-dimensional** dense float vectors.
- Trained on natural language inference + semantic textual similarity datasets.
- Designed so semantically similar sentences have high **cosine similarity** between their vectors.
- Runs on CPU in ~5ms per sentence.
- Loaded once at startup into `embedding_model` (module-level singleton).

### `generate_and_store(note_id, text)`
- Calls `embedding_model.encode(text).tolist()` — returns a Python list of 384 floats.
- Stores/updates in `Embedding` table (upsert pattern).

### `search_notes(query, user_id, limit)`
- Encodes the query string to a vector.
- Uses `EmbeddingRepository.search_similar_notes()` which issues:
  ```sql
  SELECT notes.* FROM notes
  JOIN embeddings ON embeddings.note_id = notes.id
  WHERE notes.user_id = :user_id
  ORDER BY embeddings.embedding_vector <=> :query_vector  -- cosine distance
  LIMIT :limit
  ```
- The `<=>` operator is provided by **pgvector** — does an exact cosine distance scan.
- Cache: Redis key `semantic_search:{user_id}:{query.lower()}` with default 3600s TTL.

### `get_related_notes(note_id, user_id, limit)`
- Fetches the note's stored embedding vector.
- Runs the same cosine distance query, excluding the source note.
- Returns notes closest in embedding space = semantically related.

---

## 11. Intent Extraction Service

**File:** `app/services/intent_extraction_service.py`

This service classifies *what a note is about* — its intent, actor, topic, urgency, etc.

### Intent types (9 classes)
`communication`, `todo`, `study`, `reminder`, `idea`, `reference`, `question`, `event`, `general`

### Three extraction paths

#### Path 1: Full LLM extraction (`extract(title, content)`)
Used when indexing a new note.
1. Build text: `f"{title}\n{content}"` (truncated to 4000 chars).
2. Build a structured prompt with 9 output fields and several few-shot examples.
3. Call `LLMService.extract_intent(prompt)` → Gemini with `responseSchema` enforcing JSON structure at the API level.
4. Parse the returned JSON.
5. Validate and sanitise every field through `_normalize()`.
6. If Gemini fails → try Ollama if enabled → fall back to rule-based.

#### Path 2: Rule-based fallback (`_extract_with_rules(text)`)
- Pattern matches against keyword sets: `COMMUNICATION_ACTIONS`, `TODO_ACTIONS`, reminder/event/question keywords.
- Regex for actor extraction (capitalised words after prepositions like "tell **Sid**").
- Tech map lookup for topic (e.g. "redis" → "Redis").
- Returns intent with `model_name="heuristic"`, confidence ~0.55–0.72.

#### Path 3: Fast keyword classifier (`extract_query_intent_fast(query)`)
- Zero LLM calls — runs in microseconds.
- Used at **query time** so retrieval never blocks on an LLM.
- Priority-ordered keyword group scan:
  ```
  communication > reminder > study > idea > event > reference > todo
  ```
  First matching group wins.
- If no group matches and question words present → `question`.
- Extracts pseudo-topic (meaningful content words after removing stopwords).
- Returns confidence 0.5–0.72.

### `_normalize(data, text)` — validation pipeline
Every LLM response field is sanitised before storage:

| Field | Validation |
|---|---|
| `intent_type` | Must be in 9 valid types; synonym map repairs typos ("task" → "todo") |
| `actor` | Must be a human name. Rejects: self-references, technology names, noise words, composite strings with "/" |
| `topic` | Rejects: stop words (the/a/an/…), weak verbs (added/create/…), question fragments (does/what/…), Python builtins (print/list/…), too-short non-acronyms |
| `urgency` | Fuzzy repair: "high urgency" → "high" |
| `confidence` | Clamped to [0.0, 1.0] |

**Tech-actor rescue:** if the LLM put a technology name in `actor` (e.g. `actor="redis"`) and `topic` is null, it moves the canonical form to `topic` instead.

### Extraction quality score
`compute_extraction_quality(intent)` returns a [0, 1] score:
- **Intent quality (35%):** penalises "general" intent, low confidence, heuristic model.
- **Topic quality (35%):** 1.0 if tech term, 0.85 if multi-word, 0.70 if long word, 0.0 if null.
- **Actor quality (15%):** 0.8 for null actor on non-communication notes (expected); 0.0 if tech term leaked through.
- **Consistency quality (15%):** penalty if confidence > 0.6 but all fields (topic, actor, object) are null.

### The LLM prompt (intent-v3)
Uses strict JSON format, current date injection, clear field definitions, and 9 worked examples covering different intent types. Temperature = 0 (deterministic).

---

## 12. Intent Category Service

**File:** `app/services/intent_category_service.py`

### Purpose
Take the extracted intent fields and map the note to a named category — creating a new category or reusing an existing one.

### Category naming rules (deterministic, no LLM)
```
communication + actor   → "Communication - {Actor}"
study + topic           → "Study - {Topic}"
reference + topic       → "Reference - {Topic}"
idea + topic            → "Ideas - {Topic[:2 words]}"
todo + object bucket    → "Shopping" | "Bills" | "Appointments" | "Errands" | "Tasks"
reminder                → "Reminders"
question + topic        → "Questions - {Topic}"
event + actor           → "Meetings - {Actor}"
general + topic         → "{Topic[:3 words]}"
general + no topic      → "General"
```
All names hard-capped to 4 words.

### Category reuse algorithm
Before creating a new category, the service searches for an existing one:

1. **Exact rule match** — look up `(intent_type, actor, topic)` in existing categories.
2. **Canonical name match** — does any existing category have the exact same generated name?
3. **Vector similarity search** — encode the proposed category name, find existing categories within cosine distance threshold:
   - Precise intents (study, reference, question): `CATEGORY_REUSE_THRESHOLD_PRECISE = 0.30`
   - Broad intents (idea, general, event): `CATEGORY_REUSE_THRESHOLD_BROAD = 0.40`
4. If none found → create new category, store its embedding vector.

### Adaptive category cap
`MAX_CATEGORIES_PER_USER` scales with corpus size: 1 category per 10 notes, floor 50, ceiling 2000. Prevents runaway category explosion for power users.

### Query-time category lookup (`find_category_matches_for_query`)
- Runs `extract_query_intent_fast()` on the query.
- Searches user's categories by cosine distance: cutoff `CATEGORY_QUERY_THRESHOLD = 0.55`.
- Returns `CategoryMatch(category, score, method, distance)` objects.
- Used by `ChunkService.retrieve_hybrid()` as the intent arm.

---

## 13. Background Worker & Queue

### Queue design (`app/services/queue_service.py`)

Uses two Redis lists for **reliable at-least-once processing:**

- `note_processing_queue` — the main FIFO queue.
- `note_processing_inflight` — tracks jobs currently being processed.

#### `enqueue_note_processing(note_id, user_id)`
- `LPUSH note_processing_queue '{"note_id": 1, "user_id": 5}'`
- Pushes to the left end.

#### `dequeue_note_processing(timeout=5)`
- `BRPOPLPUSH note_processing_queue note_processing_inflight timeout`
- **Atomic**: pops from the right of the main queue AND pushes to the inflight queue in one Redis operation.
- Blocking (up to `timeout` seconds) — worker sleeps efficiently, no busy-poll.
- Why atomic? If the worker crashes between pop and ack, the job is still in `inflight` and can be recovered.

#### `ack_job(note_id, user_id)`
- `LREM note_processing_inflight 1 job_json`
- Removes the job from inflight after successful processing.

#### `recover_inflight_jobs()`
- On worker startup: `RPOPLPUSH note_processing_inflight note_processing_queue` in a loop until empty.
- Moves any jobs left by a crashed worker back to the main queue.

### Worker loop (`app/workers/note_worker.py`)
```python
while True:
    job = QueueService.dequeue_note_processing(timeout=5)  # blocking pop
    note_id, user_id = job
    db = SessionLocal()
    service = NoteProcessingService(db)
    service.process_note(note_id, user_id)
    QueueService.ack_job(note_id, user_id)
    db.close()
```
- Runs in a separate Docker container from the API.
- Creates a fresh DB session per job (prevents connection leaks).
- On failure: logs the exception but does NOT ack — job stays in inflight for inspection.

---

## 14. Retrieval Systems

**File:** `app/services/chunk_service.py`

Three retrieval modes, all returning `list[dict]` with keys: `note_id`, `note_title`, `chunk_id`, `chunk_text`, `chunk_index`, `score`, `semantic_score`, `intent_score`, `source`, `intent_category`.

### Mode 1: Pure Semantic (`retrieve`)
1. Encode query → 384-dim vector.
2. `EmbeddingRepository.search_similar_notes_with_distance()` → pgvector cosine distance query.
3. `_distance_to_score(d) = max(0, 1 - d)` → converts distance [0,2] to score [0,1].
4. `_apply_score_filter()` → drop chunks below `RETRIEVAL_MIN_SCORE`.

### Mode 2: Hybrid Semantic + Intent (`retrieve_hybrid`) ⭐ Main production path

**Two arms run in parallel:**

**Semantic arm:**
- Fetches `pool_size = max(limit × 4, 20)` note candidates via cosine distance on note-level embeddings.
- More candidates than needed so intent arm has something to merge with.

**Intent arm:**
- `IntentCategoryService.find_category_matches_for_query(query, user_id)` → up to 5 matching categories.
- `get_notes_for_category()` → all notes in those categories.

**Fusion:**
```
final_score = semantic_score + intent_boost

intent_boost = effective_boost_cap × intent_score × confidence_factor

Where:
  effective_boost_cap = 0.12 (max boost a category match can add)
  confidence_factor   = (query_confidence - 0.55) / (1.0 - 0.55)  [0 if below threshold]
  intent_score        = category_match.score × confidence_factor
```

Only `canonical_name` and actor-specific `exact_rule` matches earn a boost. Other intent matches add the note as a candidate (recovery) but cannot boost score.

**Tie-breaking (deterministic):**
```python
key = (-score, -semantic_score, -intent_score, note_id, chunk_index)
```
Older notes (lower ID) and earlier chunks win ties.

**Best chunk selection** (`_best_chunk`):
For each note, picks the chunk with the highest text overlap with the query (Jaccard on >2-char tokens). Tie-broken by earlier chunk index.

### Mode 3: BM25 + RRF (`retrieve_bm25_hybrid`)
Only active when `BM25_ENABLED=True` (currently off — personal-note corpus too sparse).

**Algorithm:**
1. Run semantic arm → pool of notes with distances.
2. Run BM25 arm (`BM25Repository.search()`) → PostgreSQL full-text search via `tsvector` + `ts_rank_cd`, returning ranked chunks.
3. Deduplicate BM25 results to note level (best chunk per note).
4. **Reciprocal Rank Fusion (RRF):**
   ```
   rrf_score(note) = Σ  1 / (k + rank_i)
   
   k = 60 (BM25_RRF_K — Cormack et al. 2009 default)
   rank_i = 1-based position of note in each arm
   ```
   A note present in both arms gets contributions from both (higher combined score). A note absent from one arm gets 0 from that arm.
5. Sort by RRF score, return top K.

### BM25 via PostgreSQL
- `document_chunks.search_vector` is a `tsvector` column maintained by a DB trigger.
- `websearch_to_tsquery('english', query)` — parses natural language queries (quoted phrases, minus for NOT, AND by default). Falls back to `plainto_tsquery` if it produces NULL.
- `ts_rank_cd` (cover density) — ranks documents where query terms appear close together more highly than standard `ts_rank`. Better for short personal notes.
- `@@ ` operator — boolean match filter (only chunks that actually contain query terms).

---

## 15. Reranking Service

**File:** `app/services/reranking_service.py`  
**Model:** `cross-encoder/ms-marco-MiniLM-L-6-v2`

### What is a cross-encoder?
Unlike a bi-encoder (embedding model) which encodes query and document separately, a **cross-encoder** takes the (query, document) pair together and produces a single relevance score. It uses full cross-attention between query and document tokens, making it much more accurate but ~100× slower.

### How it's used here
1. Hybrid retrieval returns `pool = RERANK_CANDIDATE_POOL (20)` candidates.
2. For each candidate: `rerank_model.predict([(query, chunk_text), ...])` → list of relevance scores.
3. Sort candidates by reranker score descending.
4. Return top `RERANK_TOP_K (8)`.

### Graceful degradation
If `RERANKING_ENABLED=False`, model failed to load, or inference raises: returns original candidates unchanged, `reranked=False`. Never fails a request.

### Cache
Redis key: `rerank:{user_id}:{SHA-256(sorted_note_ids + query)}`.
TTL = `RERANK_CACHE_TTL_SECONDS (900s)`.
Cache key includes sorted note IDs so it's order-independent but invalidates naturally when notes change.

### Why it's disabled (ADR-003 addendum)
Cross-encoder trained on MS MARCO (web search queries) hurts on personal note corpus (short, informal, personal vocabulary). The expanded candidate pool alone (RERANK_CANDIDATE_POOL=20 vs 8) showed the real benefit. Re-enable only after finding a domain-appropriate model.

---

## 16. LLM Service & Providers

**File:** `app/services/llm_service.py`  
**File:** `app/services/llm_providers.py`

### Architecture: Two separate provider chains

**Intent extraction chain:** Gemini only (+ rule-based fallback if Gemini fails).
- Groq excluded: it doesn't support schema-enforced JSON output.
- Ollama: only if `OLLAMA_ENABLED=True`.

**Answer generation chain:** Reads `LLM_PROVIDER_PRIORITY` env var (default: `gemini,groq`).
- Instantiates providers in order; any with missing API keys are skipped.
- Tries each in order; on any failure, records the reason and falls back.

### Provider implementations

#### GeminiProvider
- REST API: `https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent`
- **Intent extraction:** uses `generationConfig.responseMimeType="application/json"` + `responseSchema` → Gemini guarantees JSON conforming to the schema. Temperature = 0.
- **Answer generation:** Temperature = 0.2 (slight variability allowed).
- **Streaming:** `streamGenerateContent` endpoint, `stream=True` on the `requests` call. Parses chunked JSON objects from the response stream, yields `candidates[0].content.parts[0].text` tokens.
- **Retry logic:** 5 retries with exponential backoff (starting 2s, doubling) on 429 rate limit.

#### GroqProvider
- OpenAI-compatible REST API: `https://api.groq.com/openai/v1/chat/completions`.
- Model: `llama-3.3-70b-versatile`.
- Standard chat completions format: `[{"role":"user","content":prompt}]`.
- Temperature = 0.2. Raises `LLMProviderError` on non-200 or missing content.

#### OllamaProvider
- Local REST API: `http://localhost:11434/api/generate`.
- Only active when `OLLAMA_ENABLED=True`.
- Dev-only; not for production.

### AllProvidersExhausted
Custom exception raised when every provider in the chain fails. `AskService` catches it and returns a retrieval-only degraded response (never a 500).

### JSON repair for intent extraction
LLM occasionally wraps JSON in markdown fences (` ```json ... ``` `). `_try_repair_json()`:
1. Strip fences.
2. Try `json.loads()`.
3. If fails: regex search for first `{...}` block, try parsing that.
4. Returns repaired string or `None`.

### Failure classification
`classify_llm_exception(exc)` maps exception messages to categories: `timeout`, `quota_exceeded`, `api_5xx`, `api_unavailable`, `malformed_response`, `unknown_error`. Used for metrics and fallback logging.

---

## 17. Ask / RAG Pipeline

**File:** `app/services/ask_service.py`

This is the core RAG (Retrieval-Augmented Generation) pipeline.

### `ask(question, user_id)` — blocking path

```
1. Check Redis cache (SHA-256 key includes user_id, normalised question, provider chain)
   ↓ hit: return cached response immediately
   ↓ miss: continue

2. retrieve_hybrid(question, user_id, limit=pool_limit)
   → returns list of chunk dicts with scores

3. RerankingService.rerank(question, chunks, top_k, user_id)
   → reorders by cross-encoder score (or no-op if disabled)

4. _filter_chunks(chunks)
   → drop chunks where score < RETRIEVAL_MIN_SCORE (0.10)

5. _build_context_map(chunks)
   → deduplication: fingerprint = first 80 chars of normalised chunk text
                    skip if fingerprint seen before (keeps highest-scored copy)
   → token budget: accumulate chunks until total chars > 3000
                   truncate last chunk if remaining space > 100 chars
   → assigns stable [N] reference numbers (1-based)
   → returns (context_string, context_map: list[ContextEntry])

6. _build_prompt(question, context)
   → structured prompt with <context> and <question> XML tags
   → instructions: 2-5 sentence answer, cite with [N], no hallucination

7. LLMService.generate(prompt)
   → Gemini → Groq → Ollama → AllProvidersExhausted

8. _validate_answer(answer)
   → rejects single-word / < 20-char responses (keyword leakage guard)

9. _parse_citations(answer, context_map)
   → regex scan for [N] references in answer
   → validates each N against valid_refs set
   → hallucinated refs (N outside range) removed + logged
   → returns (cleaned_answer, list[Citation])

10. Cache result if not retrieval_only and TTL > 0

Return: {question, answer, sources, citations, retrieval_only, status, provider, reranked}
```

### `stream_ask(question, user_id)` — streaming path
- Same retrieval + filtering + context building as blocking path.
- Calls `LLMService.generate_stream(prompt)` → yields tokens one by one.
- Uses FastAPI `StreamingResponse` with `media_type="text/event-stream"`.
- No caching (streams can't be cached).
- On `AllProvidersExhausted`: yields a plain degraded message string.

### Graceful degradation
When all LLM providers fail, `_retrieval_only_response()` returns:
```json
{
  "answer": "AI-generated responses are temporarily unavailable...",
  "retrieval_only": true,
  "status": "degraded",
  "chunks": [top 5 chunks with title, preview, score, category]
}
```
**The API never returns HTTP 500 due to LLM failure.**

### Context map & citations
`ContextEntry` dataclass:
```python
ref: int          # [1], [2], ... in prompt and answer
note_id: int
note_title: str
chunk_id: int
chunk_text: str   # full text in context
snippet: str      # first 200 chars for citation preview
intent_category: str | None
```

Context string format (what the LLM sees):
```
[1] Study - PostgreSQL | Note Title Here
Full chunk text...

[2] Reference - Docker | Another Note
Full chunk text...
```

### Cache key
```python
hashlib.sha256(f"{user_id}:{question.strip().lower()}:{LLM_PROVIDER_PRIORITY}".encode()).hexdigest()
```
Provider priority is included so changing providers busts the cache naturally.

### `ask_with_context()` — evaluation-only
Same pipeline but skips cache reads/writes and returns an `_eval` key with `retrieved_chunks`, `filtered_chunks`, `prompt`, `retrieval_ms`, `llm_ms`, `total_ms` for reproducible debugging.

---

## 18. Caching (Redis)

**File:** `app/services/cache_service.py`  
**Client:** `app/core/redis_client.py` (module-level `redis.Redis` singleton)

### `CacheService.get(key)`
- `redis_client.get(key)` → raw bytes or None.
- `json.loads(value)` → Python object.
- Returns `None` on any exception (cache failure is never fatal).

### `CacheService.set(key, value, expire_seconds=3600)`
- `redis_client.setex(key, expire_seconds, json.dumps(value))`
- Uses `setex` not `set` + `expire` — atomic TTL assignment.

### `CacheService.delete_pattern(pattern)`
- `redis_client.scan_iter(pattern)` → lazy iterator over matching keys.
- Used to invalidate caches when notes are deleted.

### What is cached and for how long?

| What | Key pattern | TTL |
|---|---|---|
| Ask responses | `ask:{user_id}:{SHA-256}` | `ASK_CACHE_TTL_SECONDS` (3600s) |
| Semantic search | `semantic_search:{user_id}:{query}` | 3600s |
| Reranker scores | `rerank:{user_id}:{SHA-256}` | `RERANK_CACHE_TTL_SECONDS` (900s) |

---

## 19. API Routes Reference

### Authentication
| Method | Path | Description |
|---|---|---|
| POST | `/auth/register` | Create account. Rate limited 5/min. |
| POST | `/auth/login` | Returns JWT access token. Rate limited 10/min. |
| GET | `/auth/me` | Returns current user (requires Bearer token). |

### Notes
| Method | Path | Description |
|---|---|---|
| POST | `/notes/` | Create note (queues background processing). |
| POST | `/notes/bulk` | Create multiple notes at once. |
| GET | `/notes/` | List all notes for current user. |
| GET | `/notes/search?q=...` | Semantic search across user's notes. |
| GET | `/notes/{id}` | Get a specific note (403 if not owner). |
| DELETE | `/notes/{id}` | Delete note (403 if not owner). |
| GET | `/notes/{id}/related` | Get semantically related notes. |
| GET | `/notes/{id}/attachments` | List attachments for a note. |

### Ask / RAG
| Method | Path | Description |
|---|---|---|
| POST | `/ask/` | Blocking RAG question answering. |
| POST | `/ask/stream` | Streaming token-by-token answer. |

### Retrieval
| Method | Path | Description |
|---|---|---|
| GET | `/retrieve/hybrid` | Hybrid retrieval without LLM synthesis. |

### Upload / Attachments
| Method | Path | Description |
|---|---|---|
| POST | `/upload/` | Upload PDF/DOCX/TXT → creates note. |
| POST | `/attachments/` | Attach file to existing note. |

### Categories, Topics, Intents
- CRUD routes for user-defined categories, topics, and viewing intent assignments.

### Health
- `GET /health` → `{"status": "ok"}` — used by Docker health checks.

---

## 20. Document Ingestion (PDF / DOCX / TXT)

**File:** `app/services/document_service.py`

`DocumentService.extract_text(file_path)` dispatches by file extension:

- `.pdf` → `PDFService.extract_text()` — PyMuPDF (`fitz`): opens each page, calls `page.get_text()`, concatenates with newlines.
- `.docx` → `DOCXService.extract_text()` — python-docx: iterates `doc.paragraphs`, joins non-empty paragraph texts.
- `.txt` → `TXTService.extract_text()` — reads raw UTF-8.

After extraction, the text is stored as the note's `content` and the file saved as an `Attachment`. The note then goes through the same background processing pipeline as a manually created note.

---

## 21. Evaluation Framework

**Location:** `app/evaluation/`

### Retrieval Evaluation
Evaluates retrieval quality against a 50-query benchmark.

**Adapters** (pluggable retrieval strategies tested):
- `SemanticAdapter` — pure vector search.
- `IntentAdapter` — intent-category only.
- `HybridAdapter` — semantic + intent fusion (production path).
- `HybridBM25Adapter` — semantic + BM25 RRF.
- `RerankAdapter` — hybrid + cross-encoder.
- `HybridNoIntentAdapter` — hybrid with `max_intent_boost=0` (ablation).

**Metrics computed** (`app/evaluation/metrics/`):
- **Precision@K** — fraction of top-K results that are relevant.
- **Recall@K** — fraction of all relevant results retrieved in top-K.
- **MRR (Mean Reciprocal Rank)** — 1/rank of first relevant result, averaged across queries. Better metric when only one result is expected.
- **nDCG (Normalized Discounted Cumulative Gain)** — rewards relevant results appearing higher in the list, penalises them when buried. `log2(rank + 1)` discount.
- **Category accuracy** — whether the retrieved notes match the expected category.
- **Latency** — p50, p95, p99 across queries.

**Benchmark v2.0.0:** 50 queries with known relevant note IDs and expected categories. Frozen — changes require semantic versioning.

### Ask / RAG Evaluation
Uses Gemini 2.0 Flash as an **LLM judge** to score generated answers on:
- **Correctness** — factual agreement with reference answer (0–1).
- **Groundedness** — fraction of claims supported by retrieved context.
- **Faithfulness** — absence of contradictions with context.
- **Hallucination** — absence of invented facts.
- **Completeness** — coverage of key information from context.
- **Context utilisation** — fraction of retrieved chunks referenced.

Debug artifacts saved per query: raw chunks, context prompt, answer, judge justification.

---

## 22. AI & CS Concepts Explained

### Embeddings / Vector Representations
A dense vector (list of floats) representing the semantic meaning of text. Texts with similar meaning have vectors that are geometrically close. `all-MiniLM-L6-v2` produces 384-dim vectors where "PostgreSQL indexing" and "database index performance" are close, while "grocery shopping" is far away.

### Cosine Similarity vs Cosine Distance
- **Cosine similarity** = dot(A, B) / (|A| × |B|) → ranges [–1, 1]. Two identical vectors = 1. Orthogonal = 0.
- **Cosine distance** = 1 – cosine_similarity → ranges [0, 2]. pgvector `<=>` operator returns this.
- Converted in code: `score = max(0, 1 - distance)`.

### pgvector
PostgreSQL extension adding a `vector(N)` column type and operators:
- `<=>` cosine distance, `<->` L2 distance, `<#>` inner product.
- Index types: IVFFlat (approximate, faster) or HNSW (better recall). This project uses exact scan (no index) — fine for personal note scale.

### RAG (Retrieval-Augmented Generation)
Pattern for grounding LLM answers in real documents rather than relying on parametric (training-time) knowledge:
1. Embed the query.
2. Retrieve the most relevant document chunks via vector similarity.
3. Insert retrieved text as context into the LLM prompt.
4. LLM generates an answer constrained to only the provided context.

Benefits: accurate, citable, up-to-date without fine-tuning, no hallucination of facts not in context.

### Chunking & Overlapping Windows
Long documents are split into fixed-size chunks to avoid diluting embeddings. Overlapping windows (overlap = 50 chars here) ensure content at chunk boundaries is represented in adjacent chunks, avoiding cold-cuts of context.

### Bi-encoder vs Cross-encoder
- **Bi-encoder** (embedding model): encodes query and document independently → fast, allows pre-computation and vector indexing. Trade-off: no cross-attention between query and document.
- **Cross-encoder**: takes (query, document) as a single input, models direct interactions. Produces a single relevance score. Much more accurate but O(n) inference per candidate — only practical as a reranker on a small candidate pool.

### BM25 (Best Match 25)
Classic TF-IDF-based sparse retrieval:
- TF (term frequency): how often the query term appears in the document.
- IDF (inverse document frequency): rarer terms get higher weight.
- BM25 adds document length normalisation.
PostgreSQL's `ts_rank_cd` is a BM25-like score (cover density variant).

### Reciprocal Rank Fusion (RRF)
A fusion algorithm for combining multiple ranked lists:
```
rrf_score(d) = Σ  1 / (k + rank(d, list_i))
```
- `k=60` (from Cormack et al. 2009) — smooths the fusion.
- Documents appearing in multiple lists get score from each.
- Documents absent from a list contribute 0 from that list.
- Advantage: no score calibration needed between lists (ranks are normalised).

### Intent Classification
NLP task of determining the purpose/goal behind a piece of text. Used here to assign notes to semantic categories ("Study - PostgreSQL", "Communication - Sid") enabling intent-aware retrieval.

### Schema-enforced JSON (Gemini `responseSchema`)
Gemini's `generationConfig.responseMimeType="application/json"` + `responseSchema` constrains the LLM output to a JSON object matching the schema. Eliminates the need to parse free-form text — the API rejects responses that don't conform. Only Gemini supports this; hence Groq is excluded from the intent chain.

### JWT (JSON Web Tokens)
Stateless authentication: server signs `{"sub": user_id, "exp": timestamp}` with HMAC-SHA256 using a secret key. Client sends token in `Authorization: Bearer <token>` header. Server verifies signature and expiry without hitting the database (no session storage).

### Rate Limiting
Prevents abuse by counting requests per time window per IP. SlowAPI uses a Redis backend for distributed counting. `5/minute` on register prevents account enumeration. `10/minute` on login prevents brute-force.

### Repository Pattern
Separates data access logic from business logic. Services call repository methods (`EmbeddingRepository.search_similar_notes_with_distance()`), not raw SQLAlchemy queries. Makes services testable with mock repositories and keeps SQL out of service layer.

### Service Layer
Business logic lives in `app/services/`. Routes (`app/api/routes/`) only handle HTTP parsing and response formatting. Services are testable independently of FastAPI.

### Dependency Injection (FastAPI `Depends`)
FastAPI resolves function parameters decorated with `Depends()` at request time. `get_db()` yields a DB session (closed after request); `get_current_user()` decodes JWT and returns the User object. Routes declare dependencies in their signature — zero boilerplate.

---

## 23. Key Design Decisions & Trade-offs

### Why note-level embeddings for hybrid retrieval instead of chunk-level?
Hybrid retrieval returns one result per note (for diversity). Using note-level embeddings is consistent — the semantic arm already operates at note level. Using chunk-level embeddings then deduplicating to note level caused the chunk with the best vector overlap to dominate, reducing diversity without improving recall. Note-level semantic + chunk-level intent fusion = cleaner boundary.

### Why is Groq excluded from intent extraction?
Intent extraction needs schema-enforced JSON output. Gemini's `responseSchema` API parameter guarantees the JSON structure at the model level. Groq (OpenAI-compatible API) doesn't support this. Instructing Groq to output JSON works inconsistently — the validation/repair overhead defeats the purpose.

### Why is BM25 disabled (BM25_ENABLED=False)?
Evaluation showed ΔMRR = −0.012 (not statistically significant) vs. the semantic-only baseline. Personal notes use idiosyncratic vocabulary, abbreviations, and informal language — the BM25 sparse signal is too noisy. The expanded candidate pool (RERANK_CANDIDATE_POOL=20) gives more recall benefit.

### Why is cross-encoder reranking disabled (RERANKING_ENABLED=False)?
The `ms-marco-MiniLM-L-6-v2` model was trained on MS MARCO web search queries. Personal note queries have different characteristics (shorter, more personal, domain-specific) — the model's relevance calibration doesn't transfer well. ΔNDCG was negative in evaluation. Keep infrastructure in place; re-enable after finding/fine-tuning a domain-matched model.

### Why Redis for both cache and queue?
Two birds, one stone — Redis handles both use cases well. The job queue uses Redis lists with `BRPOPLPUSH` for reliable at-least-once delivery. The cache uses `SETEX` for TTL-based expiry. Running separate services (RabbitMQ + Memcached) would add operational complexity with no benefit at this scale.

### Why adaptive category cap instead of hard limit?
A hard limit of 50 categories creates fragmentation for users with thousands of notes — many notes end up uncategorised or merged into wrong categories. Scaling with corpus size (1 category per 10 notes) keeps categories meaningful at every scale. Floor 50 ensures new users still get useful categorisation.

### Why SHA-256 for cache keys instead of using the raw query?
Raw query strings in Redis keys risk key collisions on special characters, excessively long keys, and encoding issues. SHA-256 produces a fixed 64-char hex string. The preimage includes `user_id:normalised_query:provider_sig` — collisions are cryptographically negligible.

### Graceful degradation (never return 500 from LLM failure)
LLM APIs are third-party and unreliable (quota, rate limits, outages). A 500 would break the entire app for a transient external failure. The design: LLM failures are caught at `AskService._synthesise()`, logged with full context, and a retrieval-only response is returned. Users still get relevant notes even when AI is unavailable.

### Why bcrypt with `truncate_error=False`?
bcrypt silently truncates passwords longer than 72 bytes. `truncate_error=False` makes passlib raise an exception instead of silently accepting a truncated password — prevents the security bug where two passwords that differ only after byte 72 would both authenticate.

### CORS credential safety
`allow_credentials=True` cannot be combined with `allow_origins=["*"]` — browsers reject the response. The code sets `allow_credentials` only when explicit origins are configured: `allow_credentials=settings.CORS_ALLOWED_ORIGINS != ["*"]`. This prevents a wildcard + credentials misconfiguration.

---

*Generated from source code analysis — every detail traces back to a specific file and method in the codebase.*
