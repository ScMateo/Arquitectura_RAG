"""Reranker port (IReranker).

Implemented by WeightedReranker. Combines relevance score with section
priority.
"""

from collections.abc import Sequence
from typing import Protocol

from ..entities.chunk import Chunk


class IReranker(Protocol):
    """Puerto de ordenación de fragmentos recuperados."""

    def rerank(self, chunks: Sequence[Chunk]) -> list[Chunk]:
        """Reordena los fragmentos por relevancia y prioridad de sección.

        Args:
            chunks: Fragmentos recuperados con su puntuación.

        Returns:
            Fragmentos reordenados.
        """
        ...
