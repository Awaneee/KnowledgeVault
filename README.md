# KnowledgeVault

**AI-powered personal knowledge base.** Capture notes and files, then ask questions across them in natural language — with cited answers, automatic organisation, and graceful degradation when LLM providers fail.

- **Live API** — https://knowledgevault-production-8903.up.railway.app
- **Mobile client** (Flutter) — https://github.com/Awaneee/knowledgevault-frontend
- **Stack** — FastAPI · PostgreSQL 16 + pgvector · Redis 7 · Docker · Railway

---

## Highlights

- **Retrieval evaluated on a 205-query manually graded benchmark.** Hybrid retrieval (semantic + intent-aware + BM25 via Reciprocal Rank Fusion) reached **0.603 MRR@5** and **74.6% Hit@5**, beating pure semantic search by **+0.023 MRR** (95% CI [0.010, 0.038]).
- **3-provider LLM fallback chain** — Gemini → OpenRouter → Groq → retrieval-only. The API **never returns HTTP 500 due to LLM failure**; the worst case degrades to raw retrieved notes with a `status: "degraded"` flag.
- **Intent-aware categorisation** via Gemini's schema-enforced JSON, with a rule-based extractor as fallback. User overrides of categories are logged to `classification_feedback` for future classifier tuning.
- **Async note-processing worker** on a Redis queue with in-flight recovery — jobs are never lost on crash. Runs in-process on Railway (single container), or as a separate service in Docker Compose.
- **884-test regression suite** across unit, integration, retrieval-quality, and end-to-end RAG scoring.
- **Production-hardened** — JWT auth, SMTP password reset via hashed 6-digit codes, per-endpoint rate limits, request-ID structured logging, non-root Docker, Alembic auto-migrations on deploy.

---

## Architecture

```
Client (Flutter mobile) ──► FastAPI (REST + SSE)
                              │
              ┌───────────────┼──────────────────────┐
              ▼               ▼                      ▼
      PostgreSQL + pgvector   Redis (cache + queue)  LLM providers
              ▲               │                      (Gemini / OpenRouter / Groq)
              │               ▼
              │        Note-processing worker
              │        ├─ chunking
              │        ├─ embedding (all-MiniLM-L6-v2)
              │        ├─ intent extraction (Gemini structured JSON → rules)
              │        └─ category assignment (semantic reuse + adaptive cap)
              │
              └─── /ask pipeline ───────────────────►
                   Hybrid retrieval (semantic + intent + BM25 RRF)
                   → dedup + token-budget context assembly
                   → LLM provider chain with automatic failover
                   → Cited answer  (or degraded retrieval-only response)
```

---

## Retrieval evaluation

Two automated evaluation harnesses under `app/evaluation/`:

**1. Retrieval quality** — measures precision, recall, MRR@k, nDCG, and category accuracy across semantic-only, intent-aware, hybrid, and cross-encoder reranking strategies on **205 manually graded queries**.

Headline result (hybrid retrieval — MiniLM embeddings + pgvector cosine + intent fusion + BM25 via RRF):

| Metric | Score |
|---|---|
| MRR@5 | **0.603** |
| Hit@5 | **74.6%** |
| Δ vs. semantic-only | **+0.023 MRR**, 95% CI [0.010, 0.038] |

**2. End-to-end RAG scoring** — uses Gemini 2.0 Flash as an LLM judge to score answers on correctness, groundedness, faithfulness, hallucination, completeness, and context utilisation. Also captures per-provider latency and estimated token cost.

**Negative results documented too.** Cross-encoder reranking (`ms-marco-MiniLM-L-6-v2`) was implemented and evaluated — it *hurt* MRR on this personal-note corpus (ΔMRR = −0.012, not significant). It's feature-flagged off by default; the evidence lives in `evaluation_results/sprint2b_fresh/`.

Run either pipeline:

```bash
python scripts/evaluate.py     --user-id 1 --output evaluation_results/
python scripts/evaluate_ask.py --user-id 1 --output evaluation_results/ --limit 5
```

---

## LLM provider fallback

```
Answer generation:
Gemini → OpenRouter → Groq (llama-3.3-70b) → retrieval-only

Intent extraction (note indexing):
Gemini (schema-enforced JSON) → JSON repair retry → rule-based extractor
```

Groq is intentionally excluded from intent extraction — schema-enforced structured JSON is a Gemini-specific capability. All providers sit behind one interface and are ordered via `LLM_PROVIDER_PRIORITY` (comma-separated, hot-swappable via env var).

**Graceful degradation.** When every provider fails, the API returns the top retrieved notes with a `status: "degraded"` flag rather than 500. Search stays fully functional even during a total LLM outage.

