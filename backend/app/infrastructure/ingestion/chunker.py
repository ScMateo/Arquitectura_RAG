"""Logical unit chunker (implements IChunker).

Segments a section into logical units with a maximum size fallback
(ESTRATEGIA_SEGMENTACION_EMBEDDINGS.md).
"""

import re

from ...domain.value_objects.section import Section


class LogicalUnitChunker:
    """Segmenta el contenido por unidades lógicas con límite de tamaño."""

    _SENTENCE_END = re.compile(r"(?<=[.!?])\s+")

    def __init__(self, max_chunk_size: int = 1500) -> None:
        self._max_chunk_size = max_chunk_size

    def chunk(self, section: Section, content: str) -> list[str]:
        sentences = [s.strip() for s in self._SENTENCE_END.split(content) if s.strip()]
        chunks: list[str] = []
        current = ""

        for sentence in sentences:
            if len(current) + len(sentence) + 1 > self._max_chunk_size and current:
                chunks.append(current)
                current = sentence
            else:
                current = f"{current} {sentence}".strip()

        if current:
            chunks.append(current)

        return chunks
