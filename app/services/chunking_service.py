class ChunkingService:
    """
    Splits plain text into ordered chunks of approximately
    CHUNK_SIZE characters with OVERLAP characters of carry-over
    from the previous chunk.

    Overlap prevents context loss at chunk boundaries — without it,
    a sentence that spans two chunks is split cold, so neither chunk
    contains enough context to answer a question about that sentence.
    50-character overlap is conservative; increase to 100-150 if
    retrieval quality on boundary-spanning content is still poor.
    """

    CHUNK_SIZE: int = 500
    OVERLAP: int = 50

    @staticmethod
    def split(text: str) -> list[str]:
        """
        Return a list of non-empty chunk strings in order.
        Each chunk (except the first) begins with up to OVERLAP
        characters carried over from the end of the previous chunk,
        ensuring no context is lost at boundaries.
        """
        text = text.strip()

        if not text:
            return []

        sentences = ChunkingService._split_sentences(text)

        chunks: list[str] = []
        current: list[str] = []
        current_len: int = 0

        for sentence in sentences:
            sentence_len = len(sentence)

            if current and current_len + sentence_len > ChunkingService.CHUNK_SIZE:
                chunk_text = " ".join(current).strip()
                chunks.append(chunk_text)

                # Carry the tail of the current chunk into the next one
                # so queries that straddle a boundary still find a match.
                overlap_text = chunk_text[-ChunkingService.OVERLAP:] if ChunkingService.OVERLAP > 0 else ""
                current = [overlap_text] if overlap_text else []
                current_len = len(overlap_text)

            if sentence_len > ChunkingService.CHUNK_SIZE:
                hard_chunks = ChunkingService._hard_split(sentence)
                # Apply overlap between hard-split pieces too
                for i, hc in enumerate(hard_chunks):
                    if i == 0:
                        chunks.append(hc)
                    else:
                        prev_tail = hard_chunks[i - 1][-ChunkingService.OVERLAP:] if ChunkingService.OVERLAP > 0 else ""
                        chunks.append((prev_tail + " " + hc).strip() if prev_tail else hc)
                current = []
                current_len = 0
                continue

            current.append(sentence)
            current_len += sentence_len + 1

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