```json
{
  "answer": "AI responses temporarily unavailable. Here are the most relevant notes.",
  "status": "degraded",
  "chunks": [
    {"title": "...", "preview": "...", "score": 0.82, "category": "Study - PostgreSQL"}
  ]
}
```

---

## Tech stack

| Layer | Choice | Why |
|-------|--------|-----|
| API | FastAPI + Uvicorn | async, typed, first-class OpenAPI |
| ORM / migrations | SQLAlchemy 2.0 + Alembic | auto-run on deploy via `railway.toml` |
| Database | PostgreSQL 16 + **pgvector** | vector similarity in-DB, no extra service |
| Cache / queue | Redis 7 | ask-response cache + job queue with in-flight recovery |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) | 384-dim, CPU-friendly, baked into image |
| LLMs | Google Gemini · OpenRouter · Groq (Llama 3.3 70B) | 3-provider failover; Ollama optional for local |
| Auth | JWT (HS256) · bcrypt | 10 kB minimum secret enforced at startup |
| Email | SMTP (Gmail app password by default) | password-reset codes (6-digit, SHA-256 hashed, 30-min TTL) |
| Runtime | Docker + Docker Compose (5 services) | reproducible local dev; single container on Railway |
| CI / deploy | GitHub → Railway auto-deploy | Alembic runs on each deploy |

---

## Getting started

**Prerequisites** — Docker, Docker Compose, a free Gemini key (https://aistudio.google.com/app/apikey), a free Groq key (https://console.groq.com/keys).

```bash
git clone https://github.com/Awaneee/KnowledgeVault
cd KnowledgeVault
cp env.example .env
# edit .env: set GEMINI_API_KEY, GROQ_API_KEY, JWT_SECRET (64-hex), POSTGRES_PASSWORD

docker compose build
docker compose up -d

curl http://localhost:8000/health/    # {"status":"ok","db":"ok","redis":"ok"}
```

OpenAPI docs live at `http://localhost:8000/docs`. The build pre-downloads the embedding model into the image so first-request latency is low.

---

## Key configuration

| Variable | Default | Purpose |
|---|---|---|
| `LLM_PROVIDER_PRIORITY` | `gemini,openrouter,groq` | comma-separated provider order for answer generation |
| `GEMINI_API_KEY` / `OPENROUTER_API_KEY` / `GROQ_API_KEY` | — | at least one required |
| `RETRIEVAL_MIN_SCORE` | `0.10` | minimum hybrid score for chunks to enter the context |
| `RERANKING_ENABLED` | `false` | cross-encoder reranking (off — hurts on personal notes) |
| `BM25_ENABLED` | `false` | BM25 + semantic RRF hybrid (dataset-dependent) |
| `ASK_CACHE_TTL_SECONDS` | `3600` | Redis cache TTL for `/ask` responses |
| `SMTP_HOST` / `SMTP_USER` / `SMTP_PASSWORD` | — | password-reset email delivery |
| `JWT_SECRET` | — | ≥32 chars enforced by pydantic validator at startup |

Full list in `env.example`.

---

## Repository layout

```
app/
├─ api/routes/         FastAPI routers (auth, notes, ask, categories, ...)
├─ services/           Business logic — retrieval, LLM chain, note processing, queue
├─ models/             SQLAlchemy ORM
├─ repositories/       DB access layer
├─ workers/            Async note-processing worker (Redis consumer)
├─ evaluation/         Benchmark harness + gold datasets
└─ core/               Config, security, redis, rate limiter, logging
migrations/versions/   Alembic revisions
scripts/               evaluate.py, evaluate_ask.py, seed helpers
tests/                 884 tests — unit, integration, retrieval quality, RAG scoring
docs/                  ADRs, sprint notes, retrieval architecture
```

---

## Design decisions worth reading

- **ADR-003 / retrieval architecture** — why note-level embeddings became the production default and Phase B (chunk-level with rerank) was deferred (`docs/adr-003-*.md`).
- **BM25 + RRF investigation** — implemented, evaluated on 205-query benchmark, feature-flagged off; personal-note corpus too lexically sparse for BM25 to add signal (see `docs/`).
- **Adaptive category cap** — max categories per user scales with corpus size instead of a hard constant, preventing UI overload at 100K notes while allowing MVP users a small set.
- **In-process worker on free-tier deploy** — a startup hook spawns the note-processing worker as a daemon thread on Railway, so a single container runs both the API and the queue consumer. For higher throughput, split into two Compose services (already supported).

---

## License

MIT.
