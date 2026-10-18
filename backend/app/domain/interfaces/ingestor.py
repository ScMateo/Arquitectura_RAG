"""Ingestor port (IIngestor).

Implemented by CsvIngestor. Reads, cleans, normalizes and chunks the data
to produce the fragments to index.
"""

from collections.abc import Sequence
from typing import Protocol

from ..entities.chunk import Chunk


class IIngestor(Protocol):
    """Puerto de ingesta de datos CvLAC desde archivos CSV."""

    def ingest(self, csv_path: str) -> Sequence[Chunk]:
        """Procesa un CSV conforme al contrato y produce fragmentos.

        Args:
            csv_path: Ruta del archivo CSV.

        Returns:
            Fragmentos listos para indexar.
        """
        ...
