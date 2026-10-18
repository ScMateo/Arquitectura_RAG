"""Reranker port (IReranker).

Implemented by WeightedReranker. Combines relevance score with section
priority.
"""

from collections.abc import Sequence
from typing import Protocol

from ..entities.chunk import Chunk


class IReranker(Protocol):
    """Puerto de ordenación de fragmentos recuperados."""

    def rerank(self, chunks: Sequence[Chunk], query: str | None = None) -> list[Chunk]:
        """Reordena los fragmentos por relevancia y prioridad de sección.

        Args:
            chunks: Fragmentos recuperados con su puntuación.
            query: Consulta normalizada; si indica una sección concreta, esa
                sección se prioriza. Si es ``None`` se aplica la prioridad fija.

        Returns:
            Fragmentos reordenados.
        """
        ...
