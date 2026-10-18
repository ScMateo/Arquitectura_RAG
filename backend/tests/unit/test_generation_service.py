"""Unit tests for GenerationService (prompt composition)."""

from app.application.services.generation_service import GenerationService
from app.domain.entities.message import Message
from app.domain.value_objects.message_role import MessageRole
from tests.helpers import FakeLLMProvider, make_chunk


def test_generate_includes_context_history_and_question() -> None:
    llm = FakeLLMProvider(answer="ok")
    service = GenerationService(llm)
    history = [Message(role=MessageRole.USER, content="hola")]

    result = service.generate("¿quien?", [make_chunk(content="CONTEXTO_UNO")], history)

    assert result == "ok"
    prompt = llm.prompts[0]
    assert "CONTEXTO_UNO" in prompt
    assert "PREGUNTA: ¿quien?" in prompt
    assert "user: hola" in prompt


def test_generate_without_context_still_builds_prompt() -> None:
    llm = FakeLLMProvider()
    GenerationService(llm).generate("q", [], [])
    assert "PREGUNTA: q" in llm.prompts[0]
    assert "CONTEXTO:\n\n" in llm.prompts[0]
