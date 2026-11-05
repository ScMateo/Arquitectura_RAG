"""Unit tests for the evaluation helpers (rejection detection)."""

from evaluation.runner import _is_rejected


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
