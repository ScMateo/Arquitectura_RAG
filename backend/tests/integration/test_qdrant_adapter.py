"""Integration tests for QdrantAdapter against a real (ephemeral) collection.

Skips automatically if no Qdrant server is reachable at QDRANT_URL.
Uses deterministic fake vectors, so the embedding model is not required.
"""

import uuid

import pytest
from qdrant_client import QdrantClient

from app.core.config import get_settings
from app.domain.value_objects.section import Section
from app.infrastructure.vectorstore.qdrant_adapter import QdrantAdapter
from tests.helpers import make_chunk

pytestmark = pytest.mark.integration


@pytest.fixture
def qdrant_url() -> str:
    url = get_settings().qdrant_url
    try:
        QdrantClient(url=url).get_collections()
    except Exception as error:  # noqa: BLE001
        pytest.skip(f"Qdrant no disponible en {url}: {error}")
    return url


@pytest.fixture
def adapter(qdrant_url: str) -> QdrantAdapter:
    collection = f"test_{uuid.uuid4().hex[:8]}"
    yield QdrantAdapter(url=qdrant_url, collection_name=collection)
    QdrantClient(url=qdrant_url).delete_collection(collection)


def test_add_and_search_roundtrip(adapter: QdrantAdapter) -> None:
    chunks = [
        make_chunk(content="uno", author="Ana"),
        make_chunk(content="dos", author="Luis"),
    ]
    adapter.add(chunks, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])

    results = adapter.search("uno", [1.0, 0.0, 0.0], top_k=10)

    assert len(results) == 2
    assert {chunk.author for chunk in results} == {"Ana", "Luis"}
    assert results[0].score is not None


def test_author_filter_is_applied(adapter: QdrantAdapter) -> None:
    adapter.add(
        [make_chunk(content="a", author="Ana"), make_chunk(content="b", author="Luis")],
        [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
    )

    results = adapter.search("x", [1.0, 0.0, 0.0], author="Ana", top_k=10)

    assert results
    assert all(chunk.author == "Ana" for chunk in results)


def test_reindexing_same_chunk_is_idempotent(adapter: QdrantAdapter) -> None:
    chunk = make_chunk(content="mismo contenido", author="Ana")
    adapter.add([chunk], [[1.0, 0.0, 0.0]])
    adapter.add([chunk], [[1.0, 0.0, 0.0]])

    results = adapter.search("mismo", [1.0, 0.0, 0.0], top_k=10)

    assert len(results) == 1


def test_section_filter_is_applied(adapter: QdrantAdapter) -> None:
    adapter.add(
        [
            make_chunk(content="a", author="Ana", section=Section.ARTICULOS),
            make_chunk(content="b", author="Ana", section=Section.LIBROS),
        ],
        [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]],
    )

    results = adapter.search("x", [1.0, 0.0, 0.0], section=Section.LIBROS, top_k=10)

    assert results
    assert all(chunk.section is Section.LIBROS for chunk in results)


def test_add_without_chunks_is_a_noop(adapter: QdrantAdapter) -> None:
    adapter.add([], [])

