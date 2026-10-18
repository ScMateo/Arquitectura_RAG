"""LLM-as-judge for generation metrics (PLAN_VALIDACION.md §6.2 and §7.2).

Implements RAGAS-inspired metrics (faithfulness, answer relevancy and answer
correctness) with the project's own LLM provider. RAGAS is not added as a
dependency so the harness stays reproducible inside the project stack; the
judge is used as a complement and must be validated against human annotation.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from app.domain.interfaces.llm_provider import ILLMProvider

_PROMPT = """Eres un evaluador experto de sistemas de recuperación aumentada por generación (RAG).
Evalúa la RESPUESTA usando únicamente el CONTEXTO recuperado y la RESPUESTA DE REFERENCIA.

Devuelve EXCLUSIVAMENTE un objeto JSON con tres claves numéricas entre 0 y 1:
- "faithfulness": proporción de afirmaciones de la respuesta sustentadas por el contexto.
- "answer_relevancy": qué tan pertinente es la respuesta respecto a la pregunta.
- "answer_correctness": qué tan correcta es la respuesta frente a la referencia.

PREGUNTA:
{question}

CONTEXTO RECUPERADO:
{context}

RESPUESTA DE REFERENCIA:
{reference}

RESPUESTA A EVALUAR:
{answer}

JSON:"""


@dataclass(frozen=True)
class JudgeScores:
    """Puntajes del juez para una respuesta."""

    faithfulness: float
    answer_relevancy: float
    answer_correctness: float


def _clamp(value: object) -> float:
    try:
        number = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(1.0, number))


class Judge:
    """Evalúa respuestas con el proveedor de lenguaje del proyecto."""

    def __init__(self, llm_provider: ILLMProvider, context_char_limit: int = 6000) -> None:
        self._llm_provider = llm_provider
        self._context_char_limit = context_char_limit

    def evaluate(
        self,
        question: str,
        answer: str,
        context: str,
        reference: str,
    ) -> JudgeScores | None:
        """Devuelve los puntajes del juez, o None si no puede evaluar."""
        prompt = _PROMPT.format(
            question=question,
            context=context[: self._context_char_limit],
            reference=reference,
            answer=answer,
        )
        try:
            raw = self._llm_provider.generate(prompt)
        except Exception:  # noqa: BLE001 - the judge is best-effort, never fatal
            return None

        payload = self._parse(raw)
        if payload is None:
            return None
        return JudgeScores(
            faithfulness=_clamp(payload.get("faithfulness")),
            answer_relevancy=_clamp(payload.get("answer_relevancy")),
            answer_correctness=_clamp(payload.get("answer_correctness")),
        )

    @staticmethod
    def _parse(text: str) -> dict | None:
        match = re.search(r"\{.*\}", text or "", re.DOTALL)
        if not match:
            return None
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None
