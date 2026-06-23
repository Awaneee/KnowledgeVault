FROM python:3.11-slim

# System deps needed by psycopg2-binary and pymupdf
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first so this layer is cached
# unless requirements.txt actually changes
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the sentence-transformers model at build time so the
# first request doesn't trigger a runtime download inside the container
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy application code after deps so code changes don't bust the
# expensive pip install layer
COPY . .

EXPOSE 8000
