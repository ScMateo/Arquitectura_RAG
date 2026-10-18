"""Pytest fixtures built on top of tests.helpers."""

from __future__ import annotations

import pytest

from tests.helpers import FakeEmbeddingProvider, FakeLLMProvider, FakeVectorStore


@pytest.fixture
def embedding_provider() -> FakeEmbeddingProvider:
    return FakeEmbeddingProvider()


@pytest.fixture
def vector_store() -> FakeVectorStore:
    return FakeVectorStore()


@pytest.fixture
def llm_provider() -> FakeLLMProvider:
    return FakeLLMProvider()
