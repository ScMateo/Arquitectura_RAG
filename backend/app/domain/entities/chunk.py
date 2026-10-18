"""Chunk entity: the indexed unit of retrieval."""

from dataclasses import dataclass

from ..value_objects.cvlac_url import CvLACUrl
from ..value_objects.section import Section


@dataclass(frozen=True)
class Chunk:
    """Fragmento segmentado por unidad lógica e indexado en la base vectorial.

    Attributes:
        content: Texto del fragmento.
        author: Nombre del investigador de origen.
        section: Sección de la hoja de vida de la que proviene.
        url: Enlace a la hoja de vida (HU-03).
        score: Relevancia asignada durante la búsqueda; vacío en la ingesta.
    """

    content: str
    author: str
    section: Section
    url: CvLACUrl
    score: float | None = None
