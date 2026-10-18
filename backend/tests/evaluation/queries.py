"""Test query set: puntuales, generales, relacionales y comparativas.

Structure for the 20 queries defined in the requirements document (p.7). Each
entry declares the question, its category and the researchers that a correct
retrieval must surface (``expected_authors``), which is the ground truth used
to compute recall@k and MRR.

NOTE: the entries below are placeholders aligned with the sample corpus
(data/sample/investigadores.csv). Replace/extend them with the 20 real queries
so the evaluation reflects the thesis dataset.
"""

from dataclasses import dataclass, field
from enum import StrEnum


class QueryCategory(StrEnum):
    """Categoría de la consulta según el documento de requisitos."""

    PUNTUAL = "puntual"
    GENERAL = "general"
    RELACIONAL = "relacional"
    COMPARATIVA = "comparativa"


@dataclass(frozen=True)
class EvaluationQuery:
    """Consulta de evaluación con su verdad de referencia."""

    category: QueryCategory
    question: str
    expected_authors: tuple[str, ...] = field(default_factory=tuple)


EVALUATION_QUERIES: list[EvaluationQuery] = [
    EvaluationQuery(
        QueryCategory.PUNTUAL,
        "¿Cuál es la formación académica de Carlos Andres Perez?",
        ("Carlos Andres Perez",),
    ),
    EvaluationQuery(
        QueryCategory.PUNTUAL,
        "¿Dónde trabaja actualmente Allan Andrew Wood?",
        ("Allan Andrew Wood",),
    ),
    EvaluationQuery(
        QueryCategory.GENERAL,
        "¿Quién ha investigado sobre salud pública?",
        ("Maria Camila Rodriguez",),
    ),
    EvaluationQuery(
        QueryCategory.RELACIONAL,
        "¿Qué proyectos tiene Maria Camila Rodriguez?",
        ("Maria Camila Rodriguez",),
    ),
    EvaluationQuery(
        QueryCategory.COMPARATIVA,
        "¿Quién tiene mayor formación académica, Carlos Andres Perez o Maria Camila Rodriguez?",
        ("Carlos Andres Perez", "Maria Camila Rodriguez"),
    ),
]
