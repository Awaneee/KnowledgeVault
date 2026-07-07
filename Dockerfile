# syntax=docker/dockerfile:1.7

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    HF_HOME=/opt/huggingface \
    SENTENCE_TRANSFORMERS_HOME=/opt/huggingface/sentence-transformers

WORKDIR /app

# Runtime/system build dependencies. Keep this before application COPY so it is
# cached unless the base image or this package list changes.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Dependency installation is the expensive layer. It only depends on
# requirements.txt, so Python source edits do not invalidate it.
COPY requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# Pre-download the embedding model into a stable image path. This layer only
# reruns when dependencies, the model name, or the Dockerfile changes.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy application code last. In development this is overridden by a bind mount.
COPY . .

EXPOSE 8000
