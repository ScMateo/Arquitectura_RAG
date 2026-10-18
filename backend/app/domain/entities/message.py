"""Message entity for conversations (HU-07)."""

from dataclasses import dataclass

from ..value_objects.message_role import MessageRole


@dataclass(frozen=True)
class Message:
    """Mensaje de una conversación.

    Attributes:
        role: Rol del autor del mensaje.
        content: Contenido del mensaje.
    """

    role: MessageRole
    content: str
