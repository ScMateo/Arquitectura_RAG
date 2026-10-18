"""Unit tests for the BM25-style sparse encoder."""

from app.infrastructure.embeddings.bm25_sparse_encoder import Bm25SparseEncoder


def test_encode_query_returns_term_frequencies() -> None:
    vector = Bm25SparseEncoder().encode_query("salud publica salud")

    assert len(vector) == 2
    assert sorted(vector.values()) == [1.0, 2.0]


def test_encoding_is_deterministic_across_instances() -> None:
    assert Bm25SparseEncoder().encode_query("dato") == Bm25SparseEncoder().encode_query("dato")


def test_empty_text_yields_empty_vector() -> None:
    assert Bm25SparseEncoder().encode_query("") == {}


def test_encode_documents_returns_one_vector_per_text() -> None:
    vectors = Bm25SparseEncoder().encode_documents(["uno", "dos tres"])

    assert len(vectors) == 2
    assert len(vectors[1]) == 2
