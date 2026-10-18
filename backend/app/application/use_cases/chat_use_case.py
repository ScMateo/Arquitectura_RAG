"""Chat use case: orchestrates retrieval, generation and conversation (HU-04/05/07/10)."""

from ...domain.entities.chunk import Chunk
from ...domain.entities.message import Message
from ...domain.interfaces.conversation_store import IConversationStore
from ...domain.value_objects.message_role import MessageRole
from ..dto.chat import ChatRequest, ChatResponse, SourceDTO
from ..services.generation_service import GenerationService
from ..services.retrieval_service import RetrievalService


class ChatUseCase:
    """Orquesta la recuperación y la generación con citación de fuentes."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
        generation_service: GenerationService,
        conversation_store: IConversationStore,
    ) -> None:
        self._retrieval_service = retrieval_service
        self._generation_service = generation_service
        self._conversation_store = conversation_store

    def execute(self, request: ChatRequest) -> ChatResponse:
        session_id = request.session_id or "default"
        history = self._conversation_store.get(session_id).messages

        chunks = self._retrieval_service.retrieve(request.message)
        answer = self._generation_service.generate(request.message, chunks, history)

        self._conversation_store.add_message(
            session_id, Message(role=MessageRole.USER, content=request.message)
        )
        self._conversation_store.add_message(
            session_id, Message(role=MessageRole.ASSISTANT, content=answer)
        )

        return ChatResponse(
            answer=answer,
            sources=[self._to_source_dto(chunk) for chunk in chunks],
        )

    @staticmethod
    def _to_source_dto(chunk: Chunk) -> SourceDTO:
        return SourceDTO(
            author=chunk.author,
            section=chunk.section.value,
            url=chunk.url.value,
            excerpt=chunk.content,
        )
