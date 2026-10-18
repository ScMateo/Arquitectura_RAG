# Identificación y Selección de Herramientas

Continuando con la planeación del proyecto, se realiza el análisis y la selección de las herramientas tecnológicas necesarias para el desarrollo e implementación del sistema. Esta selección constituye un insumo fundamental para las etapas posteriores de diseño e implementación, dado que determina las tecnologías sobre las cuales se construirá el sistema de recuperación de información basado en arquitectura RAG (Retrieval-Augmented Generation) aplicado a la información del sistema CvLAC.

El propósito de este documento es dejar registro de las herramientas seleccionadas y de los argumentos que sustentan cada decisión, de manera que toda elección sea trazable a un requisito funcional previamente establecido. Para ello, las decisiones se vinculan de forma explícita con las historias de usuario definidas en el documento de requisitos funcionales.

Los criterios de selección se derivan de dos fuentes:

1. Los requisitos funcionales expresados en las historias de usuario.
2. Las restricciones generales del proyecto.

## 1. Criterios de Selección

A partir del análisis de las historias de usuario se establecen los siguientes criterios, los cuales rigen la evaluación de las alternativas en cada componente del sistema.

### 1.1 Criterios derivados de los requisitos funcionales

| Criterio | Descripción | Historia de usuario asociada |
|---|---|---|
| C1 | Comprensión semántica del lenguaje natural en español, incluyendo el reconocimiento de acrónimos y denominaciones equivalentes | HU-06, HU-09 |
| C2 | Capacidad de filtrado por atributos del investigador (autor, sección) durante la recuperación | HU-04 |
| C3 | Recuperación temática sobre el conjunto de la información, diferenciando los investigadores identificados | HU-05 |
| C4 | Trazabilidad entre la información recuperada y la fuente de origen, para garantizar una referenciación correcta | HU-10 |
| C5 | Asociación de cada hoja de vida con un enlace de acceso directo | HU-03 |
| C6 | Gestión del contexto conversacional que permita dar continuidad a la interacción | HU-07 |
| C7 | Capacidad de resumir la información recuperada sin introducir contenido ajeno a la fuente | HU-08 |

### 1.2 Criterios derivados de las restricciones del proyecto

| Criterio | Descripción |
|---|---|
| C8 | Ejecución sobre hardware sin aceleración por GPU (procesamiento en CPU) |
| C9 | Presupuesto limitado, con preferencia por herramientas gratuitas y de software libre |
| C10 | Reproducibilidad del experimento: uso de versiones fijas y estables, evitando alias móviles |
| C11 | Mantenibilidad del código: modularidad y bajo acoplamiento entre componentes |

## 2. Análisis y Selección por Componente

Para cada componente se presenta un conjunto de alternativas, la comparación de las mismas frente a los criterios establecidos y la decisión adoptada, con su respectiva justificación.

### 2.1 Framework de Desarrollo

El sistema corresponde a una aplicación web con separación entre el componente servidor y el componente cliente. Cada uno de estos componentes exige la selección de un framework de desarrollo.

**Servidor (backend).** Se consideran las siguientes alternativas:

| Framework | Validación de datos | Soporte asíncrono | Orientación | Decisión |
|---|---|---|---|---|
| Django | Integrada (ORM) | Limitado | Aplicaciones completas | Descartado |
| Flask | No nativa | No nativo | Minimalista | Descartado |
| **FastAPI** | Nativa (Pydantic) | Nativo | Servicios y APIs | Seleccionado |
| Express (Node.js) | No nativa | Nativo | APIs | Descartado |

Se selecciona **FastAPI**. Los argumentos que sustentan la decisión son los siguientes:

- Proporciona validación de datos nativa mediante Pydantic, lo que garantiza contratos de entrada y salida bien definidos, un aspecto relevante para la trazabilidad de la información (criterio C4).
- Su soporte asíncrono nativo resulta adecuado para un servicio de inferencia que realiza llamadas a un modelo de lenguaje y a una base de datos vectorial.
- Django, si bien es completo, impone una estructura orientada a aplicaciones con persistencia relacional, lo que lo hace desproporcionado para un servicio de inferencia. Flask, por su parte, carece de validación y asíncrono nativos. Express se descarta porque el ecosistema de procesamiento de lenguaje natural y de bases de datos vectoriales está fuertemente ligado a Python.

**Cliente (frontend).** Se consideran las siguientes alternativas:

| Framework | Ecosistema | Curva de aprendizaje | Decisión |
|---|---|---|---|
| **React** | Amplio | Media | Seleccionado |
| Vue.js | Amplio | Baja | Alternativa |
| Angular | Amplio | Alta | Descartado |
| Svelte | Reducido | Baja | Descartado |

