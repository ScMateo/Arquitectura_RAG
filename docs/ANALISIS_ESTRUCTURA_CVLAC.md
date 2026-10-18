# Análisis de la Estructura de Datos de CvLAC y Clasificación de la Información

Continuando con la planeación del proyecto, se realiza el análisis de la estructura de la información administrada por la plataforma CvLAC y la clasificación de sus componentes según su utilidad para el sistema de recuperación de información. Este análisis constituye la base para determinar qué datos resultan pertinentes para caracterizar académica, científica y profesionalmente a cada investigador, y establece los criterios que orientarán la recopilación de información en las etapas posteriores.

El propósito de esta etapa es doble. En primer lugar, describir la constitución de CvLAC, es decir, las secciones y los elementos que la integran. En segundo lugar, clasificar y valorar cada elemento para seleccionar aquellos que aportan mayor valor al proyecto, garantizando que toda decisión se sustente en criterios explícitos y trazables a las historias de usuario.

## 1. Constitución de CvLAC

La información administrada por CvLAC comprende diferentes dimensiones de la trayectoria de un investigador: su identidad, su formación, su experiencia, su participación en actividades académicas, su producción intelectual y sus contribuciones técnicas y sociales. Estas dimensiones se organizan en ocho aspectos generales que en conjunto reúnen 54 subítems.

| Aspecto general | N.º de subítems | Subítems |
|---|---|---|
| **Datos Generales** | 8 | Identificación; Redes sociales académicas; Identificadores de autor; Formación académica; Formación complementaria; Estancias posdoctorales; Experiencia profesional; Otra información personal |
| **Actividades de Formación** | 3 | Asesorías; Cursos de corta duración; Trabajos dirigidos/tutorías |
| **Actividades Evaluadoras** | 3 | Jurado/comisiones evaluadoras de trabajo de grado; Par evaluador; Participación en comité de evaluación |
| **Apropiación Social** | 13 | Edición; Evento científico; Redes de conocimiento especializado; Fortalecimiento o solución de asuntos de interés social; Trabajo conjunto entre Centro de Ciencia y grupo de investigación; Generación de insumos de política pública y normatividad; Fortalecimiento de cadenas productivas; Publicaciones editoriales no especializadas; Producciones de contenido digital audiovisual; Producciones de contenido digital sonoro; Producciones de contenido digital mediante recursos gráficos; Producción de estrategias y contenidos transmedia; Desarrollos web |
| **Producción Bibliográfica** | 11 | Artículos; Libros; Capítulos de libro; Nota científica; Textos en publicaciones no científicas; Otra producción bibliográfica; Traducciones filológicas y edición de fuentes; Libro de creación; Libro de formación; Libros de divulgación y/o compilación; Manuales y guías especializadas |
| **Producción Técnica** | 9 | Patentes; Secretos empresariales; Software; Productos tecnológicos; Procesos o técnicas; Trabajos técnicos; Normas y regulaciones; Otra producción técnica; Empresas de base tecnológica |
| **Más Información** | 2 | Demás trabajos; Proyectos |
| **Producción en Arte** | 5 | Obras o productos; Registros de acuerdo de licencia; Industrias creativas y culturales; Evento artístico; Talleres creativos |

Es pertinente señalar que no todos los investigadores presentan la misma trayectoria ni desarrollan actividades equivalentes. Un investigador de ciencias básicas puede concentrar su experiencia en publicaciones y proyectos, mientras que un investigador de ingeniería puede registrar desarrollos tecnológicos o software. Por esta razón, la valoración no debe asumir que todos los subítems tienen la misma presencia o importancia en cada perfil.

## 2. Criterios de Valoración

Para clasificar los 54 subítems se establecen cinco criterios que, en conjunto, permiten valorar su utilidad potencial para el sistema de búsqueda y recuperación.

| Criterio | Descripción |
|---|---|
| Relevancia para las consultas (RC) | Mide cuánto contribuye el subítem a responder preguntas sobre la identidad, formación, experiencia, producción o especialidad de un investigador. |
| Capacidad de caracterización (CC) | Evalúa cuánto aporta a comprender la trayectoria, los conocimientos, las competencias o los resultados del investigador. |
| Generalidad (G) | Valora su aplicabilidad para caracterizar investigadores de diferentes disciplinas, sin que la presencia del dato sea uniforme en todos los perfiles. |
| Utilidad para la búsqueda y recuperación (UB) | Estima su capacidad para facilitar la identificación de perfiles pertinentes, distinguir investigadores o recuperar información relacionada con una consulta. |
| Calidad y estructura de la información (CE) | Evalúa si el campo suele contener información completa, estructurada y con el detalle descriptivo necesario para su interpretación, segmentación y recuperación. |

El quinto criterio (CE) se incorpora porque la existencia de un campo no garantiza que su contenido sea suficientemente descriptivo para resolver una consulta; para que un dato contribuya a la recuperación, es necesario que pueda interpretarse en su contexto y que contenga detalles pertinentes sobre la actividad, el producto o la experiencia registrados.

