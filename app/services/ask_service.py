import time

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
        start = time.time()

        chunks = self.chunk_service.retrieve_hybrid(
            query=question,
            user_id=user_id,
            limit=3
        )

        print(
            f"RETRIEVAL: {time.time() - start:.2f}s"
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
You are a retrieval assistant.

Use ONLY the provided notes.

DO NOT infer.
DO NOT guess.
DO NOT add information that is not present.
DO NOT explain your reasoning.

If the user asks for a list, return a simple bullet list.

If the answer cannot be found in the context, say exactly:

"I could not find that information in your notes."

Context:
{context}

Question:
{question}

Answer:
"""

        llm_start = time.time()

        answer = LLMService.generate(
            prompt=prompt,
            model=LLMService.ASK_MODEL
        )

        print(
            f"LLM: {time.time() - llm_start:.2f}s"
        )

        print(
            f"TOTAL: {time.time() - start:.2f}s"
        )

        sources = list(
            dict.fromkeys(
                chunk["note_title"]
                for chunk in chunks
            )
        )

        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }