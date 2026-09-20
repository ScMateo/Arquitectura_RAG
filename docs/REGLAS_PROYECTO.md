# Reglas de Proyecto - Arquitectura_RAG (Sistema CvLAC)

> **Versión:** 1.0 | **Fecha:** 2026-09-19 | **Stack:** Python 3.12 + FastAPI + ChromaDB + Gemini + React 19 + Vite
> Este documento es **normativo**. Todo PR que no cumpla será rechazado. Define cómo se estructura el código, cómo se nombra y cómo se comenta para garantizar SOLID, mantenibilidad y trazabilidad con las HU-01 a HU-10.

---

## 1. Objetivo y Alcance

Sistema RAG como alternativa al buscador tradicional de CvLAC. Debe cumplir:
- **HE.001 Interfaz:** HU-01, HU-02
- **HE.002 Funcionalidad:** HU-03 (links), HU-08 (resumen), HU-10 (referenciación)
- **HE.003 Consultas:** HU-04 (específica), HU-05 (general)
- **HE.004 Razonamiento:** HU-06 (libre), HU-07 (historial 10 + análisis), HU-09 (acrónimos)

Cualquier cambio debe mapear explícitamente a una HU y a una tarea del backlog del Excel.

---

## 2. Estructura Estándar (Clean Architecture)

```
Arquitectura_RAG/
├── backend/app/
│   ├── core/               # Config, settings, excepciones base. Sin dependencias hacia afuera
│   ├── api/v1/endpoints/   # Solo HTTP: parsing, validación Pydantic, inyección de dependencias
│   ├── domain/
│   │   ├── entities/       # Entidades puras (Researcher, Document, Chunk). Sin imports de infra
│   │   ├── value_objects/  # CvLACUrl, ResearchArea (inmutables, validación)
│   │   └── interfaces/     # Puertos: IVectorStore, ILLMProvider, IIngestor, IRepository
│   ├── application/
│   │   ├── dto/            # Schemas de entrada/salida (Request/Response)
│   │   ├── services/       # Lógica de orquestación reutilizable
│   │   └── use_cases/      # Un caso por historia: ChatUseCase, SummarizeUseCase, CiteSourcesUseCase
│   ├── infrastructure/     # Adaptadores (implementan domain/interfaces)
│   │   ├── vectorstore/    # ChromaAdapter
│   │   ├── llm/            # GeminiAdapter
│   │   ├── ingestion/      # cleaner.py, chunker.py, normalizer.py (HU-09)
│   │   └── repositories/   # CvLACRepository
│   └── tests/unit|integration/
├── frontend/src/
│   ├── components/ui|layout/      # Dumb components (Button, Card). Sin lógica de negocio
│   ├── features/chat/             # Feature aislada (vertical slice)
│   │   ├── components/            # ChatWindow, ChatInput, SourceList, SummaryToggle
│   │   ├── hooks/                 # useChat, useConversationHistory
│   │   └── services/              # chatApi.ts
│   ├── services/ | hooks/ | types/ | utils/
├── data/raw|processed/
└── scripts/ | docs/
```

**Regla de dependencias (DIP):** `api` -> `application` -> `domain` <- `infrastructure`. `domain` **nunca** importa de `infrastructure`. Si necesitas una librería externa, crea una interfaz en `domain/interfaces`.

---

## 3. Principios SOLID - Aplicación Práctica

| Principio | Regla Concreta | Ejemplo |
|-----------|----------------|---------|
| **S - Single Responsibility** | 1 archivo = 1 responsabilidad. Máx 200 líneas/archivo, 1 clase pública/archivo | `cleaner.py` solo limpia, no hace chunking. `ChatUseCase` solo orquesta, no llama directo a `Chroma` |
| **O - Open/Closed** | Abierto a extensión, cerrado a modificación. Usa Strategy/Adapter | Nuevo LLM = crear `OpenAIAdapter implements ILLMProvider`, no tocar `GenerationService` |
| **L - Liskov** | Cualquier implementación sustituye a la interfaz sin romper `use_cases` | `FAISSAdapter` y `ChromaAdapter` pasan los mismos tests de `IVectorStore` |
| **I - Interface Segregation** | Interfaces pequeñas y específicas | `ISearch`, `ISummarize` separadas, no `ILLM_GOD` con 10 métodos |
| **D - Dependency Inversion** | Los módulos de alto nivel dependen de abstracciones | `ChatUseCase` recibe `IVectorStore` por constructor (inyección), no `from chroma import Chroma` |

---

## 4. Convenciones de Nombres

### 4.1 Backend Python (PEP8)

