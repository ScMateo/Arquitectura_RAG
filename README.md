# Arquitectura_RAG - Sistema CvLAC (Alternativa al buscador tradicional)

Ver `docs/REGLAS_PROYECTO.md` (normativo) y `backend/app/core/config.py`.

## Inicio rápido (WSL)

```bash
# 1. Clonar y entorno
git clone <repo> && cd Arquitectura_RAG
python -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt

# 2. Config
cp .env.example .env  # edita GOOGLE_API_KEY

# 3. Ingesta (genera data/processed/chroma)
python -m backend.app.infrastructure.ingestion.indexer

# 4. Backend
uvicorn backend.app.main:app --reload --port 8000

# 5. Frontend (otra terminal)
cd frontend && npm install && npm run dev
```

## Estructura

Ver `docs/REGLAS_PROYECTO.md:20` - Clean Architecture + SOLID + Feature-Sliced.

## Reglas

Todo PR debe referenciar HU/HE y pasar `black, mypy, pytest` (ver REGLAS_PROYECTO.md §11 checklist).
