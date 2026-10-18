"""Normalizer port (INormalizer).

Implemented by AcronymNormalizer. Resolves acronyms using evidence-based
mapping (HU-09).
"""

from typing import Protocol


class INormalizer(Protocol):
    """Puerto de normalización de texto y acrónimos."""

    def normalize(self, text: str) -> str:
        """Normaliza acrónimos y variantes de denominación en un texto.

        Args:
            text: Texto a normalizar.

        Returns:
            Texto normalizado.
        """
        ...
