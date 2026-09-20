"""Domain exceptions (S: manejo de errores tipado, REGLAS_PROYECTO.md §6.3)."""


class DomainError(Exception):
    """Base para errores de dominio."""


class RetrievalError(DomainError):
    """No se encontraron documentos relevantes (HU-04/05)."""


class ConfigurationError(DomainError):
    """Falta configuración crítica (ej. GOOGLE_API_KEY)."""


class IngestionError(DomainError):
    """Fallo en cleaner/chunker/indexer."""
