# Estrategia de Segmentación y Selección del Modelo de Embeddings

A continuación se define la estrategia de segmentación de la información y se selecciona el modelo de generación de embeddings. Ambos componentes resultan determinantes para la calidad de la recuperación: la segmentación establece las unidades de información sobre las que se realiza la búsqueda, mientras que el modelo de embeddings determina la calidad de la representación vectorial de dichas unidades.

El propósito de este documento es analizar las alternativas disponibles, explicar los criterios que las justifican, compararlas y adoptar la opción más adecuada para el proyecto.

## 1. Estrategia de Segmentación

### 1.1 Objetivo y Contexto

La segmentación (chunking) divide la información de las hojas de vida en unidades procesables por el sistema. El objetivo es que cada unidad conserve su integridad semántica, de modo que la búsqueda recupere fragmentos completos y coherentes, y no porciones que pierdan el sentido al separarse de su contexto.

La información de CvLAC posee una característica determinante: se encuentra organizada en aspectos y subítems, y cada registro (una formación, un proyecto, una publicación) constituye una unidad autónoma con significado propio. Esta estructura condiciona la selección de la estrategia de segmentación.

### 1.2 Criterios de Evaluación

| Criterio | Descripción |
|---|---|
| S1 | Preservación de la integridad semántica de cada unidad de información |
| S2 | Adecuación a la estructura de los datos |
| S3 | Complejidad de implementación |
| S4 | Costo computacional |
| S5 | Trazabilidad del fragmento hacia su investigador y sección de origen |

### 1.3 Alternativas Consideradas

| Estrategia | Descripción |
|---|---|
| Fija por tamaño | Divide el texto cada cantidad determinada de caracteres o palabras, sin considerar el contenido |
| Recursiva por caracteres | Divide jerárquicamente por separadores (párrafo, oración, espacio) hasta alcanzar el tamaño objetivo |
| Por oración | Divide respetando los límites de las oraciones |
| Semántica (por embeddings) | Utiliza las representaciones vectoriales para detectar cambios de tema y ubicar los puntos de corte |
| Por unidad lógica | Aprovecha la estructura propia del documento, empleando cada registro como una unidad independiente |

### 1.4 Comparación y Decisión

| Estrategia | S1 | S2 | S3 | S4 | S5 | Decisión |
|---|---|---|---|---|---|---|
| Fija por tamaño | Baja | Baja | Baja | Baja | Baja | Descartada |
| Recursiva por caracteres | Media | Media | Baja | Baja | Media | Descartada |
| Por oración | Media | Baja | Baja | Baja | Media | Descartada |
| Semántica (por embeddings) | Alta | Media | Media | Alta | Media | Alternativa |
| **Por unidad lógica** | Alta | Alta | Media | Baja | Alta | Seleccionada |

Se selecciona la segmentación **por unidad lógica**. Los argumentos son los siguientes:

- Aprovecha la estructura propia de CvLAC: cada registro es una unidad con significado autónomo, por lo que la segmentación respeta las fronteras naturales de la información (criterios S1 y S2).
- Preserva la trazabilidad, ya que cada fragmento se vincula de manera directa con el investigador y la sección a la que pertenece (criterio S5).
- No introduce costo computacional adicional, a diferencia de la segmentación semántica, que requiere generar embeddings intermedios para localizar los puntos de corte (criterio S4).

La segmentación semántica, si bien es adecuada para textos no estructurados, se descarta como opción principal porque la información de CvLAC ya se encuentra estructurada, en este contexto la estructura proporciona fronteras semánticas más fiables y de menor costo. Las estrategias fija, recursiva y por oración se descartan por fragmentar registros completos o por desconocer la estructura de los datos.

Como complemento, se establece un **límite superior de tamaño** para cada unidad: si un registro individual excede el tamaño máximo definido, se aplica una división recursiva únicamente sobre ese registro, de modo que se garantice un tamaño manejable sin sacrificar la integridad de los registros que sí se encuentran dentro del límite.

## 2. Selección del Modelo de Embeddings

### 2.1 Rol del Modelo

El modelo de embeddings transforma el texto en una representación vectorial de alta dimensionalidad, sobre la cual se calcula la similitud semántica durante la búsqueda. La calidad de esta representación determina la capacidad del sistema para relacionar una consulta con la información relevante, incluso cuando no comparten términos literales.

