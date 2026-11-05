"""Groq adapter (implements ILLMProvider).

Uses the official Groq SDK over its OpenAI-compatible chat completions API.
Structured output is requested in JSON mode and validated with Pydantic, so the
adapter works with any Groq-hosted model (gpt-oss, qwen, ...). Retries with
exponential backoff are applied to transient errors, mirroring the Gemini
adapter (METODOS_OPTIMIZACION.md).
"""

from __future__ import annotations

import time
from collections.abc import Callable, Iterator
from typing import Any, Literal, TypeVar

from groq import Groq
from pydantic import BaseModel, Field

from ...domain.value_objects.query_analysis import QueryAnalysis
from ...domain.value_objects.query_type import QueryType

_T = TypeVar("_T")

_ANALYSIS_PROMPT = """Analiza la siguiente consulta sobre hojas de vida CvLAC.
Determina el tipo: "specific" si menciona a uno o más investigadores por su
nombre, o "general" si es una consulta temática.
Responde EXCLUSIVAMENTE un objeto JSON con estas claves:
- "type": "specific" o "general".
- "researcher_names": lista con los nombres de todos los investigadores
  mencionados (lista vacía si el tipo es "general").

Consulta: {query}"""


class _QueryAnalysisSchema(BaseModel):
    """Esquema de salida estructurada para el análisis de consultas."""

    type: Literal["specific", "general"]
    researcher_names: list[str] = Field(default_factory=list)


class GroqAdapter:
    """Accede a un modelo servido por Groq para analizar y generar respuestas."""

    def __init__(
        self,
        api_key: str,
        model: str = "openai/gpt-oss-120b",
        timeout_ms: int = 60000,
        analysis_temperature: float = 0.0,
        generation_temperature: float = 0.5,
        client: Any | None = None,
    ) -> None:
        self._client = client if client is not None else Groq(
            api_key=api_key,
            timeout=timeout_ms / 1000,
            max_retries=0,
        )
        self._model = model
        self._analysis_temperature = analysis_temperature
        self._generation_temperature = generation_temperature

    def analyze_query(self, query: str) -> QueryAnalysis:
        prompt = _ANALYSIS_PROMPT.format(query=query)

        def request_analysis() -> str:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
                temperature=self._analysis_temperature,
            )
            content = response.choices[0].message.content
            if not content:
                raise ValueError("El modelo no devolvió un análisis estructurado.")
            return content

        raw = self._retry(request_analysis)
        result = _QueryAnalysisSchema.model_validate_json(raw)
        return QueryAnalysis(
            query_type=QueryType(result.type),
            researcher_names=tuple(result.researcher_names),
        )

    def generate(self, prompt: str) -> str:
        def request_generation() -> str:
            response = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self._generation_temperature,
            )
            content = response.choices[0].message.content
            if not content:
                raise RuntimeError("El modelo no devolvió respuesta.")
            return content

        return self._retry(request_generation)

    def stream(self, prompt: str) -> Iterator[str]:
        response = self._retry(lambda: self._open_stream(prompt))
        for chunk in response:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    def _open_stream(self, prompt: str) -> Any:
        return self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self._generation_temperature,
            stream=True,
        )

    def _retry(
        self,
        operation: Callable[[], _T],
        max_attempts: int = 4,
        base_wait: float = 2.0,
        sleep: Callable[[float], None] = time.sleep,
    ) -> _T:
        """Ejecuta una operación con reintentos ante errores transitorios.

        Si el proveedor informa ``Retry-After``, se respeta ese valor en lugar
        del retroceso exponencial (útil para los límites por minuto de Groq).
        """
        wait = base_wait
        for attempt in range(max_attempts):
            try:
                return operation()
            except Exception as exc:
                if not self._is_retryable(exc) or attempt == max_attempts - 1:
                    raise
                delay = self._retry_after(exc)
                if delay is None:
                    delay = wait
                    wait *= 2
                sleep(delay)
        raise RuntimeError("No se obtuvo respuesta del modelo.")

    @staticmethod
    def _retry_after(exc: Exception) -> float | None:
        """Lee el header ``Retry-After`` de la respuesta del proveedor."""
        response = getattr(exc, "response", None)
        headers = getattr(response, "headers", None)
        if headers is None:
            return None
        raw = headers.get("retry-after")
        if raw is None:
            return None
        try:
            return max(float(raw), 0.0)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _is_retryable(exc: Exception) -> bool:
        status = getattr(exc, "status_code", None)
        if status in {408, 409, 429, 500, 502, 503, 504}:
            return True
        message = str(exc).lower()
        transient = (
            "429",
            "500",
            "502",
            "503",
            "504",
            "rate limit",
            "unavailable",
            "timeout",
            "timed out",
            "deadline",
            "connection error",
        )
        return any(token in message for token in transient)
