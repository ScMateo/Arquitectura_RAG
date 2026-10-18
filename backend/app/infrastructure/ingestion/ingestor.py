"""CsvIngestor (implements IIngestor).

Reads a CSV conforming to the data contract and produces the chunks to index.
"""

import csv
import re
from collections.abc import Sequence

from ...domain.entities.chunk import Chunk
from ...domain.interfaces.chunker import IChunker
from ...domain.interfaces.normalizer import INormalizer
from ...domain.value_objects.cvlac_url import CvLACUrl
from ...domain.value_objects.section import Section
from .cleaner import Cleaner


class CsvIngestor:
    """Procesa un CSV CvLAC y produce los fragmentos listos para indexar."""

    _NAME_PATTERN = re.compile(
        r"Nombre\s+(.+?)(?:\s+(?:Nombre en citaciones|Nacionalidad|Sexo|INICIO))",
        re.IGNORECASE,
    )

    def __init__(
        self,
        cleaner: Cleaner,
        normalizer: INormalizer,
        chunker: IChunker,
    ) -> None:
        self._cleaner = cleaner
        self._normalizer = normalizer
        self._chunker = chunker

    def ingest(self, csv_path: str) -> Sequence[Chunk]:
        chunks: list[Chunk] = []

        with open(csv_path, encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter="|")
            for row in reader:
                chunks.extend(self._process_row(row))

        return chunks

    def _process_row(self, row: dict[str, str]) -> list[Chunk]:
        url = CvLACUrl((row.get("url_cvlac") or "").strip())
        sections = {
            section: (row.get(section.value) or "").strip()
            for section in Section
        }
        author = self._extract_name(sections[Section.IDENTIFICACION])

        chunks: list[Chunk] = []
        for section, raw_content in sections.items():
            cleaned = self._cleaner.clean(raw_content)
            normalized = self._normalizer.normalize(cleaned)
            if not normalized:
                continue
            for unit in self._chunker.chunk(section, normalized):
                chunks.append(
                    Chunk(
                        content=unit,
                        author=author,
                        section=section,
                        url=url,
                    )
                )
        return chunks

    def _extract_name(self, identificacion: str) -> str:
        match = self._NAME_PATTERN.search(identificacion)
        if match:
            return match.group(1).strip()
        return identificacion.strip() or "Investigador Desconocido"
