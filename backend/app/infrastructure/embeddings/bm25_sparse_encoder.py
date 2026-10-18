"""BM25-style sparse encoder (implements ISparseEncoder).

Builds lexical sparse vectors as raw term frequencies keyed by a deterministic
32-bit hash of each token. IDF weighting is applied server-side by Qdrant's
`IDF` modifier, so the encoder only needs to produce term frequencies
(REQUISITOS_RECUPERACION.md RT-2).
"""

import re
import zlib
from collections import Counter
from collections.abc import Sequence

_TOKEN = re.compile(r"\w+", re.UNICODE)


class Bm25SparseEncoder:
    """Codifica texto en vectores sparse (frecuencia de términos)."""

    def encode_documents(self, texts: Sequence[str]) -> list[dict[int, float]]:
        """Genera vectores sparse para los documentos a indexar."""
        return [self._encode(text) for text in texts]

    def encode_query(self, text: str) -> dict[int, float]:
        """Genera el vector sparse de una consulta."""
        return self._encode(text)

    @staticmethod
    def _encode(text: str) -> dict[int, float]:
        tokens = _TOKEN.findall((text or "").lower())
        return {
            zlib.crc32(token.encode("utf-8")): float(count)
            for token, count in Counter(tokens).items()
        }
