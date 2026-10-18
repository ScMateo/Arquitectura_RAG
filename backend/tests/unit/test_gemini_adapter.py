"""Unit tests for GeminiAdapter retry classification (no network calls)."""

from app.infrastructure.llm.gemini_adapter import GeminiAdapter


def test_is_retryable_for_transient_errors() -> None:
    assert GeminiAdapter._is_retryable(Exception("503 Service Unavailable"))
    assert GeminiAdapter._is_retryable(Exception("429 Too Many Requests"))


def test_is_retryable_for_permanent_errors() -> None:
    assert not GeminiAdapter._is_retryable(Exception("400 Bad Request"))
    assert not GeminiAdapter._is_retryable(Exception("404 Not Found"))
