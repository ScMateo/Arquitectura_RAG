"""Chat endpoints (POST /api/chat, POST /api/chat/stream)."""

from collections.abc import Iterator
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.api.dependencies import get_chat_use_case
from app.application.dto.chat import ChatRequest, ChatResponse
from app.application.use_cases.chat_use_case import ChatUseCase

router = APIRouter()


@router.post("/api/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    use_case: Annotated[ChatUseCase, Depends(get_chat_use_case)],
) -> ChatResponse:
    return use_case.execute(request)


@router.post("/api/chat/stream")
async def chat_stream(
    request: ChatRequest,
    use_case: Annotated[ChatUseCase, Depends(get_chat_use_case)],
) -> StreamingResponse:
    def event_stream() -> Iterator[str]:
        for event in use_case.execute_stream(request):
            yield f"data: {event.model_dump_json()}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
