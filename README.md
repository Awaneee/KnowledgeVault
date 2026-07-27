# KnowledgeVault

AI-powered knowledge management backend that combines semantic search,
intent-aware organisation, vector embeddings, and retrieval-augmented
generation (RAG) to transform personal notes into a searchable knowledge base.

## Architecture

```
User
 ↓
FastAPI (REST API)
 ↓                        ↓
PostgreSQL + pgvector    Redis (cache + job queue)
                          ↓
                   Background Worker
                          ↓
           Chunking → Embeddings → Intent Extraction → Categorisation

Question
 ↓
Hybrid Retrieval (semantic + intent/category fusion)
 ↓
Context Assembly (dedup + token budget)
 ↓
LLM Provider Chain (Gemini → Groq → Retrieval-only)
 ↓
Synthesised Answer
```

## LLM Provider Chain

### Answer Generation
```
Gemini (primary)
  ↓ quota/timeout/5xx
Groq (secondary — llama-3.3-70b-versatile)
  ↓ all fail
Ollama (optional — OLLAMA_ENABLED=true, local dev only)
  ↓ all fail
Retrieval-only response (never a 500)
```

### Intent Extraction (note indexing)
```
Gemini (schema-enforced JSON)
  ↓ JSON repair → retry once
Rule-based heuristic extractor
```

Groq is intentionally excluded from intent extraction because schema-enforced
structured JSON is required — a capability unique to Gemini's `responseSchema`.

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI |
| ORM | SQLAlchemy + Alembic |
| Database | PostgreSQL 16 + pgvector |
| Cache / Queue | Redis 7 |
| Embeddings | Sentence Transformers (`all-MiniLM-L6-v2`) |
| Primary LLM | Google Gemini 2.0 Flash |
| Secondary LLM | Groq (Llama 3.3 70B) |
| Local LLM | Ollama (optional, dev only) |
| Runtime | Docker + Docker Compose |

## Quick Start

### Prerequisites

