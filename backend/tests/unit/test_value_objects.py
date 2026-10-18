"""Unit tests for the domain value objects."""

import pytest

from app.domain.value_objects.cvlac_url import CvLACUrl
from app.domain.value_objects.message_role import MessageRole
from app.domain.value_objects.query_analysis import QueryAnalysis
from app.domain.value_objects.query_type import QueryType
from app.domain.value_objects.section import Section


def test_cvlac_url_accepts_https() -> None:
    url = CvLACUrl("https://example.org/cv")
    assert url.value == "https://example.org/cv"


@pytest.mark.parametrize("bad", ["http://example.org", "example.org", "", "ftp://x"])
def test_cvlac_url_rejects_non_https(bad: str) -> None:
    with pytest.raises(ValueError):
        CvLACUrl(bad)


def test_section_has_22_members() -> None:
    assert len(Section) == 22


def test_section_values_match_csv_columns() -> None:
    assert Section.IDENTIFICACION.value == "identificacion"
    assert Section.FORMACION_ACADEMICA.value == "formacion_academica"
    assert Section.PAR_EVALUADOR.value == "par_evaluador"


def test_query_type_values() -> None:
    assert QueryType.SPECIFIC == "specific"
    assert QueryType.GENERAL == "general"


def test_query_analysis_defaults_name_to_none() -> None:
    analysis = QueryAnalysis(query_type=QueryType.GENERAL)
    assert analysis.researcher_name is None


def test_message_role_values() -> None:
    assert MessageRole.USER == "user"
    assert MessageRole.ASSISTANT == "assistant"
