"""Query type value object for classification (HU-04 / HU-05)."""

from enum import StrEnum


class QueryType(StrEnum):
    """Tipo de consulta según su alcance.

    SPECIFIC se refiere a un investigador concreto; GENERAL a una temática.
    """

    SPECIFIC = "specific"
    GENERAL = "general"
