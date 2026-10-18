"""LLM provider port (ILLMProvider).

Implemented by GeminiAdapter. Covers query analysis and generation,
including streaming.
"""

from collections.abc import Iterator
from typing import Protocol

from ..value_objects.query_analysis import QueryAnalysis


class ILLMProvider(Protocol):
    """Puerto de acceso al modelo de lenguaje."""

    def analyze_query(self, query: str) -> QueryAnalysis:
        """Analiza una consulta mediante salida estructurada (HU-04/05).

        Args:
            query: Consulta en lenguaje natural.

        Returns:
            Análisis con el tipo de consulta y, si aplica, el investigador.
        """
        ...

    def generate(self, prompt: str) -> str:
        """Genera una respuesta completa a partir de un prompt.

        Args:
            prompt: Prompt con instrucción, contexto e historial.

        Returns:
            Respuesta generada.
        """
        ...

    def stream(self, prompt: str) -> Iterator[str]:
        """Genera una respuesta de manera incremental.

        Args:
            prompt: Prompt con instrucción, contexto e historial.

        Yields:
            Porciones de la respuesta a medida que se generan.
        """
        ...
