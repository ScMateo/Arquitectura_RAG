"""Embedding adapters."""

from .bm25_sparse_encoder import Bm25SparseEncoder
from .huggingface_adapter import HuggingFaceAdapter

__all__ = ["Bm25SparseEncoder", "HuggingFaceAdapter"]
