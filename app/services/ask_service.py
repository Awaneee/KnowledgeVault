from sqlalchemy.orm import Session

from app.services.chunk_service import ChunkService
from app.services.llm_service import LLMService


class AskService:
    def __init__(self, db: Session):
        self.chunk_service = ChunkService(db)

    def ask(
        self,
        question: str,
        user_id: int
    ):
        chunks = self.chunk_service.retrieve_hybrid(
            query=question,
            user_id=user_id,
            limit=5
        )

        context = "\n\n".join(
            (
                f"Category: {chunk.get('intent_category') or 'Semantic match'}\n"
                f"Note: {chunk['note_title']}\n"
                f"{chunk['chunk_text']}"
            )
            for chunk in chunks
        )

        prompt = f"""
You are a helpful assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I could not find that information in your notes."

Context:
{context}

Question:
{question}

Answer:
"""

        answer = LLMService.generate(
            prompt
        )

        return {
            "question": question,
            "answer": answer
        }
