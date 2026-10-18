"""Dependency injection (composition root).

Wires the adapters, services and use cases into singletons.
"""

from functools import lru_cache

from app.application.services.generation_service import GenerationService
from app.application.services.retrieval_service import RetrievalService
from app.application.use_cases.chat_use_case import ChatUseCase
from app.core.config import get_settings
from app.infrastructure.conversation import InMemoryConversationStore
from app.infrastructure.embeddings import Bm25SparseEncoder, HuggingFaceAdapter
from app.infrastructure.ingestion import (
    AcronymNormalizer,
    Cleaner,
    CsvIngestor,
    Indexer,
    LogicalUnitChunker,
)
from app.infrastructure.llm import GeminiAdapter
from app.infrastructure.reranking import WeightedReranker
from app.infrastructure.vectorstore import QdrantAdapter


@lru_cache
def _get_embedding_provider() -> HuggingFaceAdapter:
    settings = get_settings()
    return HuggingFaceAdapter(
        model_name=settings.embedding_model_name,
        device=settings.embedding_device,
    )


@lru_cache
def _get_sparse_encoder() -> Bm25SparseEncoder:
    # Léxico para la búsqueda híbrida (RT-2): BM25 sparse servido por Qdrant.
    return Bm25SparseEncoder()


@lru_cache
def _get_vector_store() -> QdrantAdapter:
    settings = get_settings()
    return QdrantAdapter(
        url=settings.qdrant_url,
        collection_name=settings.qdrant_collection,
        sparse_encoder=_get_sparse_encoder(),
    )


@lru_cache
def _get_llm_provider() -> GeminiAdapter:
    settings = get_settings()
    return GeminiAdapter(
        api_key=settings.google_api_key.get_secret_value(),
        model=settings.gemini_model,
        timeout_ms=settings.llm_timeout_ms,
        analysis_temperature=settings.llm_temperature_analysis,
        generation_temperature=settings.llm_temperature_generation,
    )


@lru_cache
def get_chat_use_case() -> ChatUseCase:
    settings = get_settings()
    normalizer = AcronymNormalizer()
    reranker = WeightedReranker()
    conversation_store = InMemoryConversationStore(max_history=settings.max_history)

    retrieval_service = RetrievalService(
        normalizer=normalizer,
        llm_provider=_get_llm_provider(),
        embedding_provider=_get_embedding_provider(),
        vector_store=_get_vector_store(),
        reranker=reranker,
        top_k_retrieval=settings.top_k_retrieval,
        top_k_final=settings.top_k_final,
    )
    generation_service = GenerationService(llm_provider=_get_llm_provider())

    return ChatUseCase(
        retrieval_service=retrieval_service,
        generation_service=generation_service,
        conversation_store=conversation_store,
    )


@lru_cache
def get_indexer() -> Indexer:
    settings = get_settings()
    cleaner = Cleaner()
    normalizer = AcronymNormalizer()
    chunker = LogicalUnitChunker(max_chunk_size=settings.chunk_size)
    ingestor = CsvIngestor(cleaner, normalizer, chunker)
    return Indexer(
        ingestor=ingestor,
        embedding_provider=_get_embedding_provider(),
        vector_store=_get_vector_store(),
    )
