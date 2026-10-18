"""Researcher entity: a CvLAC curriculum vitae."""

from dataclasses import dataclass

from ..value_objects.cvlac_url import CvLACUrl
from ..value_objects.section import Section


@dataclass(frozen=True)
class Researcher:
    """Investigador representado por una hoja de vida CvLAC.

    Attributes:
        url: Enlace directo a la hoja de vida.
        sections: Mapeo entre cada sección y su contenido.
    """

    url: CvLACUrl
    sections: dict[Section, str]

    @property
    def identificacion(self) -> str:
        """Contenido de la sección de identificación, que incluye el nombre."""
        return self.sections[Section.IDENTIFICACION]
