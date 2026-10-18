"""Qdrant adapter (implements IVectorStore).

Supports dense search and hybrid search (dense + lexical) with native metadata
filtering (HU-04, HU-05, RT-2, RT-3). When a sparse encoder is provided, the
collection keeps a named dense vector and a named sparse vector, and queries are
resolved through reciprocal rank fusion (RRF) computed server-side. Without a
sparse encoder it falls back to dense-only search.
"""

import uuid
from collections.abc import Sequence

from qdrant_client import QdrantClient, models

from ...domain.entities.chunk import Chunk
from ...domain.interfaces.sparse_encoder import ISparseEncoder
from ...domain.value_objects.cvlac_url import CvLACUrl
from ...domain.value_objects.section import Section

_DENSE = "dense"
_SPARSE = "sparse"


class QdrantAdapter:
    """Almacena y busca fragmentos en Qdrant (denso o híbrido)."""

    def __init__(
        self,
        url: str,
        collection_name: str,
        sparse_encoder: ISparseEncoder | None = None,
    ) -> None:
        self._client = QdrantClient(url=url)
        self._collection = collection_name
        self._sparse_encoder = sparse_encoder

    def add(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None:
        if not chunks:
            return

        self._ensure_collection(vector_size=len(vectors[0]))

        sparse_vectors = (
            self._sparse_encoder.encode_documents([chunk.content for chunk in chunks])
            if self._sparse_encoder is not None
            else None
        )
        points = [
            models.PointStruct(
                id=self._point_id(chunk),
                vector=self._point_vector(index, vector, sparse_vectors),  # type: ignore[arg-type]
                payload=self._payload(chunk),
            )
            for index, (chunk, vector) in enumerate(zip(chunks, vectors))
        ]
        self._client.upsert(collection_name=self._collection, points=points)

    def search(
        self,
        query_text: str,
        query_vector: Sequence[float],
        author: str | None = None,
        section: Section | None = None,
        top_k: int = 20,
    ) -> list[Chunk]:
        query_filter = self._build_filter(author, section)
        if self._sparse_encoder is None:
            response = self._client.query_points(
                collection_name=self._collection,
                query=list(query_vector),
                query_filter=query_filter,
                limit=top_k,
            )
        else:
            response = self._client.query_points(
                collection_name=self._collection,
                prefetch=self._prefetch(query_text, query_vector, query_filter, top_k),
                query=models.FusionQuery(fusion=models.Fusion.RRF),
                limit=top_k,
            )
        return [self._to_chunk(point) for point in response.points]

    def _prefetch(
        self,
        query_text: str,
        query_vector: Sequence[float],
        query_filter: models.Filter | None,
        top_k: int,
    ) -> list[models.Prefetch]:
        candidates = max(top_k, 20)
        sparse = self._sparse_encoder.encode_query(query_text)  # type: ignore[union-attr]
        return [
            models.Prefetch(
                query=list(query_vector),
                using=_DENSE,
                limit=candidates,
                filter=query_filter,
            ),
            models.Prefetch(
                query=self._sparse_vector(sparse),
                using=_SPARSE,
                limit=candidates,
                filter=query_filter,
            ),
        ]

    def _ensure_collection(self, vector_size: int) -> None:
        if self._client.collection_exists(self._collection):
            return
        if self._sparse_encoder is None:
            self._client.create_collection(
                collection_name=self._collection,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE,
                ),
            )
            return
        self._client.create_collection(
            collection_name=self._collection,
            vectors_config={
                _DENSE: models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE,
                )
            },
            sparse_vectors_config={
                _SPARSE: models.SparseVectorParams(modifier=models.Modifier.IDF)
            },
        )

    def _build_filter(
        self,
        author: str | None,
        section: Section | None,
    ) -> models.Filter | None:
        conditions: list[models.FieldCondition] = []
        if author:
            conditions.append(
                models.FieldCondition(key="author", match=models.MatchValue(value=author))
            )
        if section:
            conditions.append(
                models.FieldCondition(key="section", match=models.MatchValue(value=section.value))
            )
        if not conditions:
            return None
        return models.Filter(must=conditions)  # type: ignore[arg-type]

    def _point_vector(
        self,
        index: int,
        dense_vector: Sequence[float],
        sparse_vectors: list[dict[int, float]] | None,
    ) -> list[float] | dict[str, list[float] | models.SparseVector]:
        if sparse_vectors is None:
            return list(dense_vector)
        return {
            _DENSE: list(dense_vector),
            _SPARSE: self._sparse_vector(sparse_vectors[index]),
        }

    @staticmethod
    def _sparse_vector(sparse: dict[int, float]) -> models.SparseVector:
        indices = list(sparse.keys())
        return models.SparseVector(indices=indices, values=[sparse[index] for index in indices])

    @staticmethod
    def _point_id(chunk: Chunk) -> str:
        # Deterministic ID so re-indexing is idempotent.
        key = f"{chunk.author}:{chunk.section.value}:{chunk.content}"
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, key))

    @staticmethod
    def _payload(chunk: Chunk) -> dict:
        return {
            "content": chunk.content,
            "author": chunk.author,
            "section": chunk.section.value,
            "url": chunk.url.value,
        }

    @staticmethod
    def _to_chunk(point) -> Chunk:
        payload = point.payload
        return Chunk(
            content=payload["content"],
            author=payload["author"],
            section=Section(payload["section"]),
            url=CvLACUrl(payload["url"]),
            score=point.score,
        )