Se selecciona **React** junto con **Vite** como herramienta de construcción. React ofrece un ecosistema maduro y una amplia disponibilidad de bibliotecas complementarias, lo que facilita el desarrollo de una interfaz interactiva y modular (criterio C11). La decisión responde a criterios de mantenibilidad y de disponibilidad de recursos, y ambas tecnologías son de software libre (criterio C9).

### 2.2 Servidor ASGI y Despliegue

Para la ejecución del servidor se selecciona **Uvicorn**, el servidor ASGI de referencia para aplicaciones FastAPI. Las alternativas (Hypercorn) no aportan ventajas significativas para este caso de uso y carecen de la integración y el desempeño que Uvicorn ofrece por defecto.

Para el empaquetado y despliegue del sistema se selecciona **Docker** con **Docker Compose**. Esta decisión atiende el criterio C10, dado que la definición del entorno mediante contenedores garantiza que el sistema se ejecute de manera idéntica en cualquier máquina, un aspecto determinante para la reproducibilidad del experimento y para la demostración ante evaluadores. La alternativa de instalación directa de dependencias, si bien es válida durante el desarrollo, no ofrece las mismas garantías de reproducibilidad.

### 2.3 Gestión de Dependencias y Entorno

| Herramienta | Bloqueo de versiones | Complejidad | Decisión |
|---|---|---|---|
| **venv + pip (requirements.txt)** | Manual | Baja | Seleccionado |
| Poetry | Automático | Media | Alternativa |
| uv | Automático | Media | Alternativa |

Se selecciona **venv + pip** con un archivo `requirements.txt` con versiones fijadas. Esta elección prioriza la simplicidad y la transparencia, dado que el número de dependencias del proyecto es acotado. Poetry y uv ofrecen un bloqueo de versiones más robusto, por lo que se documentan como alternativas válidas si el proyecto crece en complejidad.

### 2.4 Estrategia de Segmentación del Texto

La segmentación (chunking) determina la forma en que la información de las hojas de vida se divide en unidades procesables por el sistema. Se consideran las siguientes estrategias:

| Estrategia | Conservación del contexto | Complejidad | Decisión |
|---|---|---|---|
| Fija por longitud de caracteres | Baja | Baja | Descartada |
| Recursiva por caracteres | Media | Baja | Descartada |
| Semántica (por embeddings) | Alta | Media | Alternativa |
| **Por unidad lógica** | Alta | Media | Seleccionada |

Se selecciona la **segmentación por unidad lógica**. El requisito HU-04 exige recuperar aspectos específicos de un investigador (formación académica, proyectos, producción), lo cual implica que cada unidad de información debe conservar su integridad semántica. La segmentación fija y la recursiva, al dividir el texto por longitud, fragmentan registros completos y comprometen la recuperación de información específica (criterios C1 y C4). La segmentación semántica, si bien conserva el contexto, introduce un costo computacional adicional que no se justifica en este caso, pues la información de las hojas de vida posee una estructura que puede aprovecharse directamente: cada formación, proyecto, publicación o experiencia constituye una unidad lógica independiente.

### 2.5 Modelo de Embeddings

El modelo de embeddings convierte el texto en representaciones vectoriales sobre las cuales se realiza la búsqueda semántica. Dado que el corpus corresponde a hojas de vida en idioma español y que el requisito HU-09 exige relacionar denominaciones equivalentes, el modelo debe ofrecer un desempeño adecuado en dicho idioma.

El conjunto de modelos comparados se delimita de acuerdo con las siguientes familias, con el fin de representar el espectro de decisiones relevantes para el proyecto:

1. **El modelo heredado** (`all-MiniLM-L6-v2`), que representa la familia de modelos compactos de propósito general con orientación al inglés. Se incluye para evidenciar la comparación con la solución existente y justificar su sustitución.
2. **Los modelos multilingües orientados a recuperación** (`intfloat/multilingual-e5-base`), que representan la familia entrenada específicamente para búsqueda en múltiples idiomas.
3. **Los modelos multilingües con capacidad híbrida** (`BAAI/bge-m3`), que además del vector denso generan representaciones esparsas útiles para la búsqueda léxica.
4. **Los modelos específicos de español** (`jina-embeddings-v2-base-es`), que representan la familia especializada en el idioma del corpus.

Quedan excluidas de la comparación las APIs propietarias de embeddings (OpenAI, Cohere), por implicar un costo recurrente incompatible con el criterio C9.

| Modelo | Dimensiones | Desempeño en español | Costo en CPU | Decisión |
|---|---|---|---|---|
| `all-MiniLM-L6-v2` | 384 | Limitado | Bajo | Descartado |
| **`intfloat/multilingual-e5-base`** | 768 | Adecuado | Moderado | Seleccionado |
| `BAAI/bge-m3` | 1024 | Adecuado | Alto | Alternativa |
| `jina-embeddings-v2-base-es` | 768 | Alto (solo español) | Moderado | Alternativa |