| Elemento | Convención | Ejemplo Correcto | Incorrecto |
|----------|------------|------------------|------------|
| Archivo/Módulo | `snake_case.py` | `retrieval_service.py`, `acronym_normalizer.py` | `RetrievalService.py` |
| Clase | `PascalCase` | `Researcher`, `ChromaAdapter`, `ChatUseCase` | `researcher` |
| Interfaz/Protocolo | `I` + `PascalCase` | `IVectorStore`, `ILLMProvider` | `VectorStoreInterface` |
| Función/Método | `snake_case` verbo + sustantivo | `search_by_theme()`, `normalize_acronym()` | `Search()` |
| Variable | `snake_case` sustantiva | `researcher_name`, `filtered_docs` | `researcherName`, `x` |
| Constante | `UPPER_SNAKE_CASE` | `MAX_HISTORY = 10`, `CHUNK_SIZE = 1500` | `maxHistory` |
| DTO/Schema | `PascalCase` + `DTO`/`Request`/`Response` | `ChatRequestDTO`, `ChatResponse` | `chatRequest` |

### 4.2 Frontend TypeScript/React

| Elemento | Convención | Ejemplo |
|----------|------------|---------|
| Componente | `PascalCase.tsx` | `ChatWindow.tsx`, `SourceList.tsx` |
| Hook | `use` + `PascalCase` | `useChat.ts`, `useConversationHistory.ts` |
| Archivo servicio | `camelCase.ts` | `chatApi.ts` |
| Variable/Función | `camelCase` | `researcherName`, `fetchSources()` |
| Tipo/Interfaz | `PascalCase` | `ChatMessage`, `ResearcherProfile` |
| Constante | `UPPER_SNAKE_CASE` | `API_BASE_URL` |
| CSS Clase | `kebab-case` | `chat-window` |

### 4.3 Reglas Globales

- **Idioma:** Código y comentarios en **inglés**. Commits, PRs y docs pueden ser en **español**.
- **Sin abreviaturas ambiguas:** `researcher` no `res`, `document` no `doc` (excepto `doc` en domain si es claro).
- **Booleanos:** prefijo `is_`, `has_`, `should_` -> `is_retrieved`, `has_url`.
- **IDs:** `researcher_id`, `conversation_id` (no `id` solo).

---

## 5. Comentarios y Documentación - QUÉ debe contener

### 5.1 Regla de Oro

> **Comenta el POR QUÉ, no el QUÉ.** El código dice qué hace, el comentario explica por qué se hace así y qué HU/criterio cubre.

**Prohibido:**
```python
# Incrementa i en 1
i += 1
```

**Obligatorio:**
```python
# HU-09: Normaliza acrónimos antes de embedizar para evitar pérdida de recall
# "U.Nacional" y "Universidad Nacional" deben mapear al mismo vector
text = acronym_normalizer.normalize(text)
```

### 5.2 Docstrings Backend (Google Style)

Todo `public` (clase, método, función, módulo) lleva docstring.

```python
"""Use case para HU-04 y HU-05: consulta específica vs general.

Resuelve HE.003. Diferencia entre búsqueda por investigador
y búsqueda temática transversal.
"""

class ChatUseCase:
    """Orquesta retrieval + generation con citación HU-10.

    Attributes:
        vector_store: Puerto IVectorStore (DIP).
        llm_provider: Puerto ILLMProvider.
    """

    def execute(self, query: str, history: list[ChatMessage]) -> ChatResponse:
        """Ejecuta consulta RAG con historial conversacional HU-07.

        Args:
            query: Pregunta en lenguaje natural (HU-06 libre).
            history: Últimos 10 mensajes (criterio HU-07-4).

        Returns:
            ChatResponse con `answer` y `sources` (HU-10).

        Raises:
            RetrievalError: Si no se encuentran docs relevantes.
        """
```

- `__init__.py` de cada paquete lleva docstring de módulo explicando su responsabilidad SOLID.

### 5.3 JSDoc Frontend

```typescript
/**
 * HU-03 + HU-10: Muestra fuentes con link clickeable a CvLAC.
 * @param sources - Lista de { researcherName, url, section }
 * @returns Lista renderizada. Criterio HU-03-3: click redirige directo.
 */
export const SourceList = ({ sources }: Props) => {}
```

### 5.4 Comentarios Inline

- Usa `# TODO(HU-XX): descripción` para deuda mapeada a backlog.
- Usa `# FIXME: razón` solo con issue asociado.
- Cada hack necesita `# HACK: por qué es necesario y cuándo quitarlo`.

### 5.5 Commits y PRs

