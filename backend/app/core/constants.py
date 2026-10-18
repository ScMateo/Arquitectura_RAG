"""Constants centralizadas (S: evita números mágicos).

Referencia REGLAS_PROYECTO.md §6.2 y HU-07-4.
"""

# HU-07 Criterio 4: historial mínimo de 5 interacciones; se adopta 10 por margen.
MAX_HISTORY = 10

# Límite máximo de tamaño de una unidad lógica (fallback de segmentación).
CHUNK_SIZE = 1500

# Prioridad de secciones CvLAC para re-ranking (REQUISITOS_RECUPERACION.md).
# Menor valor = mayor prioridad en el contexto enviado al modelo.
SECTION_PRIORITY: dict[str, int] = {
    "identificacion": 1,
    "formacion_academica": 1,
    "experiencia_profesional": 1,
    "articulos": 1,
    "proyectos": 1,
    "identificadores_autor": 2,
    "software": 2,
    "productos_tecnologicos": 2,
    "formacion_complementaria": 3,
    "trabajos_dirigidos": 3,
    "evento_cientifico": 3,
    "libros": 3,
    "capitulos_libro": 3,
    "procesos_tecnicas": 3,
    "asesorias": 4,
    "redes_conocimiento": 4,
    "patentes": 4,
    "insumos_politica": 4,
    "desarrollos_web": 4,
    "manuales_guias": 4,
    "redes_sociales": 5,
    "par_evaluador": 5,
}

# Palabras clave que indican la sección solicitada por una consulta específica,
# en orden de especificidad (las frases más largas primero). Permiten que el
# re-ranking priorice la sección realmente preguntada (REQUISITOS_RECUPERACION.md).
SECTION_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "formacion_complementaria",
        ("formación complementaria", "formacion complementaria", "curso", "diplomado", "seminario"),
    ),
    (
        "formacion_academica",
        ("formación académica", "formacion academica", "formación", "formacion", "pregrado", "maestría", "maestria", "doctorado", "título"),
    ),
    (
        "experiencia_profesional",
        ("experiencia profesional", "experiencia", "cargo", "empleo", "trabajó", "trabajo en"),
    ),
    ("identificadores_autor", ("orcid", "identificador")),
    ("articulos", ("artículo", "articulo", "publicación", "publicacion", "publicado")),
    ("proyectos", ("proyecto",)),
    ("trabajos_dirigidos", ("trabajo dirigido", "trabajos dirigidos", "tesis")),
    ("evento_cientifico", ("evento", "congreso", "ponencia")),
    ("capitulos_libro", ("capítulo de libro", "capitulo de libro", "capítulo", "capitulo")),
    ("libros", ("libro",)),
    ("software", ("software",)),
    ("productos_tecnologicos", ("producto tecnológico", "producto tecnologico", "productos tecnológicos")),
    ("procesos_tecnicas", ("proceso", "técnica", "tecnica")),
    ("asesorias", ("asesoría", "asesoria")),
    ("redes_conocimiento", ("red de conocimiento", "redes de conocimiento")),
    ("patentes", ("patente",)),
    ("insumos_politica", ("insumo", "política pública", "politica publica")),
    ("desarrollos_web", ("desarrollo web", "aplicación web", "aplicacion web")),
    ("manuales_guias", ("manual", "guía", "guia")),
    ("redes_sociales", ("red social", "redes sociales")),
    ("par_evaluador", ("par evaluador", "evaluador")),
)
