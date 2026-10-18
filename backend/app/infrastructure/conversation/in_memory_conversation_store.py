"""In-memory conversation store (implements IConversationStore).

Keeps session-scoped context with a bounded window (HU-07).
"""

from ...domain.entities.conversation import Conversation
from ...domain.entities.message import Message


class InMemoryConversationStore:
    """Almacena las conversaciones por sesión en memoria."""

    def __init__(self, max_history: int = 10) -> None:
        self._conversations: dict[str, Conversation] = {}
        self._max_history = max_history

    def get(self, session_id: str) -> Conversation:
        if session_id not in self._conversations:
            self._conversations[session_id] = Conversation(session_id=session_id)
        return self._conversations[session_id]

    def add_message(self, session_id: str, message: Message) -> None:
        conversation = self.get(session_id)
        conversation.messages.append(message)
        if len(conversation.messages) > self._max_history:
            conversation.messages = conversation.messages[-self._max_history :]

    def clear(self, session_id: str) -> None:
        self._conversations.pop(session_id, None)
