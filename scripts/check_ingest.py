import csv

from app.infrastructure.ingestion import (
    AcronymNormalizer,
    Cleaner,
    CsvIngestor,
    LogicalUnitChunker,
)

CSV_PATH = "/tmp/sample_cvlac.csv"

header = [
    "identificacion", "url_cvlac", "formacion_academica", "experiencia_profesional",
    "articulos", "proyectos", "identificadores_autor", "software",
    "productos_tecnologicos", "formacion_complementaria", "trabajos_dirigidos",
    "evento_cientifico", "libros", "capitulos_libro", "procesos_tecnicas",
    "asesorias", "redes_conocimiento", "patentes", "insumos_politica",
    "desarrollos_web", "manuales_guias", "redes_sociales", "par_evaluador",
]

row = [
    "Nombre Allan Andrew Wood Nacionalidad Colombiana Sexo Masculino",
    "https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=1",
    "Doctorado Imperial College Agricultural Economics Octubre de 2004. Maestria en Estudios Amazonicos",
    "Profesor Universidad Nacional de Colombia",
    "Articulo sobre produccion agricola en la Amazonia. Articulo sobre seguridad alimentaria",
    "Produccion agricola local y seguridad alimentaria",
    "ORCID 0000-0000-0000-0000",
    "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
]

with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f, delimiter="|", quoting=csv.QUOTE_ALL)
    writer.writerow(header)
    writer.writerow(row)

normalizer = AcronymNormalizer({"U.Nal": "Universidad Nacional de Colombia"})
ingestor = CsvIngestor(
    cleaner=Cleaner(),
    normalizer=normalizer,
    chunker=LogicalUnitChunker(max_chunk_size=1500),
)

chunks = ingestor.ingest(CSV_PATH)
print(f"chunks generados: {len(chunks)}")
for chunk in chunks:
    print(f"- [{chunk.section.value}] {chunk.author}: {chunk.content[:60]}...")
