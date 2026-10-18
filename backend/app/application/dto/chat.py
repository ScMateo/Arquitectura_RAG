"""Chat DTOs: contracts for the chat endpoint."""

from typing import Literal

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


class ChatStreamEvent(BaseModel):
    """Evento del flujo incremental de respuesta (METODOS_OPTIMIZACION.md: streaming).

    Attributes:
        type: Tipo de evento: `token`, `sources` o `done`.
        content: Porción de texto cuando el evento es `token`.
        sources: Fuentes citadas cuando el evento es `sources`.
    """

    type: Literal["token", "sources", "done"]
    content: str | None = None
    sources: list[SourceDTO] | None = None
