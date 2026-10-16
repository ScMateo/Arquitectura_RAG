# Diseño Detallado de la Arquitectura Modular del Sistema

En el siguiente documento se presenta el diseño detallado de la arquitectura modular del sistema. Este diseño sintetiza las decisiones adoptadas en las etapas previas (selección de herramientas, infraestructura, requerimientos de recuperación, estrategia de segmentación y optimización) y las traduce en una estructura de módulos con responsabilidades definidas, interfaces explícitas y flujos de operación.

El diseño se organiza en tres partes: la estructura estática (capas, módulos e interfaces), los flujos dinámicos (preparación, recuperación y generación) y el despliegue.

## 1. Principios de Diseño

El diseño se rige por la arquitectura limpia y por los principios SOLID:

- **Separación en capas**: la capa de API depende de la aplicación, la aplicación depende del dominio, y la infraestructura implementa las interfaces del dominio.
- **Inversión de dependencias (DIP):** la lógica de negocio depende de abstracciones (puertos), nunca de implementaciones concretas. Esto permite sustituir la base vectorial, el modelo de lenguaje o el modelo de embeddings sin modificar los casos de uso.
- **Responsabilidad única:** cada módulo tiene una única responsabilidad y se comunica con los demás a través de interfaces.

## 2. Arquitectura por Capas

El sistema se organiza en cuatro capas: API, aplicación, dominio e infraestructura.

```mermaid
flowchart TB
    subgraph API["Capa API (api/v1/endpoints)"]
        A1["chat.py"]
        A2["health.py"]
    end

    subgraph APP["Capa de Aplicación (application)"]
        B1["use_cases"]
        B2["services"]
        B3["dto"]
    end

    subgraph DOM["Capa de Dominio (domain)"]
        C1["entities"]
        C2["value_objects"]
        C3["interfaces (puertos)"]
    end

    subgraph INF["Capa de Infraestructura (infrastructure)"]
        D1["vectorstore / QdrantAdapter"]
        D2["llm / GeminiAdapter"]
        D3["embeddings / HuggingFaceAdapter"]
        D4["ingestion"]
        D5["repositories"]
        D6["conversation"]
    end

    API --> APP
    APP --> DOM
    INF --> DOM
```

La regla de dependencia indica que `api -> application -> domain <- infrastructure`. La capa de dominio no importa de la infraestructura, la infraestructura implementa los puertos definidos en el dominio.

## 3. Módulos del Sistema

### 3.1 Capa de Dominio

| Módulo | Responsabilidad |
|---|---|
| `entities` | Modelos puros: `Researcher`, `Chunk`, `Message`, `Conversation`, `Source` |
| `value_objects` | Objetos inmutables con validación: `CvLACUrl`, `Section`, `QueryType` |
| `interfaces` | Puertos: `IVectorStore`, `IEmbeddingProvider`, `ILLMProvider`, `IIngestor`, `IConversationStore`, `INormalizer`, `IChunker`, `IReranker` |

### 3.2 Capa de Aplicación

| Módulo | Responsabilidad |
|---|---|
| `dto` | Contratos de entrada y salida: `ChatRequest`, `ChatResponse`, `Source`, `RetrievalResult` |
| `services` | Orquestación reutilizable: `RetrievalService`, `GenerationService` |
| `use_cases` | Casos de uso: `ChatUseCase` (HU-04/05), `SummarizeUseCase` (HU-08), `CiteSourcesUseCase` (HU-10) |

### 3.3 Capa de Infraestructura

| Módulo | Responsabilidad | Implementa |
|---|---|---|
| `vectorstore` | `QdrantAdapter`: búsqueda híbrida, filtrado por metadatos, indexación | `IVectorStore` |
| `llm` | `GeminiAdapter`: generación, clasificación, streaming, caché de contexto | `ILLMProvider` |
| `embeddings` | `HuggingFaceAdapter`: generación de embeddings con prefijos | `IEmbeddingProvider` |
| `ingestion` | `CsvReader`, `Cleaner`, `Chunker`, `Normalizer`, `Indexer` | `IIngestor`, `IChunker`, `INormalizer` |
| `repositories` | `CvLACRepository`: acceso a los datos de origen | — |
| `conversation` | `InMemoryConversationStore`: contexto por sesión | `IConversationStore` |

### 3.4 Capa de API

| Módulo | Responsabilidad |
|---|---|
| `chat.py` | Endpoint `POST /api/chat`: recibe la consulta, inyecta dependencias, invoca el caso de uso |
| `health.py` | Endpoint `GET /health`: verificación de disponibilidad |

## 4. Interfaces y Adaptadores (DIP)

La inversión de dependencias se materializa en el vínculo entre los puertos del dominio y sus adaptadores en la infraestructura.

```mermaid
flowchart LR
    subgraph DOM["Dominio — interfaces (puertos)"]
        P1["IVectorStore"]
        P2["IEmbeddingProvider"]
        P3["ILLMProvider"]
        P4["IIngestor"]
        P5["IConversationStore"]
        P6["INormalizer"]
        P7["IChunker"]
        P8["IReranker"]
    end

    subgraph INF["Infraestructura — adaptadores"]
        Q1["QdrantAdapter"]
        Q2["HuggingFaceAdapter"]
        Q3["GeminiAdapter"]
        Q4["CsvIngestor"]
        Q5["InMemoryConversationStore"]
        Q6["AcronymNormalizer"]
        Q7["LogicalUnitChunker"]
        Q8["WeightedReranker"]
    end

    Q1 -.->|implementa| P1
    Q2 -.->|implementa| P2
    Q3 -.->|implementa| P3
    Q4 -.->|implementa| P4
    Q5 -.->|implementa| P5
    Q6 -.->|implementa| P6
    Q7 -.->|implementa| P7
    Q8 -.->|implementa| P8
```

