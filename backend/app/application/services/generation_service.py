"""Generation service: composes the prompt and invokes the LLM."""

from collections.abc import Iterator

from ...domain.entities.chunk import Chunk
from ...domain.entities.message import Message
from ...domain.interfaces.llm_provider import ILLMProvider

_SYSTEM_INSTRUCTION = (
    "Eres un analista académico que responde preguntas sobre hojas de vida "
    "CvLAC. Responde usando exclusivamente el contexto proporcionado y no uses "
    "conocimiento externo. Si el contexto contiene información relacionada con "
    "la pregunta, responde de forma concreta e indica el investigador y la "
    "sección de donde proviene. Declara que la información es insuficiente "
    "únicamente si el contexto está vacío o no guarda relación con la pregunta."
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

    def generate_stream(
        self,
        query: str,
        context: list[Chunk],
        history: list[Message],
    ) -> Iterator[str]:
        """Genera la respuesta de forma incremental (streaming)."""
        prompt = self._build_prompt(query, context, history)
        yield from self._llm_provider.stream(prompt)

    def _build_prompt(
        self,
        query: str,
        context: list[Chunk],
        history: list[Message],
    ) -> str:
        context_text = self._format_context(context)
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

    @staticmethod
    def _format_context(context: list[Chunk]) -> str:
        return "\n".join(
            f"[{index}] (Investigador: {chunk.author} | "
            f"Sección: {chunk.section.value})\n{chunk.content}"
            for index, chunk in enumerate(context, start=1)
        )
