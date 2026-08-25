# syntax=docker/dockerfile:1.7
#
# Build notes
# -----------
# Three cached layers (in dependency order so code edits don't bust expensive layers):
#   1. System packages  — only rebuilds when the base image changes.
#   2. Python packages  — only rebuilds when requirements.txt changes.
#   3. HF model         — only rebuilds when deps or Dockerfile change.
#   4. Application code — rebuilds on every source change.
#
# CPU-only PyTorch
# ----------------
# The --extra-index-url below overrides PyPI for torch/torchvision so that
# pip resolves the CPU-only wheel from the PyTorch CDN instead of the full
# CUDA wheel (~2 GB). All other packages still resolve from PyPI.

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # HuggingFace cache under /home/appuser so the non-root user can write to it at runtime.
    HF_HOME=/home/appuser/.cache/huggingface \
    TRANSFORMERS_CACHE=/home/appuser/.cache/huggingface \
    SENTENCE_TRANSFORMERS_HOME=/home/appuser/.cache/huggingface/sentence-transformers

WORKDIR /app

# Layer 1 — System dependencies.
# Kept before any COPY so it is cached unless the base image or this list changes.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Layer 2 — Python dependencies.
# Only depends on requirements.txt so source edits do not invalidate it.
# BuildKit pip cache avoids re-downloading packages on incremental builds.
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install \
        --extra-index-url https://download.pytorch.org/whl/cpu \
        -r requirements.txt

# Layer 3 — Pre-download the embedding model.
# Uses the BuildKit cache at HF_HOME so the model is not re-fetched on
# every build — only when this layer's cache key changes (deps or Dockerfile).
RUN --mount=type=cache,target=/home/appuser/.cache/huggingface \
    mkdir -p /home/appuser/.cache/huggingface && \
    python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Layer 4 — Application code.
# In development this is overridden by a bind mount in docker-compose.
COPY . .

# Remove any __pycache__ directories copied from the host.
# Docker's .dockerignore __pycache__/ pattern does not reliably exclude nested
# caches on Windows hosts; stale .pyc files cause Alembic to load a corrupt
# revision map and fail with "Can't locate revision".
RUN find /app -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# C5: Run as non-root. Create the user, set ownership of the app tree and the
# HF model cache directory so the process can write downloads at runtime.
RUN useradd -m -u 1001 appuser \
    && mkdir -p /home/appuser/.cache/huggingface \
    && chown -R appuser /app /home/appuser

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
