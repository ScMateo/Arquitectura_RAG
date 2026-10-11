# Análisis de Requerimientos Técnicos y Funcionales para la Mejora de la Recuperación de Información

En el siguiente documento se realiza el análisis de los requerimientos técnicos y funcionales orientados a mejorar la recuperación de información en el aplicativo. Este análisis constituye el vínculo entre las necesidades expresadas en las historias de usuario, la información disponible en CvLAC y las herramientas seleccionadas, y define el comportamiento esperado del mecanismo de recuperación.

El propósito de este documento es doble. En primer lugar, caracterizar las limitaciones de la búsqueda tradicional que motivan la mejora. En segundo lugar, establecer los requerimientos funcionales y técnicos que el sistema debe satisfacer, así como las decisiones de diseño del proceso de recuperación.

## 1. Limitaciones de la Búsqueda Tradicional

La plataforma CvLAC dispone de un buscador basado en la coincidencia de términos y en filtros estructurados. Este mecanismo presenta limitaciones que justifican la adopción de un enfoque basado en recuperación aumentada por generación (RAG):

- **Dependencia de coincidencia literal:** el usuario debe conocer los términos exactos con los que fue registrada la información; las variantes de escritura, los sinónimos y los acrónimos no se resuelven de manera automática.
- **Ausencia de comprensión semántica:** la búsqueda no interpreta el significado de la consulta, sino la presencia de palabras, lo que limita las consultas en lenguaje natural.
- **Sin síntesis de resultados:** el buscador presenta listados de registros, pero no integra la información de múltiples hojas de vida en una respuesta coherente.
- **Sin contexto conversacional:** cada consulta se resuelve de forma aislada, sin conservar el contexto de interacciones previas.

Estas limitaciones motivan la definición de requerimientos orientados a superarlas mediante la combinación de búsqueda semántica, filtrado por atributos y generación de respuestas fundamentadas en la información recuperada.

## 2. Requerimientos Funcionales

Los requerimientos funcionales se derivan de las historias de usuario y describen las capacidades que el mecanismo de recuperación debe ofrecer.

| Identificador | Requerimiento funcional | Historia de usuario |
|---|---|---|
| RF-1 | Interpretar consultas formuladas en lenguaje natural, sin una estructura preestablecida | HU-06 |
| RF-2 | Identificar al investigador mencionado en la consulta y recuperar los aspectos solicitados | HU-04 |
| RF-3 | Aplicar filtros por atributos del investigador (autor, sección) durante la recuperación | HU-04 |
| RF-4 | Realizar búsquedas temáticas sobre el conjunto de la información, diferenciando los investigadores identificados | HU-05 |
| RF-5 | Relacionar acrónimos y denominaciones equivalentes, sin generar falsas equivalencias | HU-09 |
| RF-6 | Entregar el enlace de la hoja de vida referenciada | HU-03 |
| RF-7 | Indicar las hojas de vida empleadas como fuente de cada respuesta | HU-10 |
| RF-8 | Generar resúmenes de la información recuperada sin introducir contenido ajeno a la fuente | HU-08 |
| RF-9 | Conservar el contexto de las últimas interacciones para dar continuidad al análisis | HU-07 |

## 3. Requerimientos Técnicos

Los requerimientos técnicos describen las condiciones que debe cumplir la implementación del mecanismo de recuperación, en coherencia con las herramientas seleccionadas.

| Identificador | Requerimiento técnico |
|---|---|
| RT-1 | Indexar la información mediante segmentación por unidad lógica, preservando la integridad de cada formación, proyecto o publicación |
| RT-2 | Emplear búsqueda híbrida, que combine la recuperación semántica con la recuperación léxica |
| RT-3 | Aplicar el filtrado por metadatos de manera nativa en la base de datos vectorial |
| RT-4 | Normalizar acrónimos y variantes mediante un mapeo basado en evidencia extraída del propio corpus |
| RT-5 | Clasificar la consulta para distinguir entre búsqueda específica (un investigador) y general (temática) |
| RT-6 | Ordenar y seleccionar los fragmentos recuperados mediante un mecanismo de re-ranking |
| RT-7 | Generar la respuesta exclusivamente a partir del contexto recuperado, conservando la trazabilidad de las fuentes |