### 2.2 Criterios de Evaluación

| Criterio | Descripción |
|---|---|
| E1 | Desempeño en idioma español, dado que el corpus corresponde a hojas de vida en dicho idioma |
| E2 | Orientación a tareas de recuperación (entrenamiento contrastivo para búsqueda, no solo similitud de oraciones) |
| E3 | Dimensionalidad y costo de procesamiento en CPU |
| E4 | Licencia y costo |
| E5 | Estabilidad y reproducibilidad |

### 2.3 Conjunto de Candidatos

El conjunto de modelos comparados se delimita de acuerdo con las siguientes familias, con el fin de representar el espectro de decisiones relevantes para el proyecto:

1. **Modelos compactos de propósito general** (`all-MiniLM-L6-v2`): representan la familia de modelos pequeños con orientación al inglés. Se incluyen para evidenciar la comparación con la solución existente y justificar su sustitución.
2. **Modelos multilingües orientados a recuperación** (`intfloat/multilingual-e5-base`): representan la familia entrenada de forma contrastiva y específicamente para búsqueda en múltiples idiomas.
3. **Modelos multilingües con representación múltiple** (`BAAI/bge-m3`): además del vector denso generan representaciones esparsas y de múltiples vectores, útiles para la búsqueda léxica.
4. **Modelos específicos de español** (`jina-embeddings-v2-base-es`): representan la familia especializada en el idioma del corpus.

Quedan excluidas del análisis las APIs propietarias de embeddings, por implicar un costo recurrente incompatible con las restricciones del proyecto (criterio E4).

### 2.4 Comparación y Decisión

| Modelo | Dimensiones | E1 | E2 | E3 | E4 | E5 | Decisión |
|---|---|---|---|---|---|---|---|
| `all-MiniLM-L6-v2` | 384 | Limitado | Baja | Bajo | Libre | Alta | Descartado |
| **`intfloat/multilingual-e5-base`** | 768 | Adecuado | Alta | Moderado | Libre | Alta | Seleccionado |
| `BAAI/bge-m3` | 1024 | Adecuado | Alta | Alto | Libre | Alta | Alternativa |
| `jina-embeddings-v2-base-es` | 768 | Alto | Alta | Moderado | Libre | Alta | Alternativa |

Se selecciona el modelo **`intfloat/multilingual-e5-base`**. Los argumentos son los siguientes:

- Ofrece un desempeño adecuado en español y está entrenado de forma contrastiva orientada a recuperación, lo que lo hace apropiado para la búsqueda semántica (criterios E1 y E2).
- Su dimensionalidad (768) y su costo de procesamiento en CPU resultan moderados, compatibles con el hardware disponible (criterio E3).
- Es de código abierto y no implica costo de uso (criterio E4).

El modelo `bge-m3` ofrece una representación múltiple de interés para la búsqueda híbrida; sin embargo, su dimensionalidad superior eleva el costo de procesamiento en CPU. Dado que la componente léxica se resuelve mediante la búsqueda híbrida nativa de la base de datos vectorial, no se considera necesario asumir dicho costo adicional. El modelo `jina-embeddings-v2-base-es` queda como alternativa específica de español, en caso de que en etapas posteriores se evidencie una mejora de desempeño que justifique su adopción.

### 2.5 Requisito Técnico Asociado

La familia de modelos `e5` requiere el uso de prefijos específicos para alcanzar su desempeño óptimo: el prefijo `query:` antecede a las consultas y el prefijo `passage:` antecede a los fragmentos indexados. Este requisito debe aplicarse de manera consistente tanto en la indexación como en la consulta, y se documenta como una condición técnica de implementación del adaptador de embeddings.

## 3. Resumen de las Decisiones

| Componente | Decisión adoptada | Criterios atendidos |
|---|---|---|
| Estrategia de segmentación | Por unidad lógica, con límite de tamaño | S1, S2, S4, S5 |
| Modelo de embeddings | `intfloat/multilingual-e5-base` | E1, E2, E3, E4 |
| Prefijos de embeddings | `query:` y `passage:` | E2, E5 |
