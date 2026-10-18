"""Domain layer: entities, value objects and ports (interfaces).

This layer holds no infrastructure dependencies; infrastructure implements
the interfaces defined here (DIP).
"""

from .entities import Chunk, Conversation, Message, Researcher, Source
from .value_objects import CvLACUrl, MessageRole, QueryType, Section

__all__ = [
    "Chunk",
    "Conversation",
    "CvLACUrl",
    "Message",
    "MessageRole",
    "QueryType",
    "Researcher",
    "Section",
    "Source",
]
