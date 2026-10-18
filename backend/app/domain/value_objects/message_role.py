"""Message role value object for conversations (HU-07)."""

from enum import StrEnum


class MessageRole(StrEnum):
    """Rol del autor de un mensaje dentro de una conversación."""

    USER = "user"
    ASSISTANT = "assistant"
