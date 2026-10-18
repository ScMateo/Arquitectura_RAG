"""Unit tests for the HTTP layer (endpoint contract with an overridden use case)."""

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.application.dto.chat import ChatResponse, SourceDTO


class _FakeUseCase:
    def execute(self, request) -> ChatResponse:
        return ChatResponse(
            answer=f"eco: {request.message}",
            sources=[
                SourceDTO(
                    author="Autor Uno",
                    section="articulos",
                    url="https://example.org/cv/1",
                    excerpt="extracto",
                )
            ],
        )


@pytest.fixture
def client() -> Iterator[TestClient]:
    from app.api.dependencies import get_chat_use_case
    from app.main import app

    app.dependency_overrides[get_chat_use_case] = lambda: _FakeUseCase()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_returns_answer_and_sources(client: TestClient) -> None:
    response = client.post("/api/chat", json={"message": "hola", "session_id": "s1"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "eco: hola"
    assert body["sources"][0]["author"] == "Autor Uno"
    assert set(body["sources"][0]) == {"author", "section", "url", "excerpt"}


def test_chat_requires_message_field(client: TestClient) -> None:
    response = client.post("/api/chat", json={})
    assert response.status_code == 422
