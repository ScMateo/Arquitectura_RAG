"""Unit tests for WeightedReranker."""

from app.domain.value_objects.section import Section
from app.infrastructure.reranking.weighted_reranker import WeightedReranker
from tests.helpers import make_chunk


def test_rerank_orders_by_section_priority_before_score() -> None:
    low_priority = make_chunk(section=Section.REDES_SOCIALES, score=0.99)
    high_priority = make_chunk(section=Section.ARTICULOS, score=0.10)
    result = WeightedReranker().rerank([low_priority, high_priority])
    assert result[0] is high_priority


def test_rerank_uses_score_within_same_section() -> None:
    lower = make_chunk(section=Section.ARTICULOS, score=0.2)
    higher = make_chunk(section=Section.ARTICULOS, score=0.8)
    result = WeightedReranker().rerank([lower, higher])
    assert result[0] is higher


def test_rerank_unknown_section_sinks_to_bottom() -> None:
    reranker = WeightedReranker(section_priority={Section.ARTICULOS.value: 1})
    known = make_chunk(section=Section.ARTICULOS, score=0.1)
    unknown = make_chunk(section=Section.PATENTES, score=0.9)
    result = reranker.rerank([unknown, known])
    assert result[0] is known


def test_rerank_handles_none_score() -> None:
    first = make_chunk(section=Section.ARTICULOS, score=None)
    second = make_chunk(section=Section.ARTICULOS, score=0.5)
    result = WeightedReranker().rerank([first, second])
    assert result[0] is second