Se selecciona el modelo **`intfloat/multilingual-e5-base`**, por representar un equilibrio entre la calidad de las representaciones multilingües (criterio C1) y el costo de procesamiento en CPU (criterio C8), sin costo de licenciamiento (criterio C9). El modelo `bge-m3` ofrece mayor dimensionalidad y capacidad híbrida, pero su costo en CPU es superior; dado que la componente léxica se resuelve mediante la búsqueda híbrida de la base de datos vectorial (sección 2.6), no se considera necesario asumir ese costo adicional. El modelo `jina` queda como alternativa específica de español si en etapas posteriores se evidencia una mejora de desempeño que lo justifique.

### 2.6 Base de Datos Vectorial

La base de datos vectorial almacena las representaciones generadas y permite ejecutar las consultas de recuperación. Los requisitos HU-04 y HU-05 imponen dos condiciones determinantes: el filtrado por atributos del investigador y la búsqueda temática sobre el conjunto de la información.

| Base de datos | Filtrado por metadatos | Búsqueda híbrida | Persistencia | Decisión |
|---|---|---|---|---|
| Chroma | Limitado | No nativa | Sí | Alternativa |
| **Qdrant** | Nativo | Nativa | Sí | Seleccionada |
| FAISS | No | No | No | Descartada |
| Weaviate | Nativo | Nativa | Sí | Alternativa |

Se selecciona **Qdrant**. Los argumentos que sustentan esta decisión son los siguientes:

- Proporciona filtrado nativo por metadatos, lo que permite restringir la búsqueda por autor y por sección (criterio C2) sin necesidad de recuperar la totalidad de la colección para filtrarla en memoria.
- Soporta búsqueda híbrida, que combina la recuperación semántica con la recuperación léxica; esta característica resulta necesaria para relacionar acrónimos y variantes de escritura sin generar falsas equivalencias (criterios C1 y C3).
- FAISS se descarta por carecer de filtrado por metadatos y de persistencia nativa. Weaviate ofrece capacidades similares a Qdrant, pero implica una mayor complejidad operativa sin una ventaja equivalente para este caso de uso.

### 2.7 Modelo de Lenguaje

El modelo de lenguaje es responsable de la generación de las respuestas a partir del contexto recuperado. Se consideran dos familias de alternativas: las APIs propietarias y los modelos abiertos de ejecución local.

| Modelo | Tipo | Costo | Reproducibilidad | Decisión |
|---|---|---|---|---|
| **`gemini-3.8-flash` (versión fija)** | API propietaria | Gratuito | Alta | Seleccionado |
| `gemini-flash-latest` | API propietaria | Gratuito | Baja (alias móvil) | Descartado |
| `gpt-4o-mini` | API propietaria | De pago | Alta | Descartado |
| `claude-3-5-haiku` | API propietaria | De pago | Alta | Descartado |
| Llama / Mistral (Ollama) | Abierto local | Gratuito | Alta | Alternativa |

Se selecciona **`gemini-3.8-flash`** en una versión fija. Los argumentos que sustentan la decisión son los siguientes:

- Es la única alternativa de acceso gratuito dentro de las APIs propietarias, lo que la hace compatible con el criterio C9.
- El uso de una versión fija, en contraposición al alias `latest`, garantiza la estabilidad del modelo a lo largo del tiempo y, por tanto, la reproducibilidad del experimento (criterio C10).
- Las alternativas `gpt-4o-mini` y `claude-3-5-haiku` se descartan por implicar un costo recurrente.
- Los modelos abiertos locales (Llama, Mistral) se documentan como alternativa, dado que refuerzan el criterio de software libre y reducen la dependencia de un proveedor externo; sin embargo, su viabilidad está limitada por el procesamiento en CPU (criterio C8), que restringe el uso a modelos de tamaño reducido.

### 2.8 Framework de Orquestación RAG

El sistema requiere integrar la recuperación de información con la generación de respuestas. Para esta integración se consideran las siguientes alternativas:

| Enfoque | Integraciones disponibles | Riesgo de acoplamiento | Decisión |
|---|---|---|---|
| LangChain | Amplias (Qdrant, embeddings, LLM) | Medio | Descartado |
| LlamaIndex | Amplias (orientado a datos) | Medio | Descartado |
| **Implementación propia** | Directas (qdrant-client, sentence-transformers, google-genai) | Bajo | Seleccionada |

Se selecciona la **implementación propia mediante adaptadores directos**. Los argumentos son los siguientes:

- Las interfaces definidas en el dominio (`IVectorStore`, `IEmbeddingProvider`, `ILLMProvider`) ya proporcionan la abstracción necesaria para integrar los componentes; un framework de orquestación adicional resulta redundante.
- El uso directo de `qdrant-client`, `sentence-transformers` y `google-genai` reduce el número de dependencias y evita el acoplamiento a una capa intermedia.
- LangChain y LlamaIndex se descartan porque, si bien ofrecen integraciones estandarizadas, introducen una capa de abstracción que no aporta valor frente a las interfaces propias y aumenta la superficie de dependencias (criterio C11).

