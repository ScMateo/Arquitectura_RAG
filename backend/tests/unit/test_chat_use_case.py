"""Unit tests for ChatUseCase (orchestration + conversation memory, HU-07/10)."""

from app.application.dto.chat import ChatRequest
from app.application.services.generation_service import GenerationService
from app.application.services.retrieval_service import RetrievalService
from app.application.use_cases.chat_use_case import ChatUseCase
from app.domain.value_objects.message_role import MessageRole
from app.domain.value_objects.query_analysis import QueryAnalysis
from app.domain.value_objects.query_type import QueryType
from app.domain.value_objects.section import Section
from app.infrastructure.conversation.in_memory_conversation_store import (
    InMemoryConversationStore,
)
from app.infrastructure.reranking.weighted_reranker import WeightedReranker
from tests.helpers import (
    FakeEmbeddingProvider,
    FakeLLMProvider,
    FakeVectorStore,
    make_chunk,
)


class _NoopNormalizer:
    def normalize(self, text: str) -> str:
        return text


def _build_use_case(
    llm: FakeLLMProvider | None = None,
    store: InMemoryConversationStore | None = None,
) -> tuple[ChatUseCase, InMemoryConversationStore, FakeLLMProvider]:
    llm = llm or FakeLLMProvider(
        analysis=QueryAnalysis(query_type=QueryType.GENERAL), answer="respuesta"
    )
    store = store or InMemoryConversationStore()
    vector_store = FakeVectorStore(results=[make_chunk(content="c", section=Section.ARTICULOS)])
    retrieval = RetrievalService(
        normalizer=_NoopNormalizer(),
        llm_provider=llm,
        embedding_provider=FakeEmbeddingProvider(),
        vector_store=vector_store,
        reranker=WeightedReranker(),
    )
    generation = GenerationService(llm)
    return ChatUseCase(retrieval, generation, store), store, llm


def test_execute_returns_answer_and_sources() -> None:
    use_case, _, _ = _build_use_case()
    response = use_case.execute(ChatRequest(message="hola"))
    assert response.answer == "respuesta"
    assert len(response.sources) == 1
    assert response.sources[0].author == "Autor Uno"
    assert response.sources[0].url.startswith("https://")


def test_execute_records_user_and_assistant_messages() -> None:
    use_case, store, _ = _build_use_case()
    use_case.execute(ChatRequest(message="pregunta uno", session_id="abc"))

    messages = store.get("abc").messages
    assert [message.role for message in messages] == [
        MessageRole.USER,
        MessageRole.ASSISTANT,
    ]
    assert messages[0].content == "pregunta uno"
    assert messages[1].content == "respuesta"


def test_execute_uses_default_session_when_absent() -> None:
    use_case, store, _ = _build_use_case()
    use_case.execute(ChatRequest(message="x"))
    assert store.get("default").messages


def test_second_turn_includes_previous_history_in_prompt() -> None:
    use_case, _, llm = _build_use_case()
    use_case.execute(ChatRequest(message="primer turno", session_id="s"))
    use_case.execute(ChatRequest(message="segundo turno", session_id="s"))
    assert "primer turno" in llm.prompts[-1]


def test_execute_stream_emits_tokens_sources_and_done() -> None:
    use_case, store, _ = _build_use_case()

    events = list(use_case.execute_stream(ChatRequest(message="hola", session_id="s")))

    assert [event.type for event in events] == ["token", "sources", "done"]
    assert events[0].content == "respuesta"
    assert events[1].sources is not None
    assert events[1].sources[0].author == "Autor Uno"
    assert [message.role for message in store.get("s").messages] == [
        MessageRole.USER,
        MessageRole.ASSISTANT,
    ]
