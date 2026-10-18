"""Unit tests for the Researcher entity."""

from app.domain.entities.researcher import Researcher
from app.domain.value_objects.cvlac_url import CvLACUrl
from app.domain.value_objects.section import Section


def test_identificacion_returns_identification_section() -> None:
    researcher = Researcher(
        url=CvLACUrl("https://example.org/cv"),
        sections={
            Section.IDENTIFICACION: "Nombre Juan Perez",
            Section.ARTICULOS: "Articulo uno.",
        },
    )
    assert researcher.identificacion == "Nombre Juan Perez"
