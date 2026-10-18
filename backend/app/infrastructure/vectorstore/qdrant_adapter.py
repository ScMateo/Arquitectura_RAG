"""Qdrant adapter (implements IVectorStore).

Stores and retrieves chunks with native metadata filtering (HU-04, HU-05).
"""

import uuid
from collections.abc import Sequence

from qdrant_client import QdrantClient, models

from ...domain.entities.chunk import Chunk
from ...domain.value_objects.cvlac_url import CvLACUrl
from ...domain.value_objects.section import Section


class QdrantAdapter:
    """Almacena y busca fragmentos en Qdrant con filtrado por metadatos."""

    def __init__(self, url: str, collection_name: str) -> None:
        self._client = QdrantClient(url=url)
        self._collection = collection_name

    def add(self, chunks: Sequence[Chunk], vectors: Sequence[Sequence[float]]) -> None:
        if not chunks:
            return

        self._ensure_collection(vector_size=len(vectors[0]))

        points = [
            models.PointStruct(
                id=self._point_id(chunk),
                vector=list(vector),
                payload=self._payload(chunk),
            )
            for chunk, vector in zip(chunks, vectors)
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
        response = self._client.query_points(
            collection_name=self._collection,
            query=list(query_vector),
            query_filter=query_filter,
            limit=top_k,
        )
        return [self._to_chunk(point) for point in response.points]

    def _ensure_collection(self, vector_size: int) -> None:
        if self._client.collection_exists(self._collection):
            return
        self._client.create_collection(
            collection_name=self._collection,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
            ),
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
