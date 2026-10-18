"""Retrieval metrics (PLAN_VALIDACION.md §6.1).

All metrics operate on a ranked list of binary relevance flags (True when the
retrieved chunk is relevant) plus the total number of relevant chunks that
exist in the corpus for the case.
"""

from __future__ import annotations

import math
from collections.abc import Sequence


def precision_at_k(relevance: Sequence[bool], k: int) -> float:
    """Proporción de fragmentos relevantes entre los K primeros."""
    top = relevance[:k]
    if not top:
        return 0.0
    return sum(top) / len(top)


def recall_at_k(relevance: Sequence[bool], k: int, total_relevant: int) -> float:
    """Proporción de fragmentos relevantes recuperados del total existente."""
    if total_relevant <= 0:
        return 0.0
    return min(sum(relevance[:k]), total_relevant) / total_relevant


def mrr_at_k(relevance: Sequence[bool], k: int) -> float:
    """Inverso de la posición del primer fragmento relevante."""
    for position, relevant in enumerate(relevance[:k], start=1):
        if relevant:
            return 1.0 / position
    return 0.0


def ndcg_at_k(relevance: Sequence[bool], k: int, total_relevant: int) -> float:
    """nDCG con relevancia binaria y descuento logarítmico por posición."""
    dcg = sum(
        1.0 / math.log2(position + 1)
        for position, relevant in enumerate(relevance[:k], start=1)
        if relevant
    )
    ideal_hits = min(total_relevant, k)
    idcg = sum(1.0 / math.log2(position + 1) for position in range(1, ideal_hits + 1))
    if idcg == 0:
        return 0.0
    return min(dcg / idcg, 1.0)


def mean(values: Sequence[float]) -> float:
    """Media aritmética; 0.0 si la secuencia está vacía."""
    return sum(values) / len(values) if values else 0.0


def percentile(values: Sequence[float], ratio: float) -> float:
    """Percentil por rango más cercano (0.0 <= ratio <= 1.0)."""
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(round(ratio * (len(ordered) - 1)), len(ordered) - 1)
    return ordered[index]
