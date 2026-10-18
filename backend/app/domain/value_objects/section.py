"""Section value object: enumerated CvLAC sections.

Derived from ANALISIS_ESTRUCTURA_CVLAC.md. Each member maps to a column
of the CSV contract defined in REGLAS_DATOS_CSV.md.
"""

from enum import StrEnum


class Section(StrEnum):
    """Sección de la hoja de vida CvLAC usada como metadato de los fragmentos."""

    IDENTIFICACION = "identificacion"
    FORMACION_ACADEMICA = "formacion_academica"
    EXPERIENCIA_PROFESIONAL = "experiencia_profesional"
    ARTICULOS = "articulos"
    PROYECTOS = "proyectos"
    IDENTIFICADORES_AUTOR = "identificadores_autor"
    SOFTWARE = "software"
    PRODUCTOS_TECNOLOGICOS = "productos_tecnologicos"
    FORMACION_COMPLEMENTARIA = "formacion_complementaria"
    TRABAJOS_DIRIGIDOS = "trabajos_dirigidos"
    EVENTO_CIENTIFICO = "evento_cientifico"
    LIBROS = "libros"
    CAPITULOS_LIBRO = "capitulos_libro"
    PROCESOS_TECNICAS = "procesos_tecnicas"
    ASESORIAS = "asesorias"
    REDES_CONOCIMIENTO = "redes_conocimiento"
    PATENTES = "patentes"
    INSUMOS_POLITICA = "insumos_politica"
    DESARROLLOS_WEB = "desarrollos_web"
    MANUALES_GUIAS = "manuales_guias"
    REDES_SOCIALES = "redes_sociales"
    PAR_EVALUADOR = "par_evaluador"
