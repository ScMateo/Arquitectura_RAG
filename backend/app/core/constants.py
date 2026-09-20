"""Constants centralizadas (S: evita números mágicos).

Referencia REGLAS_PROYECTO.md §6.2 y HU-07-4.
"""

# HU-07 Criterio 4: historial conversacional mínimo 10
MAX_HISTORY = 10

# Ingestion strategy (migrado de src/ingest_academico.py:22)
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 500

# Prioridad de secciones CvLAC para re-ranking (HE.003)
# Menor valor = mayor prioridad en prompt
SECTION_PRIORITY: dict[str, int] = {
    "formacion_academica": 1,
    "experiencia_profesional": 2,
    "proyectos": 3,
    "produccion_bibliografica": 4,
    "trabajos_dirigidos": 5,
}
