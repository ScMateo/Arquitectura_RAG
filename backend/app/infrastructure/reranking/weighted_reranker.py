"""Weighted reranker (implements IReranker).

Orders chunks by section priority and relevance score
(REQUISITOS_RECUPERACION.md §5.3). When the query explicitly asks about a
section, that section is prioritized so the requested information is not buried
by the fixed priority order.
"""

import re
from collections.abc import Sequence

from ...core.constants import SECTION_KEYWORDS, SECTION_PRIORITY
from ...domain.entities.chunk import Chunk


class WeightedReranker:
    """Reordena fragmentos por prioridad de sección y relevancia."""

    def __init__(self, section_priority: dict[str, int] | None = None) -> None:
        self._section_priority = section_priority or SECTION_PRIORITY

    def rerank(self, chunks: Sequence[Chunk], query: str | None = None) -> list[Chunk]:
        target = self._target_section(query)

        def key(chunk: Chunk) -> tuple[int, float]:
            if target is not None and chunk.section.value == target:
                priority = 0
            else:
                priority = self._section_priority.get(chunk.section.value, 99)
            score = chunk.score if chunk.score is not None else 0.0
            return (priority, -score)

        return sorted(chunks, key=key)

    @staticmethod
    def _target_section(query: str | None) -> str | None:
        """Devuelve la sección solicitada por la consulta, si es identificable."""
        if not query:
            return None
        lowered = query.lower()
        for section, keywords in SECTION_KEYWORDS:
            if any(re.search(rf"\b{re.escape(word)}\b", lowered) for word in keywords):
                return section
        return None
