"""Gemini adapter (implements ILLMProvider).

Uses the google-genai client with a pinned model version. Includes structured
output for query analysis and retry with exponential backoff (METODOS_OPTIMIZACION.md).
"""

import time
from collections.abc import Callable, Iterator
from typing import Literal

from google import genai
from google.genai import types
from pydantic import BaseModel

from ...domain.value_objects.query_analysis import QueryAnalysis
from ...domain.value_objects.query_type import QueryType


class _QueryAnalysisSchema(BaseModel):
    """Esquema de salida estructurada para el análisis de consultas."""

    type: Literal["specific", "general"]
    researcher_name: str | None = None


class GeminiAdapter:
    """Accede al modelo Gemini para analizar y generar respuestas."""

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-3.8-flash",
        timeout_ms: int = 60000,
        analysis_temperature: float = 0.0,
        generation_temperature: float = 0.5,
    ) -> None:
        self._client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=timeout_ms),
        )
        self._model = model
        self._analysis_temperature = analysis_temperature
        self._generation_temperature = generation_temperature

    def analyze_query(self, query: str) -> QueryAnalysis:
        prompt = (
            "Analiza la siguiente consulta sobre hojas de vida CvLAC.\n"
            "Determina el tipo: 'specific' si menciona a un investigador "
            "específico por su nombre, o 'general' si es una consulta "
            "temática o general.\n"
            "Si el tipo es 'specific', indica el nombre del investigador "
            "en researcher_name.\n\n"
            f"Consulta: {query}"
        )

        def request_analysis() -> str:
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=_QueryAnalysisSchema,
                    temperature=self._analysis_temperature,
                ),
            )
            if response.text is None:
                raise ValueError("El modelo no devolvió un análisis estructurado.")
            return response.text

        raw = self._retry(request_analysis)
        result = _QueryAnalysisSchema.model_validate_json(raw)
        return QueryAnalysis(
            query_type=QueryType(result.type),
            researcher_name=result.researcher_name,
        )

    def generate(self, prompt: str) -> str:
        def request_generation() -> str:
            response = self._client.models.generate_content(
                model=self._model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=self._generation_temperature,
                ),
            )
            if response.text is None:
                raise RuntimeError("El modelo no devolvió respuesta.")
            return response.text

        return self._retry(request_generation)

    def stream(self, prompt: str) -> Iterator[str]:
        for chunk in self._client.models.generate_content_stream(
            model=self._model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=self._generation_temperature,
            ),
        ):
            if chunk.text:
                yield chunk.text

    def _retry(
        self,
        operation: Callable[[], str],
        max_attempts: int = 3,
        base_wait: float = 2.0,
    ) -> str:
        """Ejecuta una operación con reintentos ante errores transitorios."""
        wait = base_wait
        for attempt in range(max_attempts):
            try:
                return operation()
            except Exception as exc:
                if not self._is_retryable(exc) or attempt == max_attempts - 1:
                    raise
                time.sleep(wait)
                wait *= 2
        raise RuntimeError("No se obtuvo respuesta del modelo.")

    @staticmethod
    def _is_retryable(exc: Exception) -> bool:
        message = str(exc).lower()
        transient = ("503", "429", "unavailable", "timeout", "timed out", "deadline")
        return any(token in message for token in transient)
