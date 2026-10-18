"""Unit tests for RetrievalService (orchestration with mocked ports)."""

from app.application.services.retrieval_service import RetrievalService
from app.domain.value_objects.query_analysis import QueryAnalysis
from app.domain.value_objects.section import Section
from app.domain.value_objects.query_type import QueryType
from app.infrastructure.reranking.weighted_reranker import WeightedReranker
from tests.helpers import (
    FakeEmbeddingProvider,
    FakeLLMProvider,
    FakeVectorStore,
    make_chunk,
)


class _SpyNormalizer:
    def __init__(self) -> None:
        self.seen: list[str] = []

    def normalize(self, text: str) -> str:
        self.seen.append(text)
        return text.upper()


def _build_service(
    normalizer: _SpyNormalizer,
    llm: FakeLLMProvider,
    store: FakeVectorStore,
    top_k_retrieval: int = 20,
    top_k_final: int = 15,
) -> RetrievalService:
    return RetrievalService(
        normalizer=normalizer,
        llm_provider=llm,
        embedding_provider=FakeEmbeddingProvider(),
        vector_store=store,
        reranker=WeightedReranker(),
        top_k_retrieval=top_k_retrieval,
        top_k_final=top_k_final,
    )


def test_retrieve_normalizes_and_searches_without_author_for_general() -> None:
    normalizer = _SpyNormalizer()
    llm = FakeLLMProvider(analysis=QueryAnalysis(query_type=QueryType.GENERAL))
    store = FakeVectorStore(results=[make_chunk(content="c1")])
    service = _build_service(normalizer, llm, store)

    result = service.retrieve("consulta")

    assert normalizer.seen == ["consulta"]
    assert store.last_search is not None
    assert store.last_search["query_text"] == "CONSULTA"
    assert store.last_search["author"] is None
    assert len(result) == 1


def test_retrieve_applies_author_filter_for_specific_query() -> None:
    normalizer = _SpyNormalizer()
    llm = FakeLLMProvider(
        analysis=QueryAnalysis(query_type=QueryType.SPECIFIC, researcher_name="Juan Perez")
    )
    store = FakeVectorStore(results=[make_chunk()])
    service = _build_service(normalizer, llm, store)

    service.retrieve("formacion de juan perez")

    assert store.last_search is not None
    assert store.last_search["author"] == "Juan Perez"


def test_retrieve_prioritizes_requested_section_for_specific_query() -> None:
    normalizer = _SpyNormalizer()
    llm = FakeLLMProvider(
        analysis=QueryAnalysis(query_type=QueryType.SPECIFIC, researcher_name="Juan Perez")
    )
    store = FakeVectorStore(
        results=[
            make_chunk(section=Section.ARTICULOS, score=0.10),
            make_chunk(section=Section.REDES_SOCIALES, score=0.99),
        ]
    )
    service = _build_service(normalizer, llm, store)

    result = service.retrieve("redes sociales de juan perez")

    assert result[0].section is Section.REDES_SOCIALES


def test_retrieve_truncates_to_top_k_final() -> None:
    normalizer = _SpyNormalizer()
    llm = FakeLLMProvider(analysis=QueryAnalysis(query_type=QueryType.GENERAL))
    store = FakeVectorStore(results=[make_chunk(content=f"c{i}") for i in range(30)])
    service = _build_service(normalizer, llm, store, top_k_retrieval=30, top_k_final=5)

    result = service.retrieve("q")

    assert len(result) == 5
