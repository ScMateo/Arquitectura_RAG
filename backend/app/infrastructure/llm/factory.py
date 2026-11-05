"""LLM provider factory (composition helper).

Selects the adapter declared in ``LLM_PROVIDER`` so that the composition roots
(FastAPI dependencies and the evaluation harness) stay free of provider
conditionals (Open/Closed: a new provider only adds an adapter and a branch
here).
"""

from ...core.config import Settings
from ...domain.interfaces.llm_provider import ILLMProvider
from .gemini_adapter import GeminiAdapter
from .groq_adapter import GroqAdapter


def build_llm_provider(settings: Settings) -> ILLMProvider:
    """Construye el adaptador del proveedor configurado.

    Args:
        settings: Configuración validada del sistema.

    Returns:
        Adaptador que implementa ``ILLMProvider``.

    Raises:
        ValueError: Si falta la API key del proveedor seleccionado.
    """
    if settings.llm_provider == "groq":
        if settings.groq_api_key is None:
            raise ValueError("GROQ_API_KEY es obligatoria cuando LLM_PROVIDER=groq.")
        return GroqAdapter(
            api_key=settings.groq_api_key.get_secret_value(),
            model=settings.groq_model,
            timeout_ms=settings.llm_timeout_ms,
            analysis_temperature=settings.llm_temperature_analysis,
            generation_temperature=settings.llm_temperature_generation,
        )

    if settings.google_api_key is None:
        raise ValueError("GOOGLE_API_KEY es obligatoria cuando LLM_PROVIDER=gemini.")
    return GeminiAdapter(
        api_key=settings.google_api_key.get_secret_value(),
        model=settings.gemini_model,
        timeout_ms=settings.llm_timeout_ms,
        analysis_temperature=settings.llm_temperature_analysis,
        generation_temperature=settings.llm_temperature_generation,
    )
