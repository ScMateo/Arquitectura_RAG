"""Acronym normalizer (implements INormalizer).

Resolves acronyms and equivalent denominations using an evidence-based
mapping (HU-09). The mapping is injected, so it is derived from the corpus
rather than hardcoded.
"""

import re


class AcronymNormalizer:
    """Normaliza acrónimos mediante un mapeo basado en evidencia."""

    def __init__(self, mapping: dict[str, str] | None = None) -> None:
        self._patterns = {
            re.compile(rf"\b{re.escape(acronym)}\b", re.IGNORECASE): full_name
            for acronym, full_name in (mapping or {}).items()
        }

    def normalize(self, text: str) -> str:
        result = text
        for pattern, replacement in self._patterns.items():
            result = pattern.sub(replacement, result)
        return result
