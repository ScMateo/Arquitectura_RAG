"""Indexer: orchestrates ingestion, embedding and indexing."""

from ...domain.interfaces.embedding_provider import IEmbeddingProvider
from ...domain.interfaces.ingestor import IIngestor
from ...domain.interfaces.vector_store import IVectorStore


class Indexer:
    """Carga la información: ingesta, generación de embeddings e indexación."""

    def __init__(
        self,
        ingestor: IIngestor,
        embedding_provider: IEmbeddingProvider,
        vector_store: IVectorStore,
    ) -> None:
        self._ingestor = ingestor
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    def index(self, csv_path: str) -> None:
        """Procesa un CSV y lo indexa en la base vectorial.

        Args:
            csv_path: Ruta del archivo CSV conforme al contrato de datos.
        """
        chunks = self._ingestor.ingest(csv_path)
        texts = [chunk.content for chunk in chunks]
        vectors = self._embedding_provider.embed_documents(texts)
        self._vector_store.add(chunks, vectors)
