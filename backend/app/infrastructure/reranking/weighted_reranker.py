"""Weighted reranker (implements IReranker).

Orders chunks by section priority and relevance score
(REQUISITOS_RECUPERACION.md §5.3).
"""

from collections.abc import Sequence

from ...core.constants import SECTION_PRIORITY
from ...domain.entities.chunk import Chunk


class WeightedReranker:
    """Reordena fragmentos por prioridad de sección y relevancia."""

    def __init__(self, section_priority: dict[str, int] | None = None) -> None:
        self._section_priority = section_priority or SECTION_PRIORITY

    def rerank(self, chunks: Sequence[Chunk]) -> list[Chunk]:
        def key(chunk: Chunk) -> tuple[int, float]:
            priority = self._section_priority.get(chunk.section.value, 99)
            score = chunk.score if chunk.score is not None else 0.0
            return (priority, -score)

        return sorted(chunks, key=key)
