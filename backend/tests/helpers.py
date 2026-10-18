"""Test doubles and factories shared across the test suite."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from app.domain.entities.chunk import Chunk
from app.domain.value_objects.cvlac_url import CvLACUrl
from app.domain.value_objects.query_analysis import QueryAnalysis
from app.domain.value_objects.query_type import QueryType
from app.domain.value_objects.section import Section

DEFAULT_URL = (
    "https://scienti.minciencias.gov.co/cvlac/visualizador/"
    "generarCurriculoCv.do?cod_rh=0000000001"
)


def make_chunk(
    content: str = "contenido",
    author: str = "Autor Uno",
    section: Section = Section.ARTICULOS,
    score: float | None = None,
    url: str = DEFAULT_URL,
) -> Chunk:
    """Build a Chunk with sensible defaults (factory for tests)."""
    return Chunk(
        content=content,
        author=author,
        section=section,
        url=CvLACUrl(url),
        score=score,
    )


class FakeEmbeddingProvider:
    """Deterministic embedding provider (port IEmbeddingProvider)."""

    def __init__(self, dimension: int = 3) -> None:
        self._dimension = dimension
        self.document_calls: list[Sequence[str]] = []

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        self.document_calls.append(list(texts))
        return [self._vector(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._vector(text)

    def _vector(self, text: str) -> list[float]:
        vector = [0.0] * self._dimension
        if self._dimension:
            vector[0] = float(len(text) + 1)
        return vector


class FakeVectorStore:
    """In-memory vector store (port IVectorStore)."""

    def __init__(self, results: Sequence[Chunk] | None = None) -> None:
        self.added_chunks: list[Chunk] = []
        self.added_vectors: list[list[float]] = []
        self.results = list(results or [])
        self.last_search: dict | None = None

    def add(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None:
        self.added_chunks.extend(chunks)
        self.added_vectors.extend([list(vector) for vector in vectors])

    def search(
        self,
        query_text: str,
        query_vector: Sequence[float],
        author: str | None = None,
        section: Section | None = None,
        top_k: int = 20,
    ) -> list[Chunk]:
        self.last_search = {
            "query_text": query_text,
            "query_vector": list(query_vector),
            "author": author,
            "section": section,
            "top_k": top_k,
        }
        return self.results[:top_k]


class FakeLLMProvider:
    """Scriptable LLM provider (port ILLMProvider)."""

    def __init__(
        self,
        analysis: QueryAnalysis | None = None,
        answer: str = "respuesta generada",
    ) -> None:
        self.analysis = analysis or QueryAnalysis(query_type=QueryType.GENERAL)
        self.answer = answer
        self.prompts: list[str] = []

    def analyze_query(self, query: str) -> QueryAnalysis:
        return self.analysis

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.answer

    def stream(self, prompt: str) -> Iterator[str]:
        yield self.answer
