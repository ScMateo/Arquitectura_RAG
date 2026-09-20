"""Core configuration (S: Single Responsibility, DIP).

Centraliza toda la configuración del sistema RAG CvLAC.
Resuelve REGLAS_PROYECTO.md §6.5: nunca hardcodear keys/paths.

Mapea a HU-07 (MAX_HISTORY=10) y a la estrategia de chunking
definida en src/ingest_academico.py:22.
"""

from functools import lru_cache

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración única del sistema. Lee .env una sola vez.

    Attributes:
        google_api_key: SecretStr para no exponer en logs (HU-03/10 trazabilidad).
        chroma_persist_directory: Ruta donde se persiste Chroma (DIP: infra lo consume).
        embedding_model_name: Modelo HuggingFace para embeddings (Liskov: intercambiable).
        gemini_model: Modelo generativo (O: extensible a OpenAI sin tocar use_cases).
        max_history: Ventana conversacional HU-07-4 (10 mensajes).
        chunk_size: Tamaño de fragmento ingestion strategy.
        chunk_overlap: Solapamiento para no perder contexto entre chunks.
        cors_origins: Orígenes permitidos frontend.
    """

    # --- LLM / API Keys ---
    google_api_key: SecretStr = Field(
        ...,
        alias="GOOGLE_API_KEY",
        description="API key de Google Gemini. Obligatoria.",
    )

    # --- Vector Store ---
    chroma_persist_directory: str = Field(
        default="data/processed/chroma",
        alias="CHROMA_PERSIST_DIR",
        description="Directorio persistencia ChromaDB.",
    )
    embedding_model_name: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        alias="EMBEDDING_MODEL_NAME",
    )
    gemini_model: str = Field(
        default="gemini-flash-latest",
        alias="GEMINI_MODEL",
    )

    # --- RAG Strategy ---
    chunk_size: int = Field(default=1500, ge=500, le=4000)
    chunk_overlap: int = Field(default=500, ge=0, le=1000)
    max_history: int = Field(default=10, ge=1, le=20, description="HU-07-4: historial 10")
    top_k_retrieval: int = Field(default=20, ge=1, le=50)
    top_k_final: int = Field(default=15, ge=1, le=20)

    # --- API ---
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000, ge=1024, le=65535)
    cors_origins: list[str] = Field(default=["http://localhost:5173"])

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Factory cacheada (O: reutilizable, no relee .env por request).

    Uso vía FastAPI Depends:
        @app.get("/api/chat")
        def chat(settings: Settings = Depends(get_settings)): ...

    Returns:
        Instancia singleton de Settings validada.
    """
    return Settings()
