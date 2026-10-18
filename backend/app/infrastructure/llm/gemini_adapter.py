"""Gemini adapter (implements ILLMProvider).

Uses the google-genai client with a pinned model version. Includes structured
output for query analysis and retry with exponential backoff (METODOS_OPTIMIZACION.md).
"""

import time
from collections.abc import Iterator
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
        result = _QueryAnalysisSchema.model_validate_json(response.text)
        return QueryAnalysis(
            query_type=QueryType(result.type),
            researcher_name=result.researcher_name,
        )

    def generate(self, prompt: str) -> str:
        max_attempts = 3
        wait = 1.0
        for attempt in range(max_attempts):
            try:
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
            except Exception as exc:
                if not self._is_retryable(exc) or attempt == max_attempts - 1:
                    raise
                time.sleep(wait)
                wait *= 2
        raise RuntimeError("No se obtuvo respuesta del modelo.")

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

    @staticmethod
    def _is_retryable(exc: Exception) -> bool:
        return "503" in str(exc) or "429" in str(exc)
