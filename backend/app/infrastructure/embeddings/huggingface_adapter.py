"""HuggingFace embeddings adapter (implements IEmbeddingProvider).

Uses sentence-transformers with the e5 family. Applies the `query:` and
`passage:` prefixes required for optimal performance (ESTRATEGIA_SEGMENTACION_EMBEDDINGS.md).
"""

from collections.abc import Sequence

from sentence_transformers import SentenceTransformer


class HuggingFaceAdapter:
    """Genera embeddings con sentence-transformers en el dispositivo indicado."""

    _QUERY_PREFIX = "query: "
    _PASSAGE_PREFIX = "passage: "

    def __init__(self, model_name: str, device: str = "cpu") -> None:
        self._model = SentenceTransformer(model_name, device=device)

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        prefixed = [self._PASSAGE_PREFIX + text for text in texts]
        vectors = self._model.encode(prefixed, normalize_embeddings=True)
        return [vector.tolist() for vector in vectors]

    def embed_query(self, text: str) -> list[float]:
        vector = self._model.encode(
            self._QUERY_PREFIX + text,
            normalize_embeddings=True,
        )
        return vector.tolist()