## 4. Proceso de Recuperación Propuesto

El mecanismo de recuperación se organiza en una secuencia de etapas que transforman la consulta del usuario en una respuesta fundamentada.

1. **Preprocesamiento de la consulta:** se normaliza el texto y se resuelven los acrónimos mediante el mapeo basado en evidencia (RT-4).
2. **Clasificación de la consulta:** se determina si la consulta se refiere a un investigador específico o a una temática general (RT-5).
3. **Recuperación:** se ejecuta la búsqueda híbrida, con filtrado por metadatos cuando corresponde (RT-2, RT-3).
4. **Re-ranking:** se ordenan y seleccionan los fragmentos más pertinentes (RT-6).
5. **Generación:** se compone la respuesta a partir del contexto recuperado, indicando las fuentes (RT-7).

## 5. Alternativas y Decisiones de Diseño

### 5.1 Estrategia de Recuperación

| Estrategia | Manejo de acrónimos | Precisión | Decisión |
|---|---|---|---|
| Densa (solo semántica) | Limitado | Media | Descartada |
| **Híbrida (densa + léxica)** | Adecuado | Alta | Seleccionada |
| Léxica (solo palabras clave) | Bajo | Baja | Descartada |

Se selecciona la **búsqueda híbrida**. La combinación de la recuperación semántica con la recuperación léxica permite, por un lado, interpretar consultas en lenguaje natural (RF-1) y, por otro, relacionar acrónimos y variantes de escritura sin generar falsas equivalencias (RF-5). La búsqueda únicamente léxica reproduce las limitaciones del buscador tradicional, mientras que la únicamente densa no resuelve de forma fiable las variantes de denominación.

### 5.2 Clasificación de Consultas

La clasificación permite distinguir entre una consulta específica sobre un investigador y una consulta general sobre una temática, condición necesaria para aplicar el filtrado por metadatos cuando corresponde.

| Enfoque | Precisión | Robustez | Decisión |
|---|---|---|---|
| Reglas y heurísticas (palabras clave) | Baja | Media | Descartada |
| **Modelo de lenguaje con salida estructurada** | Alta | Alta | Seleccionado |
| Sin clasificación (recuperación única) | No aplica | Baja | Descartada |

Se selecciona la **clasificación mediante el modelo de lenguaje con salida estructurada**. Este enfoque interpreta la consulta en lenguaje natural y devuelve una clasificación formal (investigador específico o temática general), superando la fragilidad de las reglas basadas en palabras clave, que no se adaptan a la variedad de formulaciones propias del lenguaje natural (RF-1). La ausencia de clasificación se descarta porque impide aplicar correctamente el filtrado por metadatos (RF-3).

### 5.3 Re-ranking de Resultados

El re-ranking ordena los fragmentos recuperados para seleccionar los más pertinentes a la consulta.

| Enfoque | Costo | Precisión | Decisión |
|---|---|---|---|
| Sin re-ranking (orden por similitud) | Nulo | Media | Descartada |
| **Ponderación de relevancia y prioridad de sección** | Bajo | Adecuada | Seleccionada |
| Re-ranking por modelo de relevancia (cross-encoder) | Medio | Alta | Evolución futura |
| Re-ranking mediante el modelo de lenguaje | Alto | Alta | Descartada |

Se selecciona la **ponderación entre la relevancia semántica y la prioridad de la sección**. Este enfoque combina la puntuación de similitud obtenida en la recuperación con la prioridad definida para cada sección de la hoja de vida, de modo que las secciones de mayor valor descriptivo (formación, experiencia, proyectos) se favorezcan sin descartar el resto. No introduce modelos adicionales ni llamadas externas, lo que resulta compatible con el procesamiento en CPU.

El re-ranking mediante un modelo de relevancia (cross-encoder) se documenta como evolución, por su capacidad de mejorar la precisión a cambio de un costo de procesamiento adicional. El re-ranking mediante el modelo de lenguaje se descarta por añadir latencia y llamadas a la API sin una ventaja proporcional en esta etapa.
