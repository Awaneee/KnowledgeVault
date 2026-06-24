# KnowledgeVault

AI-powered knowledge management platform that combines semantic search,
intent-aware organization, vector embeddings, and retrieval-augmented
generation (RAG) to transform personal notes into a searchable
knowledge base.

## Key Features

- Semantic search powered by pgvector and Sentence Transformers
- Intent extraction and automatic categorization using local LLMs
- Retrieval-Augmented Generation (RAG) over personal knowledge
- Asynchronous note processing with Redis workers
- Dockerized deployment architecture
- Local-first AI inference through Ollama

## Architecture

User
 ↓
FastAPI API
 ↓
PostgreSQL

Redis Queue
 ↓
Background Worker
 ↓
Chunking → Embeddings → Intent Extraction → Categorization

Question
 ↓
Hybrid Retrieval
 ↓
Context Assembly
 ↓
Llama 3 Response

## Tech Stack

Backend:
- FastAPI
- SQLAlchemy
- Alembic

Data:
- PostgreSQL
- pgvector
- Redis

AI:
- Ollama
- Phi-3 Mini
- Llama 3
- Sentence Transformers

Infrastructure:
- Docker
- Docker Compose

## Current Capabilities

- User authentication
- Note ingestion and organization
- Background AI processing
- Semantic retrieval
- Intent-aware categorization
- Chunk-based RAG pipeline
- Streaming AI responses

## Roadmap

- Retrieval evaluation framework
- Category governance
- Observability and metrics
- Advanced citation support
- Horizontal worker scaling