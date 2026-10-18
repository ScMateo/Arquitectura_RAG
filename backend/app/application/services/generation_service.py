"""Generation service: composes the prompt and invokes the LLM."""

from ...domain.entities.chunk import Chunk
from ...domain.entities.message import Message
from ...domain.interfaces.llm_provider import ILLMProvider

_SYSTEM_INSTRUCTION = (
    "Eres un analista académico que responde preguntas sobre hojas de vida "
    "CvLAC. Basa tu respuesta exclusivamente en el contexto proporcionado y "
    "no uses conocimiento previo. Si la información no es suficiente para "
    "responder, indícalo explícitamente."
)


class GenerationService:
    """Compone el prompt y genera la respuesta a partir del contexto."""

    def __init__(
        self,
        llm_provider: ILLMProvider,
        system_instruction: str = _SYSTEM_INSTRUCTION,
    ) -> None:
        self._llm_provider = llm_provider
        self._system_instruction = system_instruction

    def generate(
        self,
        query: str,
        context: list[Chunk],
        history: list[Message],
    ) -> str:
        prompt = self._build_prompt(query, context, history)
        return self._llm_provider.generate(prompt)

    def _build_prompt(
        self,
        query: str,
        context: list[Chunk],
        history: list[Message],
    ) -> str:
        context_text = "\n---\n".join(chunk.content for chunk in context)
        history_text = "\n".join(
            f"{message.role.value}: {message.content}" for message in history
        )
        return (
            f"{self._system_instruction}\n\n"
            f"CONTEXTO:\n{context_text}\n\n"
            f"HISTORIAL:\n{history_text}\n\n"
            f"PREGUNTA: {query}\n"
            "Respuesta:"
        )
