"""Chunker port (IChunker).

Implemented by LogicalUnitChunker. Segments each section by logical unit
with a maximum size fallback.
"""

from typing import Protocol

from ..value_objects.section import Section


class IChunker(Protocol):
    """Puerto de segmentación por unidad lógica."""

    def chunk(self, section: Section, content: str) -> list[str]:
        """Divide el contenido de una sección en unidades lógicas.

        Args:
            section: Sección de origen del contenido.
            content: Contenido a segmentar.

        Returns:
            Lista de fragmentos de texto.
        """
        ...
