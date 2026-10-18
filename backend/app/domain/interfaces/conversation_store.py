"""Conversation store port (IConversationStore).

Implemented by InMemoryConversationStore. Keeps session-scoped context (HU-07).
"""

from typing import Protocol

from ..entities.conversation import Conversation
from ..entities.message import Message


class IConversationStore(Protocol):
    """Puerto de almacenamiento del contexto conversacional por sesión."""

    def get(self, session_id: str) -> Conversation:
        """Obtiene la conversación de una sesión, creándola si no existe.

        Args:
            session_id: Identificador de la sesión.

        Returns:
            Conversación asociada.
        """
        ...

    def add_message(self, session_id: str, message: Message) -> None:
        """Registra un mensaje en la conversación de la sesión.

        Args:
            session_id: Identificador de la sesión.
            message: Mensaje a registrar.
        """
        ...

    def clear(self, session_id: str) -> None:
        """Elimina el contexto de la sesión.

        Args:
            session_id: Identificador de la sesión.
        """
        ...