- **Conventional Commits:** `feat(HU-03): add CvLAC link rendering` , `fix(HU-09): normalize UNAL acronym`
- Mensaje debe referenciar HU/HE: `feat(domain): add IVectorStore - HE.003`
- PR template obligatorio:
  ```
  HU: HU-03, HU-10
  Qué: ...
  Por qué: ...
  Cómo probado: consultas de prueba p.7 (puntual #1)
  Checklist: [ ] tests, [ ] docstring, [ ] SOLID check
  ```

---

## 6. Código Limpio y Buenas Prácticas

1.  **Límite función:** < 30 líneas, < 3 parámetros. Si más, usa DTO.
2.  **Sin números mágicos:** `MAX_HISTORY = 10` en `core/constants.py`, no `[-10:]` suelto.
3.  **Manejo de errores:** No `except: pass`. Usa excepciones de dominio `DomainError`, `NotFoundError` en `core/exceptions.py`.
4.  **Logging:** Usa `logger.info("HU-07 history_len=%s", len(history))`, no `print`. Nivel `INFO` para flujo, `DEBUG` para vectores.
5.  **Config:** Nunca hardcodear `GOOGLE_API_KEY`, `CHROMA_PATH`. Usa `core/config.py` con `pydantic-settings` + `.env`.
6.  **Formato:** `black`, `isort`, `flake8`, `mypy --strict` (backend) | `eslint + prettier` (frontend). Se ejecuta en pre-commit.
7.  **Sin código muerto:** Si no se usa, se borra. No `frontend_old`.

---

## 7. Backend - Reglas Específicas

- **Endpoints:** Solo en `api/v1/endpoints/`. Un archivo por recurso `chat.py`, `health.py`. No lógica de negocio aquí, solo `use_case.execute()`.
- **Validación:** Todo `Request` con `Pydantic BaseModel` con `Field(description=...)`.
- **Inyección:** Usa `FastAPI Depends` para inyectar `IVectorStore`.
- **Ingesta:** `infrastructure/ingestion/` debe ser idempotente. `cleaner.py` (HU-09 normaliza), `chunker.py` (estrategia `RecursiveCharacter` con `chunk_size=1500, overlap=500` documentada), `indexer.py`.

## 8. Frontend - Reglas Específicas

- **Componentes:** `components/ui` son dumb (solo props). `features/chat/components` son smart (usan hooks).
- **Estado:** `useConversationHistory` guarda 10 mensajes (HU-07-4) en `localStorage` + memoria. No global mutable.
- **API:** Todo fetch en `services/chatApi.ts`, no en componentes. Tipado `ChatRequest/ChatResponse`.
- **Links:** HU-03-2: URL completo visible y copiable. Usa `<a href={url} target="_blank" rel="noopener">`.

## 9. Testing (Obligatorio por HU)

- **Ubicación:** `backend/tests/unit` (mocks de puertos) y `tests/integration` (Chroma real efímero).
- **Consultas de prueba (p.7 doc):** Cada PR que toque retrieval debe pasar las 20 consultas (puntuales, generales, relacionales, comparativas) como test parametrizado.
- **Cobertura mínima:** 80% en `domain` y `application`.

## 10. Git y Flujo

```
main (protegida)
  └── feature/HU-03-links
  └── fix/HU-09-acronyms
  └── docs/reglas-proyecto
```

- **Ramas:** `feature/HU-XX-descripcion`, `fix/HU-XX`, `docs/...`
- **No push directo a `main`.** Siempre PR con 1 aprobación.
- **`.gitignore` obligatorio:** `venv/`, `__pycache__/`, `.env`, `data/processed/chroma.sqlite3`, `frontend/node_modules/`, `dist/`.

## 11. Checklist Antes de Merge

- [ ] ¿Mapea a HU/HE y tarea del Excel?
- [ ] ¿Sigue Clean Architecture (sin import circular)?
- [ ] ¿Nombres según §4?
- [ ] ¿Docstring Google/JSDoc con Args/Returns/HU?
- [ ] ¿Tests de las 20 consultas si toca RAG?
- [ ] ¿`black && mypy && pytest` pasa?
- [ ] ¿No expone `.env` ni `GOOGLE_API_KEY`?
- [ ] ¿Frontend muestra `sources` con URL (HU-10) si aplica?

---

## 12. Referencias

- PEP8, Google Python Style Guide
- Clean Architecture (Robert C. Martin)
- Conventional Commits
- Criterios de aceptación HU-01 a HU-10 (doc Word)

> **Próximo paso:** Crear `CONTRIBUTING.md` corto que apunte aquí y `scripts/lint.sh` para validar automáticamente.
