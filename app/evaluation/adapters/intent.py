from __future__ import annotations


from app.evaluation.adapters.base import BaseRetrievalAdapter
from app.evaluation.constants import DEFAULT_INTENT_LIMIT
from app.evaluation.models import (
    BenchmarkQuery,
    RetrievalResult,
    RetrievalStrategy,
)

from app.services.intent_category_service import (
    IntentCategoryService,
)


class IntentAdapter(BaseRetrievalAdapter):

    strategy = RetrievalStrategy.INTENT

    def __init__(
        self,
        db,
        user_id: int,
        limit: int = DEFAULT_INTENT_LIMIT,
    ) -> None:

        super().__init__(db)

        self._service = IntentCategoryService(db)
        self._user_id = user_id
        self._limit = limit

    def _retrieve(
        self,
        benchmark_query: BenchmarkQuery,
    ) -> RetrievalResult:

        categories = self._service.find_categories_for_query(
            query=benchmark_query.query,
            user_id=self._user_id,
            limit=3,
        )

        predicted_category = (
            categories[0].name
            if categories
            else None
        )
        predicted_intent = self._service.extractor.extract_query_intent_fast(
            benchmark_query.query
        )["intent_type"]

        note_ids = []
        seen = set()

        for category in categories:

            notes = self._service.get_notes_for_category(
                intent_category_id=category.id,
                user_id=self._user_id,
            )

            for note in notes:

                if note.id not in seen:
                    seen.add(note.id)
                    note_ids.append(note.id)

                if len(note_ids) >= self._limit:
                    break

            if len(note_ids) >= self._limit:
                break

        return RetrievalResult(
            strategy=self.strategy,
            query=benchmark_query.query,
            retrieved_note_ids=note_ids,
            predicted_intent=predicted_intent,
            predicted_category=predicted_category,
        )
