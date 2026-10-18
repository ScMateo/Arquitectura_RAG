"""Embedding provider port (IEmbeddingProvider).

Implemented by HuggingFaceAdapter. Applies the `query:` / `passage:`
prefixes required by the e5 family.
"""

from collections.abc import Sequence
from typing import Protocol


class IEmbeddingProvider(Protocol):
    """Puerto de generación de representaciones vectoriales."""

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        """Genera embeddings para documentos (prefijo `passage:`).

        Args:
            texts: Textos a representar.

        Returns:
            Lista de vectores, uno por texto.
        """
        ...

    def embed_query(self, text: str) -> list[float]:
        """Genera el embedding de una consulta (prefijo `query:`).

        Args:
            text: Texto de la consulta.

        Returns:
            Vector de la consulta.
        """
        ...
