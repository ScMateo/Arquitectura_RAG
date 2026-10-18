"""Core configuration (S: Single Responsibility, DIP).

Centraliza toda la configuración del sistema RAG CvLAC.
Resuelve REGLAS_PROYECTO.md §6.5: nunca hardcodear keys/paths.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# .env en la raíz del proyecto (Arquitectura_RAG/), independiente del CWD.
_ENV_FILE = Path(__file__).resolve().parents[3] / ".env"


class Settings(BaseSettings):
    """Configuración única del sistema. Lee .env una sola vez.

    Attributes:
        google_api_key: SecretStr para no exponer en logs.
        qdrant_url: URL del servidor Qdrant.
        qdrant_collection: Nombre de la colección vectorial.
        embedding_model_name: Modelo de embeddings (Liskov: intercambiable).
        embedding_device: Dispositivo de ejecución del modelo de embeddings.
        gemini_model: Modelo generativo, con versión fija por reproducibilidad.
        llm_timeout_ms: Límite de tiempo por solicitud al modelo (ms).
        llm_temperature_analysis: Temperatura para la clasificación de consultas.
        llm_temperature_generation: Temperatura para la generación de respuestas.
        chunk_size: Límite máximo de tamaño de una unidad lógica.
        max_history: Ventana conversacional (HU-07-4: mínimo 5, se adopta 10).
        top_k_retrieval: Fragmentos recuperados en la búsqueda.
        top_k_final: Fragmentos finales enviados al modelo.
        cors_origins: Orígenes permitidos del frontend.
    """

    # --- LLM / API Keys ---
    google_api_key: SecretStr = Field(
        ...,
        alias="GOOGLE_API_KEY",
        description="API key de Google Gemini. Obligatoria.",
    )

    # --- Vector Store ---
    qdrant_url: str = Field(
        default="http://localhost:6333",
        alias="QDRANT_URL",
        description="URL del servidor Qdrant.",
    )
    qdrant_collection: str = Field(
        default="cvlac_researchers",
        alias="QDRANT_COLLECTION",
        description="Nombre de la colección vectorial.",
    )

    # --- Embeddings ---
    embedding_model_name: str = Field(
        default="intfloat/multilingual-e5-base",
        alias="EMBEDDING_MODEL_NAME",
    )
    embedding_device: str = Field(
        default="cpu",
        alias="EMBEDDING_DEVICE",
    )

    # --- LLM ---
    gemini_model: str = Field(
        default="gemini-3.8-flash",
        alias="GEMINI_MODEL",
        description="Modelo generativo con versión fija (reproducibilidad).",
    )

    # --- LLM optimization (METODOS_OPTIMIZACION.md) ---
    llm_timeout_ms: int = Field(
        default=60000,
        ge=1000,
        description="Límite de tiempo por solicitud al modelo (ms). Método: timeout.",
    )
    llm_temperature_analysis: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0,
        description="Temperatura para la clasificación de consultas (determinista).",
    )
    llm_temperature_generation: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Temperatura para la generación de respuestas (redacción natural).",
    )

    # --- RAG Strategy ---
    chunk_size: int = Field(default=1500, ge=500, le=4000)
    max_history: int = Field(default=10, ge=5, le=20, description="HU-07-4: mínimo 5, se adopta 10")
    top_k_retrieval: int = Field(default=20, ge=1, le=50)
    top_k_final: int = Field(default=15, ge=1, le=20)

    # --- API ---
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000, ge=1024, le=65535)
    cors_origins: list[str] = Field(default=["http://localhost:5173"])

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
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
    return Settings()  # type: ignore[call-arg]
