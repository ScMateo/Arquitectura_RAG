"""Query analysis value object (HU-04 / HU-05 classification)."""

from dataclasses import dataclass

from .query_type import QueryType


@dataclass(frozen=True)
class QueryAnalysis:
    """Resultado del análisis de una consulta.

    Attributes:
        query_type: Tipo de consulta (específica o general).
        researcher_name: Nombre del investigador si la consulta es específica.
    """

    query_type: QueryType
    researcher_name: str | None = None
