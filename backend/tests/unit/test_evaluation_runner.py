"""Unit tests for the evaluation helpers (rejection and summary)."""

from evaluation.runner import CaseResult, _format_judge_context, _is_rejected, _summarize
from tests.helpers import make_chunk


def _result(**overrides: object) -> CaseResult:
    base: dict[str, object] = {
        "id": "X",
        "kind": "general",
        "query": "q",
        "n_relevant": 1,
        "n_retrieved": 1,
        "precision_5": 1.0,
        "precision_10": 1.0,
        "recall_5": 1.0,
        "recall_10": 1.0,
        "mrr_10": 1.0,
        "ndcg_10": 1.0,
        "author_recall_10": 1.0,
        "author_coverage": 1.0,
        "rejected": 0,
        "judged": 1,
        "urls_valid": 1,
        "ttft_ms": 0.0,
        "gen_ms": 0.0,
        "retrieval_ms": 0.0,
        "faithfulness": 0.0,
        "answer_relevancy": 0.0,
        "answer_correctness": 0.0,
        "answer": "",
        "sources": "",
        "error": "",
    }
    base.update(overrides)
    return CaseResult(**base)  # type: ignore[arg-type]


def test_detects_explicit_insufficient_answer() -> None:
    assert _is_rejected("No hay información suficiente en las hojas de vida.") == 1


def test_detects_paraphrased_rejection() -> None:
    answer = (
        "La información disponible en el contexto no menciona a ningún "
        "investigador que trabaje en astrofísica. Por lo tanto, no es posible "
        "identificar a investigadores en esa área."
    )
    assert _is_rejected(answer) == 1


def test_detects_rejection_without_data_phrase() -> None:
    answer = "La información proporcionada no contiene datos sobre investigadores en astrofísica."
    assert _is_rejected(answer) == 1


def test_does_not_flag_a_normal_answer() -> None:
    answer = "María Camila Rodríguez Gómez tiene un doctorado en Inteligencia Artificial."
    assert _is_rejected(answer) == 0


def test_summary_includes_zero_scores_from_judge() -> None:
    results = [
        _result(id="A", faithfulness=0.0, answer_relevancy=1.0, answer_correctness=0.0),
        _result(id="B", faithfulness=1.0, answer_relevancy=1.0, answer_correctness=1.0),
    ]

    summary = _summarize(results, ("general",), judge_enabled=True)

    assert summary["faithfulness"] == 0.5
    assert summary["answer_correctness"] == 0.5


def test_summary_excludes_unjudged_cases() -> None:
    results = [
        _result(id="A", judged=0, faithfulness=0.0),
        _result(id="B", judged=1, faithfulness=1.0),
    ]

    summary = _summarize(results, ("general",), judge_enabled=True)

    assert summary["faithfulness"] == 1.0


def test_summary_is_zero_when_judge_is_disabled() -> None:
    summary = _summarize([_result(judged=0)], ("general",), judge_enabled=False)

    assert summary["faithfulness"] == 0.0


def test_judge_context_includes_author_and_section() -> None:
    context = _format_judge_context([make_chunk(content="contenido", author="Ana Torres")])

    assert "Ana Torres" in context
    assert "articulos" in context
    assert "contenido" in context

