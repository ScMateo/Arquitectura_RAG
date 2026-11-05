"""Unit tests for GroqAdapter (no network calls, fake client)."""

from types import SimpleNamespace

import pytest

from app.domain.value_objects.query_type import QueryType
from app.infrastructure.llm.groq_adapter import GroqAdapter


class _Completions:
    """Doble del recurso chat.completions.create."""

    def __init__(self, responses: list[object]) -> None:
        self._responses = iter(responses)
        self.calls: list[dict[str, object]] = []

    def create(self, **kwargs: object) -> object:
        self.calls.append(kwargs)
        return next(self._responses)


class _Client:
    def __init__(self, completions: _Completions) -> None:
        self.chat = SimpleNamespace(completions=completions)


def _response(content: str | None) -> object:
    message = SimpleNamespace(content=content)
    return SimpleNamespace(choices=[SimpleNamespace(message=message)])


def _chunk(content: str | None) -> object:
    delta = SimpleNamespace(content=content)
    return SimpleNamespace(choices=[SimpleNamespace(delta=delta)])


def _adapter(completions: _Completions) -> GroqAdapter:
    return GroqAdapter(api_key="test", client=_Client(completions))


def test_analyze_query_parses_multiple_researchers() -> None:
    completions = _Completions(
        [_response('{"type": "specific", "researcher_names": ["Ana", "Luis"]}')]
    )
    adapter = _adapter(completions)

    analysis = adapter.analyze_query("quien tiene mas articulos, Ana o Luis")

    assert analysis.query_type is QueryType.SPECIFIC
    assert analysis.researcher_names == ("Ana", "Luis")
    assert completions.calls[0]["response_format"] == {"type": "json_object"}


def test_analyze_query_returns_general_without_names() -> None:
    completions = _Completions([_response('{"type": "general"}')])

    analysis = _adapter(completions).analyze_query("investigadores en IA")

    assert analysis.query_type is QueryType.GENERAL
    assert analysis.researcher_names == ()


def test_analyze_query_raises_on_empty_content() -> None:
    adapter = _adapter(_Completions([_response(None)]))

    with pytest.raises(ValueError, match="análisis estructurado"):
        adapter.analyze_query("q")


def test_generate_returns_content() -> None:
    completions = _Completions([_response("respuesta")])
    adapter = _adapter(completions)

    assert adapter.generate("prompt") == "respuesta"
    assert completions.calls[0]["model"] == "openai/gpt-oss-120b"


def test_generate_raises_on_empty_content() -> None:
    adapter = _adapter(_Completions([_response(None)]))

    with pytest.raises(RuntimeError, match="no devolvió respuesta"):
        adapter.generate("prompt")


def test_stream_concatenates_deltas_and_skips_empty() -> None:
    completions = _Completions([iter([_chunk("Hola"), _chunk(None), _chunk(" mundo")])])
    adapter = _adapter(completions)

    assert "".join(adapter.stream("prompt")) == "Hola mundo"
    assert completions.calls[0]["stream"] is True


def test_is_retryable_for_transient_errors() -> None:
    assert GroqAdapter._is_retryable(Exception("503 Service Unavailable"))
    assert GroqAdapter._is_retryable(Exception("429 rate limit reached"))
    assert GroqAdapter._is_retryable(Exception("Connection error."))
    assert GroqAdapter._is_retryable(Exception("Request timed out"))


def test_is_retryable_by_status_code() -> None:
    assert GroqAdapter._is_retryable(SimpleNamespace(status_code=503))  # type: ignore[arg-type]
    assert not GroqAdapter._is_retryable(SimpleNamespace(status_code=400))  # type: ignore[arg-type]


def test_is_retryable_for_permanent_errors() -> None:
    assert not GroqAdapter._is_retryable(Exception("400 Bad Request"))
    assert not GroqAdapter._is_retryable(Exception("invalid api key"))


def test_retry_recovers_from_transient_error() -> None:
    adapter = GroqAdapter(api_key="test", client=_Client(_Completions([])))
    calls = {"n": 0}

    def operation() -> str:
        calls["n"] += 1
        if calls["n"] < 2:
            raise RuntimeError("503 Service Unavailable")
        return "ok"

    assert adapter._retry(operation, base_wait=0.0) == "ok"
    assert calls["n"] == 2


def test_retry_honors_retry_after_header() -> None:
    adapter = GroqAdapter(api_key="test", client=_Client(_Completions([])))
    calls = {"n": 0}
    waits: list[float] = []

    def operation() -> str:
        calls["n"] += 1
        if calls["n"] < 2:
            error = RuntimeError("429 rate limit reached")
            error.response = SimpleNamespace(headers={"retry-after": "7"})  # type: ignore[attr-defined]
            raise error
        return "ok"

    assert adapter._retry(operation, base_wait=0.0, sleep=waits.append) == "ok"
    assert waits == [7.0]


def test_retry_after_ignores_invalid_header() -> None:
    error = RuntimeError("429")
    error.response = SimpleNamespace(headers={"retry-after": "soon"})  # type: ignore[attr-defined]

    assert GroqAdapter._retry_after(error) is None


def test_retry_raises_on_permanent_error() -> None:
    adapter = GroqAdapter(api_key="test", client=_Client(_Completions([])))

    def operation() -> str:
        raise RuntimeError("400 Bad Request")

    with pytest.raises(RuntimeError, match="400"):
        adapter._retry(operation, base_wait=0.0)