- Docker + Docker Compose
- A Gemini API key (free at https://aistudio.google.com/app/apikey)
- A Groq API key (free at https://console.groq.com/keys)

### 1. Clone and configure

```bash
git clone <repo-url>
cd knowledgevault-backend
cp .env.example .env
```

Edit `.env` and set at minimum:
```
GEMINI_API_KEY=your-key
GROQ_API_KEY=your-key
JWT_SECRET=<random 64-char hex>
POSTGRES_PASSWORD=<strong password>
```

### 2. Build and start

```bash
docker compose build
docker compose up -d
```

The build process:
1. Installs Python dependencies (CPU-only PyTorch, ~500 MB).
2. Pre-downloads the embedding model (`all-MiniLM-L6-v2`).
3. Runs Alembic migrations.
4. Starts the API and background worker.

### 3. Verify

```bash
curl http://localhost:8000/health
```

## Provider Configuration

### Production (recommended)

```env
LLM_PROVIDER_PRIORITY=gemini,groq
GEMINI_API_KEY=...
GROQ_API_KEY=...
OLLAMA_ENABLED=false
```

### Local development with Ollama fallback

```env
LLM_PROVIDER_PRIORITY=gemini,groq,ollama
OLLAMA_ENABLED=true
OLLAMA_URL=http://host.docker.internal:11434/api/generate
```

### Groq-only (Gemini quota exhausted)

```env
LLM_PROVIDER_PRIORITY=groq
GROQ_API_KEY=...
```

### Retrieval-only (no LLM)

```env
LLM_PROVIDER_PRIORITY=
```

All `/ask` requests return retrieved notes without synthesis.

## Graceful Degradation

KnowledgeVault **never returns HTTP 500 due to LLM failure**.

When all configured providers fail, the API returns:

```json
{
  "answer": "AI-generated responses are temporarily unavailable. Here are the most relevant notes we found for your question.",
  "sources": ["Note title 1", "Note title 2"],
  "retrieval_only": true,
  "status": "degraded",
  "chunks": [
    {"title": "...", "preview": "...", "score": 0.82, "category": "Study - PostgreSQL"}
  ]
}
```

Search remains fully functional in degraded mode.

## Docker Tips

**Fast rebuilds** — Dependencies are cached in a separate layer from source code.
Only changing `requirements.txt` rebuilds the Python layer.

**No CUDA downloads** — The Dockerfile passes `--extra-index-url https://download.pytorch.org/whl/cpu`
so pip always selects the CPU-only PyTorch wheel (~500 MB vs ~2 GB for CUDA).

**HuggingFace model cache** — The embedding model is baked into the image layer and
cached via BuildKit. It is not re-downloaded unless dependencies change.

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `LLM_PROVIDER_PRIORITY` | `gemini,groq` | Comma-separated provider priority for answer generation |
| `GEMINI_API_KEY` | — | Google AI Studio API key |
| `GEMINI_ANSWER_MODEL` | `gemini-2.0-flash` | Gemini model for answers |
| `GROQ_API_KEY` | — | Groq Console API key |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Groq model for answers |
| `OLLAMA_ENABLED` | `false` | Include Ollama in fallback chain |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Ollama endpoint |
| `RETRIEVAL_MIN_SCORE` | `0.10` | Minimum chunk score for inclusion |
| `ASK_CACHE_TTL_SECONDS` | `3600` | Ask response cache TTL |
| `LLM_TIMEOUT_SECONDS` | `60` | Per-provider API timeout |
| `CATEGORY_QUERY_THRESHOLD` | `0.55` | Intent category similarity threshold |

## Capabilities

- User authentication (JWT)
- Note ingestion (text, PDF, DOCX)
- Background AI processing (async Redis worker)
- Semantic retrieval (pgvector cosine similarity)
- Intent-aware categorisation (Gemini → rule-based)
- Hybrid RAG pipeline (semantic + intent fusion)
- Streaming AI responses
- Multi-provider LLM with automatic failover
- Graceful degradation to retrieval-only mode
- Response caching (Redis, configurable TTL)
- LLM provider metrics (attempts, latency, fallbacks)

## Evaluation Framework

KnowledgeVault features two automated evaluation pipelines located under `app/evaluation/` to verify system quality:

### 1. Retrieval Evaluation

Evaluates retrieval quality (precision, recall, MRR, nDCG, category accuracy) across semantic, intent, and hybrid search.

- **Dataset:** `app/evaluation/benchmark/benchmark.json` (50 queries)
- **Execution:**
  ```bash
  python scripts/evaluate.py --user-id 1 --output evaluation_results/
  ```
- **Outputs:**
  - `evaluation_results/evaluation_report.md` (Markdown dashboard)
  - `evaluation_results/evaluation_results.csv` (Flat metrics)

### 2. End-to-End RAG (Ask Endpoint) Evaluation

Evaluates generated answer quality using Gemini 2.0 Flash as a judge. It measures:
- **Correctness:** Compare answer to reference answer on factual content (0.0-1.0).
- **Groundedness:** Fraction of answer claims supported by the retrieved context.
- **Faithfulness:** Absence of contradictions against the retrieved context.
- **Hallucination:** Measures absence of invented/hallucinated facts.
- **Completeness:** Coverage of key information from retrieved context.
- **Context Utilisation:** Fraction of retrieved chunks referenced in answer.
- **Timing & Latency:** Breakdowns of retrieval, LLM, and total milliseconds.
- **Cost:** Estimated token usage and API call costs.

- **Dataset:** `app/evaluation/ask_benchmark/gold_dataset.json` (50 representative questions across 10 categories).
- **Execution:**
  ```bash
  # Run full evaluation
  python scripts/evaluate_ask.py --user-id 1 --output evaluation_results/
  
  # Run a subset (e.g. limit to 5 queries to save API key quota)
  python scripts/evaluate_ask.py --user-id 1 --output evaluation_results/ --limit 5
  ```
- **Outputs:**
  - `evaluation_results/ask_evaluation_report.md` (Answers quality dashboard)
  - `evaluation_results/ask_evaluation_results.csv` (Full dataset results)
  - `evaluation_results/ask_debug/{query_id}_debug.json` (JSON debug artifacts containing raw chunks, context prompt, generated answer, and judge justification for deterministic post-hoc debugging).