Cada criterio se valora en una escala de cinco niveles, donde 1 representa una contribución baja y 5 una contribución alta. El puntaje total se obtiene sumando las valoraciones de los cinco criterios, con un máximo de 25 puntos. Los resultados se interpretan mediante las siguientes categorías:

| Puntaje | Categoría |
|---|---|
| 21–25 | Contribución muy alta |
| 17–20 | Contribución alta |
| 13–16 | Contribución media |
| 9–12 | Contribución baja |
| 5–8 | Contribución muy baja |

## 3. Clasificación de los Subítems

La siguiente tabla presenta la valoración de los 54 subítems. La puntuación constituye una valoración metodológica inicial y no una medida estadística de la calidad de los datos, debe entenderse como un instrumento para comparar la utilidad potencial de los elementos.

| N.º | Aspecto | Subítem | RC | CC | G | UB | CE | Total |
|---|---|---|---|---|---|---|---|---|
| 1 | Datos Generales | Identificación | 5 | 5 | 5 | 5 | 5 | **25** |
| 2 | Datos Generales | Redes sociales académicas | 3 | 3 | 4 | 3 | 4 | **17** |
| 3 | Datos Generales | Identificadores de autor | 4 | 4 | 5 | 5 | 4 | **22** |
| 4 | Datos Generales | Formación académica | 5 | 5 | 5 | 5 | 5 | **25** |
| 5 | Datos Generales | Formación complementaria | 4 | 4 | 4 | 4 | 4 | **20** |
| 6 | Datos Generales | Estancias posdoctorales | 3 | 4 | 3 | 3 | 3 | **16** |
| 7 | Datos Generales | Experiencia profesional | 5 | 5 | 5 | 5 | 5 | **25** |
| 8 | Datos Generales | Otra información personal | 2 | 2 | 3 | 2 | 2 | **11** |
| 9 | Actividades de Formación | Asesorías | 4 | 4 | 4 | 4 | 3 | **19** |
| 10 | Actividades de Formación | Cursos de corta duración | 3 | 3 | 4 | 3 | 3 | **16** |
| 11 | Actividades de Formación | Trabajos dirigidos/tutorías | 4 | 4 | 4 | 4 | 4 | **20** |
| 12 | Actividades Evaluadoras | Jurado/comisiones evaluadoras | 3 | 4 | 3 | 3 | 3 | **16** |
| 13 | Actividades Evaluadoras | Par evaluador | 3 | 4 | 3 | 4 | 3 | **17** |
| 14 | Actividades Evaluadoras | Participación en comité de evaluación | 3 | 3 | 3 | 3 | 3 | **15** |
| 15 | Apropiación Social | Edición | 2 | 3 | 2 | 2 | 3 | **12** |
| 16 | Apropiación Social | Evento científico | 4 | 4 | 4 | 4 | 4 | **20** |
| 17 | Apropiación Social | Redes de conocimiento especializado | 4 | 4 | 4 | 4 | 3 | **19** |
| 18 | Apropiación Social | Fortalecimiento o solución de asuntos de interés social | 3 | 4 | 3 | 3 | 3 | **16** |
| 19 | Apropiación Social | Trabajo conjunto Centro de Ciencia-grupo | 3 | 4 | 2 | 3 | 3 | **15** |
| 20 | Apropiación Social | Insumos de política pública y normatividad | 4 | 4 | 3 | 4 | 3 | **18** |
| 21 | Apropiación Social | Fortalecimiento de cadenas productivas | 3 | 4 | 2 | 3 | 3 | **15** |
| 22 | Apropiación Social | Publicaciones editoriales no especializadas | 2 | 3 | 3 | 2 | 3 | **13** |
| 23 | Apropiación Social | Contenido digital audiovisual | 3 | 3 | 3 | 3 | 3 | **15** |
| 24 | Apropiación Social | Contenido digital sonoro | 2 | 3 | 2 | 2 | 3 | **12** |
| 25 | Apropiación Social | Contenido digital recursos gráficos | 2 | 3 | 3 | 2 | 3 | **13** |
| 26 | Apropiación Social | Estrategias y contenidos transmedia | 2 | 3 | 2 | 2 | 2 | **11** |
| 27 | Apropiación Social | Desarrollos web | 3 | 4 | 3 | 4 | 4 | **18** |
| 28 | Producción Bibliográfica | Artículos | 5 | 5 | 5 | 5 | 5 | **25** |
| 29 | Producción Bibliográfica | Libros | 4 | 4 | 4 | 4 | 4 | **20** |
| 30 | Producción Bibliográfica | Capítulos de libro | 4 | 4 | 4 | 4 | 4 | **20** |
| 31 | Producción Bibliográfica | Nota científica | 3 | 4 | 3 | 3 | 3 | **16** |
| 32 | Producción Bibliográfica | Textos en publicaciones no científicas | 2 | 3 | 3 | 2 | 3 | **13** |
| 33 | Producción Bibliográfica | Otra producción bibliográfica | 3 | 3 | 3 | 3 | 3 | **15** |
| 34 | Producción Bibliográfica | Traducciones filológicas | 2 | 3 | 2 | 2 | 3 | **12** |
| 35 | Producción Bibliográfica | Libro de creación | 2 | 3 | 2 | 2 | 3 | **12** |
| 36 | Producción Bibliográfica | Libro de formación | 3 | 4 | 3 | 3 | 3 | **16** |
| 37 | Producción Bibliográfica | Libros de divulgación | 3 | 4 | 3 | 3 | 3 | **16** |
| 38 | Producción Bibliográfica | Manuales y guías especializadas | 3 | 4 | 3 | 4 | 4 | **18** |
| 39 | Producción Técnica | Patentes | 4 | 5 | 2 | 4 | 4 | **19** |
| 40 | Producción Técnica | Secretos empresariales | 2 | 4 | 2 | 2 | 2 | **12** |
| 41 | Producción Técnica | Software | 4 | 5 | 3 | 5 | 4 | **21** |
| 42 | Producción Técnica | Productos tecnológicos | 4 | 5 | 3 | 5 | 4 | **21** |
| 43 | Producción Técnica | Procesos o técnicas | 4 | 5 | 3 | 4 | 4 | **20** |
| 44 | Producción Técnica | Trabajos técnicos | 3 | 4 | 3 | 3 | 3 | **16** |
| 45 | Producción Técnica | Normas y regulaciones | 3 | 4 | 2 | 3 | 3 | **15** |
| 46 | Producción Técnica | Otra producción técnica | 3 | 3 | 2 | 3 | 3 | **14** |
| 47 | Producción Técnica | Empresas de base tecnológica | 3 | 4 | 2 | 3 | 3 | **15** |
| 48 | Más Información | Demás trabajos | 2 | 3 | 2 | 2 | 2 | **11** |
| 49 | Más Información | Proyectos | 5 | 5 | 5 | 5 | 5 | **25** |
| 50 | Producción en Arte | Obras o productos | 3 | 4 | 2 | 3 | 3 | **15** |
| 51 | Producción en Arte | Registros de acuerdo de licencia | 2 | 3 | 2 | 2 | 2 | **11** |
| 52 | Producción en Arte | Industrias creativas y culturales | 3 | 4 | 2 | 3 | 3 | **15** |
| 53 | Producción en Arte | Evento artístico | 2 | 3 | 2 | 2 | 3 | **12** |
| 54 | Producción en Arte | Talleres creativos | 2 | 3 | 2 | 2 | 3 | **12** |

