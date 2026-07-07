from sqlalchemy.orm import Session

from app.core.embedding_model import embedding_model
from app.repositories.chunk_repository import ChunkRepository
from app.repositories.chunk_embedding_repository import ChunkEmbeddingRepository
from app.services.intent_category_service import IntentCategoryService
from app.services.chunking_service import ChunkingService


class ChunkService:
    """
    Orchestrates the full chunk pipeline for a single note:

        text
            ↓
        chunks
            ↓
        store chunks
            ↓
        embeddings
            ↓
        store embeddings
    """

    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self, db: Session):
        self.db = db
        self.chunk_repo = ChunkRepository(db)
        self.embedding_repo = ChunkEmbeddingRepository(db)
        self.intent_category_service = IntentCategoryService(db)

    def process_note(
        self,
        note_id: int,
        text: str
    ) -> int:

        chunk_texts = ChunkingService.split(text)

        if not chunk_texts:
            return 0

        chunks = self.chunk_repo.create_chunks(
            note_id=note_id,
            texts=chunk_texts
        )

        vectors = embedding_model.encode(
            chunk_texts
        ).tolist()

        records = [
            {
                "chunk_id": chunk.id,
                "embedding_model": self.MODEL_NAME,
                "embedding_vector": vector
            }
            for chunk, vector in zip(chunks, vectors)
        ]

        self.embedding_repo.bulk_create_embeddings(records)

        return len(chunks)

    def retrieve(
        self,
        query: str,
        user_id: int,
        limit: int = 5
    ) -> list[dict]:
        """
        Pure semantic retrieval.
        """

        query_vector = embedding_model.encode(query).tolist()

        rows = self.embedding_repo.search_similar_chunks_with_distance(
            query_vector=query_vector,
            user_id=user_id,
            limit=limit
        )

        return [
            {
                "note_id": note.id,
                "note_title": note.title,
                "chunk_text": chunk.chunk_text,
                "chunk_index": chunk.chunk_index,
                "semantic_score": self._score_from_distance(distance)
            }
            for chunk, note, distance in rows
        ]

    def retrieve_hybrid(
        self,
        query: str,
        user_id: int,
        limit: int = 5
    ) -> list[dict]:
        """
        Hybrid retrieval with weighted score fusion.

        Semantic search supplies fine-grained chunk relevance. Intent/category
        matching supplies purpose-level evidence. The final rank combines both
        instead of prefixing intent chunks ahead of semantic hits.
        """

        query_vector = embedding_model.encode(query).tolist()
        semantic_rows = self.embedding_repo.search_similar_chunks_with_distance(
            query_vector=query_vector,
            user_id=user_id,
            limit=max(limit * 4, 20)
        )

        category_matches = (
            self.intent_category_service.find_category_matches_for_query(
                query=query,
                user_id=user_id,
                limit=5
            )
        )

        category_scores = {
            match.category.id: match.score
            for match in category_matches
        }

        fused: dict[tuple[int, int, str], dict] = {}

        for rank, (chunk, note, distance) in enumerate(semantic_rows, start=1):
            semantic_score = self._score_from_distance(distance)
            rank_bonus = 1.0 / (rank + 1)
            key = self._chunk_key(note.id, chunk.chunk_index, chunk.chunk_text)
            fused[key] = {
                "note_id": note.id,
                "note_title": note.title,
                "chunk_text": chunk.chunk_text,
                "chunk_index": chunk.chunk_index,
                "source": "semantic",
                "intent_category": None,
                "semantic_score": semantic_score,
                "intent_score": 0.0,
                "score": (semantic_score * 0.72) + (rank_bonus * 0.08)
            }

        for category_rank, match in enumerate(category_matches, start=1):
            category = match.category
            notes = self.intent_category_service.get_notes_for_category(
                intent_category_id=category.id,
                user_id=user_id
            )

            category_rank_bonus = 1.0 / (category_rank + 1)
            base_intent_score = (
                (category_scores.get(category.id, match.score) * 0.82)
                + (category_rank_bonus * 0.18)
            )

            for note_rank, note in enumerate(notes, start=1):
                note_rank_bonus = 1.0 / (note_rank + 1)
                intent_score = min(
                    1.0,
                    (base_intent_score * 0.88) + (note_rank_bonus * 0.12)
                )

                chunks = self.chunk_repo.get_chunks_by_note(
                    note_id=note.id
                )

                if not chunks:
                    continue

                for chunk in chunks:
                    key = self._chunk_key(
                        note.id,
                        chunk.chunk_index,
                        chunk.chunk_text
                    )

                    current = fused.get(key)
                    if current is None:
                        semantic_score = self._text_overlap_score(
                            query=query,
                            text=f"{note.title} {chunk.chunk_text}"
                        )
                        current = {
                            "note_id": note.id,
                            "note_title": note.title,
                            "chunk_text": chunk.chunk_text,
                            "chunk_index": chunk.chunk_index,
                            "source": "intent",
                            "intent_category": category.name,
                            "semantic_score": semantic_score,
                            "intent_score": intent_score,
                            "score": 0.0
                        }
                        fused[key] = current
                    else:
                        current["source"] = "hybrid"
                        current["intent_category"] = category.name
                        current["intent_score"] = max(
                            current["intent_score"],
                            intent_score
                        )

                    current["score"] = (
                        (current["semantic_score"] * 0.72)
                        + (current["intent_score"] * 0.28)
                    )

        ranked = sorted(
            fused.values(),
            key=lambda item: (
                item["score"],
                item["semantic_score"],
                item["intent_score"],
                -item["note_id"],
                -item["chunk_index"]
            ),
            reverse=True
        )

        return ranked[:limit]

    @staticmethod
    def _chunk_key(
        note_id: int,
        chunk_index: int,
        chunk_text: str
    ) -> tuple[int, int, str]:
        return (
            note_id,
            chunk_index,
            chunk_text
        )

    @staticmethod
    def _score_from_distance(distance: float) -> float:
        try:
            value = float(distance)
        except (TypeError, ValueError):
            return 0.0

        return max(0.0, min(1.0, 1.0 - value))

    @staticmethod
    def _text_overlap_score(
        query: str,
        text: str
    ) -> float:
        import re

        query_tokens = {
            token for token in re.findall(r"[a-z0-9]+", query.lower())
            if len(token) > 2
        }
        text_tokens = set(
            re.findall(r"[a-z0-9]+", text.lower())
        )

        if not query_tokens:
            return 0.0

        return len(query_tokens & text_tokens) / len(query_tokens)
