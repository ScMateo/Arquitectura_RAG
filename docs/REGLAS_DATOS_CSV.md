# Reglas de Datos (Contrato CSV)

> **Versión:** 2.0 | **Fecha:** 2026-10-12 | **Alcance:** Contrato de datos para el módulo de extracción

Este documento define la estructura que deben cumplir los archivos CSV generados por el módulo de extracción. Su propósito es que la información recopilada de CvLAC llegue al sistema con un formato uniforme, de modo que las etapas de limpieza, segmentación e indexación operen sobre un formato conocido y consistente.

Los campos del archivo corresponden, sin modificaciones, a los subítems de CvLAC seleccionados en el análisis de la estructura de datos, junto con el enlace de la hoja de vida requerido por la historia de usuario HU-03.

## 1. Reglas Globales de Formato

| Propiedad | Regla |
|---|---|
| Archivo | Un archivo por lote, nombrado `investigadores.csv` (o `investigadores_<lote>.csv`) |
| Codificación | UTF-8 sin BOM |
| Separador de campos | `|` (barra vertical) |
| Cita de campos | `QUOTE_ALL`: todas las celdas se encierran entre comillas dobles |
| Encabezado | Primera fila con los nombres de las columnas, en `snake_case`, sin acentos ni espacios |
| Registros | Una hoja de vida por fila |
| Fin de línea | `\n` (LF) |

El uso de `|` como separador y de `QUOTE_ALL` evita los conflictos derivados de comas, comillas o caracteres especiales presentes en el texto de las hojas de vida.

## 2. Reglas de Formato por Tipo de Dato

| Tipo | Regla |
|---|---|
| Texto libre | Sin saltos de línea (`\n`, `\r`), sin tabulaciones (`\t`), sin entidades HTML, sin comillas internas |
| Valores vacíos | Cadena vacía `""`; nunca `nan`, `0` ni `NULL` |
| Fecha | Se conserva como texto, normalizada sin espacios intermedios |
| URL | Dirección completa con protocolo (`https://...`), sin espacios |

## 3. Columnas del Archivo

El archivo debe contener las siguientes columnas, en este orden. La columna indica el nombre que debe aparecer en el encabezado, y el campo indica el subítem de CvLAC del cual proviene la información.

| Columna | Campo en CvLAC | Contenido |
|---|---|---|
| `identificacion` | Identificación | Datos que permiten reconocer al investigador: nombre, nacionalidad, sexo |
| `url_cvlac` | Enlace de la hoja de vida | Dirección directa al perfil del investigador en CvLAC |
| `formacion_academica` | Formación académica | Estudios realizados, títulos, instituciones y fechas |
| `experiencia_profesional` | Experiencia profesional | Cargos, instituciones y períodos laborales |
| `articulos` | Artículos | Artículos publicados |
| `proyectos` | Proyectos | Proyectos de investigación en los que participa |
| `identificadores_autor` | Identificadores de autor | Identificadores académicos como ORCID |
| `software` | Software | Desarrollos de software registrados |
| `productos_tecnologicos` | Productos tecnológicos | Productos tecnológicos desarrollados |
| `formacion_complementaria` | Formación complementaria | Cursos y actividades de formación adicional |
| `trabajos_dirigidos` | Trabajos dirigidos/tutorías | Dirección y tutoría de trabajos académicos |
| `evento_cientifico` | Evento científico | Participación en eventos científicos |
| `libros` | Libros | Libros publicados |
| `capitulos_libro` | Capítulos de libro | Capítulos publicados en obras colectivas |
| `procesos_tecnicas` | Procesos o técnicas | Procesos y técnicas desarrollados |
| `asesorias` | Asesorías | Actividades de asesoría y acompañamiento |
| `redes_conocimiento` | Redes de conocimiento especializado | Participación en redes de conocimiento |
| `patentes` | Patentes | Patentes registradas |
| `insumos_politica` | Insumos de política pública y normatividad | Aportes a políticas públicas o normas |
| `desarrollos_web` | Desarrollos web | Productos o recursos digitales desarrollados |
| `manuales_guias` | Manuales y guías especializadas | Documentos de orientación sobre temas específicos |
| `redes_sociales` | Redes sociales académicas | Perfiles académicos y redes asociadas |
| `par_evaluador` | Par evaluador | Participación como evaluador de productos académicos |

## 4. Convenciones de Nombres de Columnas

- Nombres en `snake_case`, en minúsculas, sin acentos, sin espacios ni caracteres especiales.
- Cada columna corresponde a un único subítem de CvLAC; no se agrupan subítems distintos en una misma columna.
- El nombre de la columna conserva el singular o plural del campo original.

## 5. Relación con la Ingesta

Cada columna se interpreta como una sección durante la ingesta, y cada registro dentro de la columna se segmenta por unidad lógica. El metadato de cada fragmento se construye a partir de las columnas: la sección corresponde al nombre de la columna, el enlace corresponde a `url_cvlac`, y el autor se obtiene del campo de identificación.

Esta relación garantiza que la trazabilidad de la información (HU-10) y la entrega del enlace (HU-03) se conserven desde el origen de los datos hasta la respuesta del sistema.

## 6. Ejemplo de Registro

```
"identificacion"|"url_cvlac"|"formacion_academica"|"experiencia_profesional"|"articulos"|"proyectos"|"identificadores_autor"|"software"|"productos_tecnologicos"|"formacion_complementaria"|"trabajos_dirigidos"|"evento_cientifico"|"libros"|"capitulos_libro"|"procesos_tecnicas"|"asesorias"|"redes_conocimiento"|"patentes"|"insumos_politica"|"desarrollos_web"|"manuales_guias"|"redes_sociales"|"par_evaluador"
"Nombre Allan Andrew Wood Nacionalidad Colombiana Sexo Masculino"|"https://scienti.minciencias.gov.co/cvlac/visualizador/generarCurriculoCv.do?cod_rh=0000000000"|"Doctorado Imperial College of Science, Technology and Medicine Agricultural Economics Octubre de 2004"|"Profesor Universidad Nacional de Colombia"|"Artículo sobre producción agrícola en la Amazonía"|"Producción agrícola local y seguridad alimentaria"|"ORCID 0000-0000-0000-0000"|""|""|""|""|""|""|""|""|""|""|""|""|""|""|""|""
```

## 7. Referencias

- Documento de análisis de la estructura de datos de CvLAC.
- Documento de estrategia de segmentación y selección del modelo de embeddings.
- Documento de reglas del proyecto.
