"""Unit tests for the LLM provider factory (no network calls)."""

import pytest

from app.core.config import Settings
from app.infrastructure.llm import GeminiAdapter, GroqAdapter, build_llm_provider


def _settings(**overrides: object) -> Settings:
    base: dict[str, object] = {
        "LLM_PROVIDER": "gemini",
        "GOOGLE_API_KEY": "google-test",
        "GROQ_API_KEY": "groq-test",
    }
    base.update(overrides)
    return Settings(**base)  # type: ignore[arg-type]


def test_factory_builds_gemini_by_default() -> None:
    assert isinstance(build_llm_provider(_settings()), GeminiAdapter)


def test_factory_builds_groq_when_selected() -> None:
    assert isinstance(build_llm_provider(_settings(LLM_PROVIDER="groq")), GroqAdapter)


def test_factory_rejects_missing_groq_key() -> None:
    settings = _settings(LLM_PROVIDER="groq", GROQ_API_KEY=None)

    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        build_llm_provider(settings)


def test_factory_rejects_missing_google_key() -> None:
    settings = _settings(LLM_PROVIDER="gemini", GOOGLE_API_KEY=None)

    with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
        build_llm_provider(settings)
