"""Vector store port (IVectorStore).

Implemented by QdrantAdapter. Supports hybrid search and metadata filtering
(HU-04, HU-05).
"""

from collections.abc import Sequence
from typing import Protocol

from ..entities.chunk import Chunk
from ..value_objects.section import Section


class IVectorStore(Protocol):
    """Puerto de acceso a la base de datos vectorial."""

    def add(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None:
        """Indexa fragmentos con sus metadatos y vectores.

        Args:
            chunks: Fragmentos a indexar.
            vectors: Vectores densos correspondientes, uno por fragmento.
        """
        ...

    def search(
        self,
        query_text: str,
        query_vector: Sequence[float],
        author: str | None = None,
        section: Section | None = None,
        top_k: int = 20,
    ) -> list[Chunk]:
        """Recupera los fragmentos más relevantes mediante búsqueda híbrida.

        Args:
            query_text: Texto de la consulta para la componente léxica.
            query_vector: Vector denso de la consulta.
            author: Filtro opcional por investigador (HU-04).
            section: Filtro opcional por sección.
            top_k: Número máximo de fragmentos a recuperar.

        Returns:
            Fragmentos ordenados por relevancia descendente.
        """
        ...
