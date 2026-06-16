class ChunkingService:
    """
    Splits plain text into ordered chunks of approximately
    CHUNK_SIZE characters. Splits on sentence boundaries
    ('. ') where possible to avoid cutting mid-sentence;
    falls back to a hard character split when a single
    sentence exceeds the target size.
    """

    CHUNK_SIZE: int = 500
    OVERLAP: int = 0  # reserved for future sliding-window RAG

    @staticmethod
    def split(text: str) -> list[str]:
        """
        Return a list of non-empty chunk strings in order.
        Guarantees that every chunk is <= CHUNK_SIZE * 2 chars
        and that the concatenation of all chunks covers the
        full input text (no content is dropped).
        """
        text = text.strip()

        if not text:
            return []

        # Split on sentence-ending punctuation followed by
        # whitespace so we can re-join cleanly.
        sentences = ChunkingService._split_sentences(text)

        chunks: list[str] = []
        current: list[str] = []
        current_len: int = 0

        for sentence in sentences:
            sentence_len = len(sentence)

            # If adding this sentence would exceed the target,
            # flush the current buffer first.
            if current and current_len + sentence_len > ChunkingService.CHUNK_SIZE:
                chunks.append(" ".join(current).strip())
                current = []
                current_len = 0

            # A single sentence longer than CHUNK_SIZE gets its
            # own chunk (hard-split by character).
            if sentence_len > ChunkingService.CHUNK_SIZE:
                hard_chunks = ChunkingService._hard_split(sentence)
                chunks.extend(hard_chunks)
                continue

            current.append(sentence)
            current_len += sentence_len + 1  # +1 for the space

        if current:
            chunks.append(" ".join(current).strip())

        return [c for c in chunks if c]

    # ----------------------------------------------------------
    # Private helpers
    # ----------------------------------------------------------

    @staticmethod
    def _split_sentences(text: str) -> list[str]:
        """
        Naive sentence tokeniser: split on '. ', '! ', '? '.
        Preserves the punctuation on the preceding token.
        """
        import re

        parts = re.split(r'(?<=[.!?])\s+', text)
        return [p.strip() for p in parts if p.strip()]

    @staticmethod
    def _hard_split(text: str) -> list[str]:
        """
        Split a long string into CHUNK_SIZE character slices.
        Used only when a single sentence already exceeds the limit.
        """
        size = ChunkingService.CHUNK_SIZE
        return [
            text[i: i + size]
            for i in range(0, len(text), size)
        ]
