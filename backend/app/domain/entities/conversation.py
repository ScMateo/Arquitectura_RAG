"""Conversation entity: session-scoped context (HU-07)."""

from dataclasses import dataclass, field

from .message import Message


@dataclass
class Conversation:
    """Conversación asociada a una sesión.

    Attributes:
        session_id: Identificador único de la sesión.
        messages: Mensajes intercambiados en orden cronológico.
    """

    session_id: str
    messages: list[Message] = field(default_factory=list)
