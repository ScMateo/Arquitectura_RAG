# Arquitectura_RAG — Sistema CvLAC

Sistema de Recuperación Aumentada por Generación (RAG) que responde preguntas
sobre hojas de vida de investigadores registradas en CvLAC, como alternativa a
un buscador tradicional.

- Documento normativo del proyecto: `docs/REGLAS_PROYECTO.md`.
- Configuración del sistema: `backend/app/core/config.py` y `.env.example`.
- Plan de validación y métricas: `docs/PLAN_VALIDACION.md`.

## Requisitos

| Herramienta | Versión usada | Necesaria para |
|---|---|---|
| Python | 3.12 | Backend, ingesta y evaluación |
| Docker + Docker Compose | Docker 29.x | Base vectorial Qdrant |
| Clave de API de Google (Gemini) | — | Clasificación y generación (LLM) |
| Node.js | 18+ (opcional) | Frontend (aún no implementado) |

Recursos: ~2 GB de RAM libre (el modelo de embeddings `multilingual-e5-base`
corre en CPU).

## Estructura

```
Arquitectura_RAG/
├── backend/
│   ├── app/                 # Backend (Clean Architecture: api → application → domain ← infrastructure)
│   ├── evaluation/          # Harness de evaluación (corpus, casos, métricas, instrumentación)
│   ├── tests/               # Suite de pruebas (unit / integration)
│   └── requirements.txt
├── data/
│   ├── sample/              # CSV de ejemplo (contrato de datos)
│   └── processed/           # Artefactos generados (corpus de evaluación, resultados) — no versionado
├── docs/                    # Documentación y reglas del proyecto
├── scripts/
│   ├── index.py             # CLI de indexación de un CSV
│   └── evaluate.py          # CLI del harness de evaluación
├── frontend/                # Frontend (pendiente, Fase 5)
└── docker-compose.yml       # Qdrant
```

## Inicio rápido (WSL/Linux/macOS)

```bash
# 1. Clonar el repositorio
git clone https://github.com/ScMateo/Arquitectura_RAG.git
cd Arquitectura_RAG

# 2. Levantar Qdrant (base vectorial)
docker compose up -d          # quedará en http://localhost:6333

# 3. Entorno de Python
python3.12 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# 4. Configuración (edita GOOGLE_API_KEY; el resto trae defaults)
cp .env.example .env

# 5. Indexar un CSV conforme al contrato de datos
PYTHONPATH=backend python scripts/index.py data/sample/investigadores.csv

# 6. Arrancar el backend
PYTHONPATH=backend python -m uvicorn app.main:app --reload --port 8000
```

> En Windows (PowerShell) usa `py -3.12 -m venv venv`, activa con
> `venv\Scripts\Activate.ps1` y exporta la variable con
> `$env:PYTHONPATH = "backend"` antes de los comandos que la requieren.

### Verificar que funciona

```bash
curl http://localhost:8000/health          # {"status":"ok"}

curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Quién ha investigado sobre salud pública?"}'
```

### Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/health` | Estado del servicio |
| `POST` | `/api/chat` | Pregunta–respuesta (retrieval + generación) |
| `POST` | `/api/chat/stream` | Igual que `/api/chat` pero en *streaming* (SSE) |

Cuerpo de las peticiones de chat: `{"message": "...", "session_id": "opcional"}`.

## Calidad y pruebas

```bash
# Pruebas (desde backend/, el pytest.ini fija pythonpath=.)
cd backend && python -m pytest && cd ..

# Lint y tipado (desde la raíz)
ruff check backend/app backend/evaluation
cd backend && mypy app evaluation && cd ..
```

Las pruebas de integración requieren un Qdrant en ejecución y se omiten
automáticamente si no está disponible. Los umbrales de calidad son los de
`docs/REGLAS_PROYECTO.md` (cobertura ≥ 80 % en `domain` y `application`).

## Evaluación

El harness mide recuperación, generación y desempeño sobre un corpus sintético
de 50 investigadores y 40 casos (ver `docs/PLAN_VALIDACION.md`).

```bash
# Corrida completa (requiere cuota de la API del LLM)
PYTHONPATH=backend python scripts/evaluate.py

# Con el juez LLM de generación (faithfulness / relevancy / correctness)
PYTHONPATH=backend python scripts/evaluate.py --judge

# Subconjunto estratificado (p. ej. 2 casos por tipo = 10 casos), útil con la cuota gratuita
PYTHONPATH=backend python scripts/evaluate.py --per-kind 2

# Modo offline sin cuota (LLM simulado): valida la mecánica y las métricas de recuperación
PYTHONPATH=backend python scripts/evaluate.py --stub-llm
```

Opciones: `--corpus`, `--output`, `--collection`, `--judge`, `--per-kind`,
`--limit`, `--thresholds`, `--stub-llm`. Los resultados se escriben en
`data/processed/evaluation_results.csv`.

> **Cuota de la API.** El nivel gratuito de `gemini-3.8-flash` permite ≈ 20
> solicitudes por día y cada caso consume 2 (sin juez) o 3 (con juez). Para la
> corrida completa de 40 casos se requiere una clave con facturación habilitada.

## Datos

El sistema consume un CSV con el contrato de 23 columnas separadas por `|`
(UTF-8 sin BOM). Detalles y obligatoriedad de columnas en
`docs/REGLAS_DATOS_CSV.md`. `data/sample/investigadores.csv` es un ejemplo
mínimo; `backend/evaluation/corpus.py` genera el corpus sintético de evaluación.

## Notas

- **Nunca** subas `.env` al repositorio: ya está en `.gitignore`. Usa
  `.env.example` como plantilla.
- Todo PR debe referenciar una Historia de Usuario (HU) y pasar
  `ruff`, `mypy` y `pytest` (checklist en `docs/REGLAS_PROYECTO.md` §11).
- El frontend (`frontend/`) todavía no está implementado (Fase 5).
