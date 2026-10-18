"""Chat DTOs: contracts for the chat endpoint."""

from pydantic import BaseModel


class SourceDTO(BaseModel):
    """Fuente citada en la respuesta (HU-10)."""

    author: str
    section: str
    url: str
    excerpt: str


class ChatRequest(BaseModel):
    """Petición de chat."""

    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    """Respuesta de chat con sus fuentes."""

    answer: str
    sources: list[SourceDTO]