## 5. Flujos del Sistema

### 5.1 Flujo de Preparación (Ingesta)

Transforma los archivos CSV en fragmentos indexados en la base vectorial.

```mermaid
flowchart LR
    A["CSV (23 columnas)"] --> B["CsvReader"]
    B --> C["Cleaner"]
    C --> D["AcronymNormalizer"]
    D --> E["LogicalUnitChunker"]
    E --> F["HuggingFaceAdapter<br/>(prefijo passage:)"]
    F --> G["QdrantAdapter"]
    G --> H["Qdrant (índice + metadatos)"]
```

Etapas:

1. **Lectura:** el `CsvReader` lee el archivo conforme al contrato de datos y produce una entidad `Researcher` por fila.
2. **Limpieza:** el `Cleaner` elimina caracteres de control y normaliza el texto.
3. **Normalización:** el `AcronymNormalizer` resuelve acrónimos mediante el mapeo basado en evidencia (HU-09).
4. **Segmentación:** el `LogicalUnitChunker` divide cada sección por unidad lógica, con límite de tamaño.
5. **Embeddings:** el `HuggingFaceAdapter` genera los vectores aplicando el prefijo `passage:`.
6. **Indexación:** el `QdrantAdapter` almacena los fragmentos con metadatos de autor, sección y enlace.

### 5.2 Flujo de Recuperación

Recupera los fragmentos más relevantes para una consulta.

```mermaid
flowchart LR
    A["Consulta"] --> B["AcronymNormalizer"]
    B --> C["QueryClassifier<br/>(LLM, salida estructurada)"]
    C --> D["HuggingFaceAdapter<br/>(prefijo query:)"]
    D --> E["QdrantAdapter<br/>(híbrida + filtro)"]
    E --> F["WeightedReranker"]
    F --> G["Fragmentos seleccionados"]
```

Etapas:

1. **Normalización:** se resuelven acrónimos de la consulta (HU-09).
2. **Clasificación:** el `QueryClassifier` determina si la consulta es específica (un investigador) o general (temática), mediante salida estructurada (HU-04/05).
3. **Embedding:** se genera el vector de la consulta con el prefijo `query:`.
4. **Búsqueda:** el `QdrantAdapter` ejecuta la búsqueda híbrida, aplicando filtrado por metadatos cuando la consulta es específica.
5. **Re-ranking:** el `WeightedReranker` ordena los fragmentos por relevancia y prioridad de sección.

### 5.3 Flujo de Generación

Genera la respuesta a partir del contexto recuperado.

```mermaid
flowchart LR
    A["Contexto (fragmentos + historial)"] --> B["PromptBuilder"]
    B --> C["GeminiAdapter<br/>(streaming, caché de contexto)"]
    C --> D["Respuesta"]
    C --> E["Fuentes (HU-10)"]
```

Etapas:

1. **Composición del prompt:** el `PromptBuilder` combina la instrucción de sistema, el contexto recuperado, el historial conversacional y la consulta.
2. **Generación:** el `GeminiAdapter` genera la respuesta de manera incremental, con caché del prefijo del sistema y reintentos con espera exponencial.
3. **Trazabilidad:** se extraen las fuentes empleadas para acompañar la respuesta (HU-10).

### 5.4 Flujo Completo (End-to-End)

```mermaid
sequenceDiagram
    participant U as Usuario (Frontend)
    participant A as API (chat.py)
    participant C as ChatUseCase
    participant R as RetrievalService
    participant N as AcronymNormalizer
    participant Q as QueryClassifier
    participant E as HuggingFaceAdapter
    participant V as QdrantAdapter
    participant W as WeightedReranker
    participant G as GenerationService
    participant L as GeminiAdapter
    participant S as ConversationStore

    U->>A: POST /api/chat {message}
    A->>C: execute(message, session)
    C->>R: retrieve(message)
    R->>N: normalize(message)
    N-->>R: consulta normalizada
    R->>Q: classify(consulta)
    Q-->>R: tipo de consulta
    R->>E: embed(consulta)
    E-->>R: vector de consulta
    R->>V: search(vector, filtro)
    V-->>R: fragmentos candidatos
    R->>W: rerank(fragmentos)
    W-->>R: fragmentos ordenados
    R-->>C: contexto
    C->>G: generate(contexto, historial, consulta)
    G->>L: generar (streaming)
    L-->>G: respuesta
    G-->>C: respuesta + fuentes
    C->>S: guardar mensajes (HU-07)
    C-->>A: ChatResponse
    A-->>U: respuesta con fuentes
```

## 6. Despliegue

El sistema se empaqueta con Docker Compose en tres servicios.

```mermaid
flowchart TB
    subgraph FRONT["Cliente"]
        F1["React (Vite)"]
    end

    subgraph BACK["Servidor"]
        B1["FastAPI + Uvicorn"]
        B2["Capa de aplicación y dominio"]
    end

    subgraph DATA["Servicios de datos"]
        D1["Qdrant (contenedor)"]
    end

    EXT["Gemini API (internet)"]

    F1 -->|HTTP /api/chat| B1
    B1 --> B2
    B1 -->|gRPC/HTTP| D1
    B1 -->|HTTPS| EXT
```

La separación en servicios (cliente, servidor y servicio vectorial) mantiene un acoplamiento bajo y permite incorporar, en etapas posteriores, la medición del comportamiento del sistema sobre la red.