### 2.9 Normalización de Acrónimos

El requisito HU-09 establece que el sistema debe relacionar acrónimos y denominaciones equivalentes, pero a la vez impone una condición restrictiva: no debe considerar como equivalentes dos términos cuando no exista evidencia suficiente de que hacen referencia a la misma entidad.

Esta condición descarta la expansión libre de sinónimos. En su lugar, se selecciona una estrategia de **normalización basada en evidencia**, en la cual las equivalencias (por ejemplo, entre una sigla institucional y su nombre completo) se derivan de los propios registros del corpus y se aplican como un paso previo tanto a la indexación como a la consulta.

### 2.10 Gestión del Contexto Conversacional

El requisito HU-07 establece que el sistema debe conservar el contexto de las últimas interacciones para dar continuidad al análisis. Se consideran las siguientes alternativas para el almacenamiento del contexto:

| Mecanismo | Persistencia | Aislamiento por sesión | Complejidad | Decisión |
|---|---|---|---|---|
| **En memoria por sesión** | No (volátil) | Sí | Baja | Seleccionado |
| Base de datos relacional (SQLite) | Sí | Sí | Media | Alternativa |
| Redis | Sí | Sí | Media | Alternativa |

Se selecciona el **almacenamiento en memoria por sesión**, de modo que cada interacción conserve su propio contexto de manera aislada. Esta decisión responde a la necesidad de atender múltiples usuarios sin que los historiales se mezclen, y de hacerlo mediante una abstracción que permita reemplazar el mecanismo de almacenamiento sin afectar la lógica de negocio (criterio C11). La persistencia en SQLite o Redis se documenta como evolución si en etapas posteriores se requiere conservar el historial entre ejecuciones.

### 2.11 Calidad de Código y Pruebas

Para garantizar la mantenibilidad del código (criterio C11) y la verificación del sistema, se seleccionan las siguientes herramientas:

| Herramienta | Propósito | Decisión |
|---|---|---|
| **Ruff** | Análisis estático y formato de código | Seleccionado |
| **mypy** | Verificación de tipos | Seleccionado |
| **pytest** | Ejecución de pruebas unitarias y de integración | Seleccionado |

Se selecciona **Ruff** como herramienta unificada de formato y análisis estático, por su desempeño y por consolidar en una sola herramienta funciones que tradicionalmente requieren varias (black, isort, flake8). Se complementa con **mypy** para la verificación de tipos, dado que el proyecto adopta tipado estático mediante Pydantic. **pytest** se selecciona para la ejecución de las pruebas, por ser el estándar del ecosistema Python.

### 2.12 Evaluación

La verificación del sistema requiere un mecanismo de evaluación de la recuperación y de la generación. Se seleccionan las siguientes métricas y herramientas:

| Herramienta | Qué evalúa | Decisión |
|---|---|---|
| **recall@k y MRR** | Calidad de la recuperación | Seleccionado |
| **RAGAS** | Fidelidad y relevancia de la generación | Alternativa |

Se seleccionan las métricas **recall@k** (capacidad de recuperar los documentos relevantes) y **MRR** (Mean Reciprocal Rank, que evalúa la posición del primer resultado relevante) como mecanismo principal de evaluación, aplicadas sobre el conjunto de consultas de prueba definidas en el documento de requisitos. **RAGAS** se documenta como alternativa para evaluar la calidad de la generación cuando se disponga de un conjunto de referencia anotado.

## 3. Resumen de las Decisiones

En la siguiente tabla se presentan los resultados obtenidos luego del proceso de análisis y selección.

| Componente | Herramienta seleccionada | Criterios atendidos |
|---|---|---|
| Framework servidor | FastAPI + Uvicorn | C4, C9 |
| Framework cliente | React + Vite | C9, C11 |
| Despliegue | Docker + Docker Compose | C10 |
| Gestión de dependencias | venv + pip | C9 |
| Segmentación | Por unidad lógica | C1, C4 |
| Modelo de embeddings | `intfloat/multilingual-e5-base` | C1, C8, C9 |
| Base de datos vectorial | Qdrant | C1, C2, C3 |
| Modelo de lenguaje | `gemini-3.8-flash` (versión fija) | C9, C10 |
| Orquestación RAG | Implementación propia (adaptadores directos) | C11 |
| Normalización | Basada en evidencia (acrónimos) | C1 |
| Contexto conversacional | En memoria por sesión | C6, C11 |
| Calidad de código | Ruff, mypy, pytest | C11 |
| Evaluación | recall@k y MRR | C4 |
