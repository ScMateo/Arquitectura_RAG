"""Chat endpoint (POST /api/chat)."""

from typing import Annotated

from fastapi import APIRouter, Depends

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
