"""Unit tests for GeminiAdapter retry classification (no network calls)."""

import pytest

from app.infrastructure.llm.gemini_adapter import GeminiAdapter


def test_is_retryable_for_transient_errors() -> None:
    assert GeminiAdapter._is_retryable(Exception("503 Service Unavailable"))
    assert GeminiAdapter._is_retryable(Exception("429 Too Many Requests"))
    assert GeminiAdapter._is_retryable(Exception("ReadTimeout: timed out"))
    assert GeminiAdapter._is_retryable(Exception("DeadlineExceeded"))


def test_is_retryable_for_permanent_errors() -> None:
    assert not GeminiAdapter._is_retryable(Exception("400 Bad Request"))
    assert not GeminiAdapter._is_retryable(Exception("404 Not Found"))


def test_retry_recovers_from_transient_error() -> None:
    adapter = GeminiAdapter(api_key="test")
    calls = {"n": 0}

    def operation() -> str:
        calls["n"] += 1
        if calls["n"] < 2:
            raise RuntimeError("503 Service Unavailable")
        return "ok"

    assert adapter._retry(operation, base_wait=0.0) == "ok"
    assert calls["n"] == 2


def test_retry_raises_on_permanent_error() -> None:
    adapter = GeminiAdapter(api_key="test")

    def operation() -> str:
        raise RuntimeError("400 Bad Request")

    with pytest.raises(RuntimeError, match="400"):
        adapter._retry(operation, base_wait=0.0)
