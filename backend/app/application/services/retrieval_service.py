"""Retrieval service: orchestrates the retrieval flow (REQUISITOS_RECUPERACION.md)."""

from ...domain.entities.chunk import Chunk
from ...domain.interfaces.embedding_provider import IEmbeddingProvider
from ...domain.interfaces.llm_provider import ILLMProvider
from ...domain.interfaces.normalizer import INormalizer
from ...domain.interfaces.reranker import IReranker
from ...domain.interfaces.vector_store import IVectorStore
from ...domain.value_objects.query_type import QueryType


class RetrievalService:
    """Encadena normalización, análisis, embedding, búsqueda y re-ranking."""

    def __init__(
        self,
        normalizer: INormalizer,
        llm_provider: ILLMProvider,
        embedding_provider: IEmbeddingProvider,
        vector_store: IVectorStore,
        reranker: IReranker,
        top_k_retrieval: int = 20,
        top_k_final: int = 15,
    ) -> None:
        self._normalizer = normalizer
        self._llm_provider = llm_provider
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store
        self._reranker = reranker
        self._top_k_retrieval = top_k_retrieval
        self._top_k_final = top_k_final

    def retrieve(self, query: str) -> list[Chunk]:
        normalized = self._normalizer.normalize(query)
        analysis = self._llm_provider.analyze_query(normalized)
        query_vector = self._embedding_provider.embed_query(normalized)

        author = (
            analysis.researcher_name
            if analysis.query_type == QueryType.SPECIFIC
            else None
        )

        chunks = self._vector_store.search(
            query_text=normalized,
            query_vector=query_vector,
            author=author,
            top_k=self._top_k_retrieval,
        )
        reranked = self._reranker.rerank(chunks)
        return reranked[: self._top_k_final]
