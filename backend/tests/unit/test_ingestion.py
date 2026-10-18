"""Unit tests for the ingestion pipeline (cleaner, chunker, normalizer, ingestor, indexer)."""

import csv
from collections.abc import Sequence

from app.domain.entities.chunk import Chunk
from app.domain.value_objects.section import Section
from app.infrastructure.ingestion.chunker import LogicalUnitChunker
from app.infrastructure.ingestion.cleaner import Cleaner
from app.infrastructure.ingestion.indexer import Indexer
from app.infrastructure.ingestion.ingestor import CsvIngestor
from app.infrastructure.ingestion.normalizer import AcronymNormalizer
from tests.helpers import FakeEmbeddingProvider, FakeVectorStore, make_chunk


def _write_csv(path, header: Sequence[str], rows: Sequence[Sequence[str]]) -> None:
    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter="|", quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        writer.writerows(rows)


def _build_ingestor() -> CsvIngestor:
    return CsvIngestor(Cleaner(), AcronymNormalizer(), LogicalUnitChunker())


# --- Cleaner ---


def test_cleaner_unescapes_entities_and_strips_control_chars() -> None:
    assert Cleaner().clean('Hola &amp; mundo\n"x"\t') == "Hola & mundo x"


def test_cleaner_collapses_whitespace() -> None:
    assert Cleaner().clean("a   b\n\nc") == "a b c"


# --- Chunker ---


def test_chunker_combines_small_sentences() -> None:
    result = LogicalUnitChunker(max_chunk_size=1000).chunk(Section.ARTICULOS, "Uno. Dos. Tres.")
    assert result == ["Uno. Dos. Tres."]


def test_chunker_splits_when_exceeding_max_size() -> None:
    result = LogicalUnitChunker(max_chunk_size=10).chunk(
        Section.ARTICULOS, "aaaaaa. bbbbbb. cccccc."
    )
    assert len(result) == 3
    assert all(len(chunk) <= 10 for chunk in result)


# --- Normalizer (HU-09) ---


def test_normalizer_applies_mapping_case_insensitive() -> None:
    normalizer = AcronymNormalizer({"UNAL": "Universidad Nacional de Colombia"})
    assert normalizer.normalize("trabaja en UNAL desde 2020") == (
        "trabaja en Universidad Nacional de Colombia desde 2020"
    )


def test_normalizer_without_mapping_is_noop() -> None:
    text = "texto sin acronimos"
    assert AcronymNormalizer().normalize(text) == text


def test_normalizer_respects_word_boundaries() -> None:
    normalizer = AcronymNormalizer({"IA": "Inteligencia Artificial"})
    assert normalizer.normalize("media") == "media"


# --- CsvIngestor ---


def test_csv_ingestor_produces_chunks_with_metadata(tmp_path) -> None:
    path = tmp_path / "investigadores.csv"
    _write_csv(
        path,
        ["identificacion", "articulos", "url_cvlac"],
        [
            [
                "Nombre Juan Perez Nacionalidad Colombiana Sexo Masculino",
                "Uno. Dos.",
                "https://example.org/cv/1",
            ]
        ],
    )

    chunks = _build_ingestor().ingest(str(path))

    assert {chunk.section for chunk in chunks} == {
        Section.IDENTIFICACION,
        Section.ARTICULOS,
    }
    article = next(chunk for chunk in chunks if chunk.section is Section.ARTICULOS)
    assert article.author == "Juan Perez"
    assert article.url.value == "https://example.org/cv/1"
    assert article.content == "Uno. Dos."


def test_csv_ingestor_handles_missing_trailing_fields(tmp_path) -> None:
    path = tmp_path / "trailing.csv"
    _write_csv(
        path,
        ["identificacion", "articulos", "url_cvlac", "software"],
        [
            [
                "Nombre Ana Gomez Nacionalidad Colombiana Sexo Femenino",
                "Solo.",
                "https://example.org/cv/2",
            ]
        ],
    )

    chunks = _build_ingestor().ingest(str(path))

    assert Section.SOFTWARE not in {chunk.section for chunk in chunks}
    assert any(chunk.section is Section.ARTICULOS for chunk in chunks)


# --- Indexer ---


class _StubIngestor:
    def ingest(self, csv_path: str) -> Sequence[Chunk]:
        return [make_chunk(content="a"), make_chunk(content="bb")]


def test_indexer_embeds_and_stores() -> None:
    embeddings = FakeEmbeddingProvider()
    vector_store = FakeVectorStore()
    indexer = Indexer(_StubIngestor(), embeddings, vector_store)

    indexer.index("cualquier.csv")

    assert len(vector_store.added_chunks) == 2
    assert len(vector_store.added_vectors) == 2
    assert embeddings.document_calls == [["a", "bb"]]
