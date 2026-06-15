from collections import defaultdict
from collections import Counter

import re
import numpy as np

from sklearn.cluster import AgglomerativeClustering

from sqlalchemy.orm import Session

from app.repositories.topic_repository import TopicRepository


class TopicService:
    STOP_WORDS = {
        "the",
        "and",
        "for",
        "with",
        "using",
        "note",
        "test",
        "pdf",
        "txt",
        "docx",
        "pasted",
        "statement",
        "updated"
    }

    def __init__(self, db: Session):
        self.repo = TopicRepository(db)

    def _generate_topic_name(
        self,
        notes: list[dict]
    ) -> str:

        words = []

        for note in notes:
            title = note["title"]

            tokens = re.findall(
                r"\b[a-zA-Z]+\b",
                title.lower()
            )

            words.extend(
                token
                for token in tokens
                if token not in self.STOP_WORDS
            )

        if not words:
            return "General Knowledge"

        common_words = Counter(
            words
        ).most_common(2)

        return " ".join(
            word.title()
            for word, _ in common_words
        )

    def generate_topics(
        self,
        user_id: int
    ):
        notes = self.repo.get_notes_with_embeddings(
            user_id=user_id
        )

        if len(notes) < 2:
            return []

        vectors = np.array(
            [
                note.embedding.embedding_vector
                for note in notes
            ]
        )

        n_clusters = min(
            max(2, len(notes) // 5),
            10
        )

        clustering = AgglomerativeClustering(
            n_clusters=n_clusters
        )

        labels = clustering.fit_predict(
            vectors
        )

        topics = defaultdict(list)

        for note, label in zip(
            notes,
            labels
        ):
            topics[int(label)].append(
                {
                    "id": note.id,
                    "title": note.title
                }
            )

        result = []

        for cluster_id, cluster_notes in topics.items():

            topic_name = self._generate_topic_name(
                cluster_notes
            )

            result.append(
                {
                    "cluster_id": cluster_id,
                    "topic_name": topic_name,
                    "notes": cluster_notes
                }
            )

        return result