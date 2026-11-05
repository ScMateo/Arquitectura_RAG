"""Query analysis value object (HU-04 / HU-05 classification)."""

from dataclasses import dataclass

from .query_type import QueryType


@dataclass(frozen=True)
class QueryAnalysis:
    """Resultado del análisis de una consulta.

    Attributes:
        query_type: Tipo de consulta (específica o general).
        researcher_names: Nombres de los investigadores mencionados cuando la
            consulta es específica; puede ser más de uno en consultas
            comparativas (p. ej. "¿quién tiene más artículos, X o Y?").
    """

    query_type: QueryType
    researcher_names: tuple[str, ...] = ()

    @property
    def researcher_name(self) -> str | None:
        """Primer investigador, o None si la consulta no nombra a ninguno."""
        return self.researcher_names[0] if self.researcher_names else None
