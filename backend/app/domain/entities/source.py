"""Source entity: citation reference for a generated answer (HU-10)."""

from dataclasses import dataclass

from ..value_objects.cvlac_url import CvLACUrl
from ..value_objects.section import Section


@dataclass(frozen=True)
class Source:
    """Fuente que sustenta la información empleada en una respuesta.

    Attributes:
        author: Nombre del investigador.
        section: Sección de la hoja de vida de origen.
        url: Enlace a la hoja de vida.
        excerpt: Extracto del fragmento empleado.
    """

    author: str
    section: Section
    url: CvLACUrl
    excerpt: str