## 4. Selección de la Información

La clasificación permite distinguir entre la utilidad general y la utilidad especializada. Los campos de utilidad general permiten construir una descripción inicial de una amplia variedad de investigadores, mientras que los campos especializados permiten reconocer características particulares que pueden ser decisivas en una consulta específica.

### 4.1 Campos de contribución muy alta (21–25)

Estos campos constituyen el núcleo de la información que se recopilará, por su capacidad para responder las consultas más frecuentes y por su valor descriptivo general.

| Subítem | Total | Relevancia para el proyecto |
|---|---|---|
| Identificación | 25 | Permite reconocer y diferenciar al investigador (HU-04, HU-05) |
| Formación académica | 25 | Responde consultas específicas sobre formación y especialidad (HU-04) |
| Experiencia profesional | 25 | Aporta trayectoria y antecedentes laborales (HU-04, HU-05) |
| Artículos | 25 | Producción científica central para búsquedas temáticas (HU-04, HU-05, HU-10) |
| Proyectos | 25 | Iniciativas de investigación y líneas de trabajo (HU-04, HU-05) |
| Identificadores de autor | 22 | Diferencian autores y vinculan la producción (HU-03, HU-10) |
| Software | 21 | Evidencia capacidades técnicas aplicadas (HU-05) |
| Productos tecnológicos | 21 | Representan innovación aplicada no reflejada en publicaciones (HU-05) |

### 4.2 Campos de contribución alta (17–20)

Estos campos complementan la caracterización del investigador y resultan determinantes en consultas específicas.

| Subítem | Total |
|---|---|
| Formación complementaria | 20 |
| Trabajos dirigidos/tutorías | 20 |
| Evento científico | 20 |
| Libros | 20 |
| Capítulos de libro | 20 |
| Procesos o técnicas | 20 |
| Asesorías | 19 |
| Redes de conocimiento especializado | 19 |
| Patentes | 19 |
| Insumos de política pública y normatividad | 18 |
| Desarrollos web | 18 |
| Manuales y guías especializadas | 18 |
| Redes sociales académicas | 17 |
| Par evaluador | 17 |

### 4.3 Campos excluidos por defecto

Los campos de contribución media o baja (puntaje menor a 17) no se consideran prioritarios para la recopilación inicial, dado que su aplicabilidad es más específica o su contenido suele ser menos descriptivo. Esta exclusión no implica que carezcan de valor: pueden incorporarse en consultas especializadas (industrias creativas, comunicación del conocimiento o transferencia tecnológica) si en etapas posteriores se identifica una necesidad concreta.