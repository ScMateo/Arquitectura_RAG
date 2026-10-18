"""Sparse encoder port (ISparseEncoder).

Produces the lexical component of hybrid search (REQUISITOS_RECUPERACION.md
RT-2). A sparse vector maps token identifiers to weights; the identifier is
derived deterministically from the token, so indexing and querying agree
without needing to share a vocabulary between processes.
"""

from collections.abc import Sequence
from typing import Protocol


class ISparseEncoder(Protocol):
    """Puerto de codificación léxica dispersa."""

    def encode_documents(self, texts: Sequence[str]) -> list[dict[int, float]]:
        """Genera vectores sparse para los documentos a indexar.

        Args:
            texts: Textos de los fragmentos.

        Returns:
            Un vector sparse (índice -> peso) por texto.
        """
        ...

    def encode_query(self, text: str) -> dict[int, float]:
        """Genera el vector sparse de una consulta.

        Args:
            text: Texto de la consulta.

        Returns:
            Vector sparse (índice -> peso) de la consulta.
        """
        ...
