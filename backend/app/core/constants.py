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
