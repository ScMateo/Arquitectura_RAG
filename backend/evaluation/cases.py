"""Evaluation cases with ground truth (PLAN_VALIDACION.md §5).

Derives 40 cases (8 per type) from the synthetic corpus by construction.
"""

from __future__ import annotations

from dataclasses import dataclass

from .corpus import Researcher

INSUFFICIENT = "No hay información suficiente en las hojas de vida para responder."

_PUNTUAL_SPECS: list[tuple[int, str, str, str]] = [
    (0, "formacion_academica", "¿Cuál es la formación académica de {name}?", "list"),
    (11, "proyectos", "¿Qué proyectos de investigación ha realizado {name}?", "list"),
    (19, "articulos", "¿Cuántos artículos científicos tiene registrados {name}?", "count"),
    (28, "experiencia_profesional", "¿Cuál es la experiencia profesional de {name}?", "list"),
    (37, "formacion_complementaria", "¿Qué formación complementaria tiene {name}?", "list"),
    (5, "articulos", "¿Qué artículos ha publicado {name}?", "list"),
    (24, "proyectos", "¿En qué proyectos ha participado {name}?", "list"),
    (45, "experiencia_profesional", "¿Dónde ha trabajado {name}?", "list"),
]

_RELATIONAL_PAIRS: list[tuple[str, str]] = [
    ("inteligencia artificial", "procesamiento de lenguaje natural"),
    ("inteligencia artificial", "visión por computador"),
    ("aprendizaje automático", "salud pública"),
    ("ciencia de datos", "salud pública"),
    ("desarrollo de software", "inteligencia artificial"),
    ("aprendizaje automático", "ciencia de datos"),
    ("procesamiento de lenguaje natural", "desarrollo de software"),
    ("inteligencia artificial", "ciencia de datos"),
]

_NEGATIVE_TOPICS = [
    "astrofísica",
    "derecho penal",
    "gastronomía molecular",
    "arqueología",
    "medicina veterinaria",
    "ingeniería de minas",
    "teología",
    "danza contemporánea",
]


@dataclass(frozen=True)
class EvalCase:
    """Caso de evaluación con su verdad de referencia."""

    id: str
    query: str
    kind: str
    relevant_authors: tuple[str, ...]
    expected_sections: tuple[str, ...]
    reference: str


def _puntual_cases(researchers: list[Researcher]) -> list[EvalCase]:
    cases: list[EvalCase] = []
    for number, (index, aspect, template, mode) in enumerate(_PUNTUAL_SPECS, start=1):
        researcher = researchers[index]
        content = researcher.sections[aspect]
        reference = content if mode == "list" else str(len(researcher.articles))
        cases.append(
            EvalCase(
                id=f"P{number}",
                query=template.format(name=researcher.name),
                kind="puntual",
                relevant_authors=(researcher.name,),
                expected_sections=(aspect,),
                reference=reference,
            )
        )
    return cases


def _general_cases(researchers: list[Researcher], themes: list[str]) -> list[EvalCase]:
    cases: list[EvalCase] = []
    for number, theme in enumerate(themes, start=1):
        authors = tuple(r.name for r in researchers if theme in r.themes)
        cases.append(
            EvalCase(
                id=f"G{number}",
                query=f"¿Qué investigadores trabajan en {theme}?",
                kind="general",
                relevant_authors=authors,
                expected_sections=(),
                reference=", ".join(authors),
            )
        )
    return cases


def _relational_cases(researchers: list[Researcher]) -> list[EvalCase]:
    cases: list[EvalCase] = []
    for number, (first, second) in enumerate(_RELATIONAL_PAIRS, start=1):
        authors = tuple(
            r.name for r in researchers if first in r.themes and second in r.themes
        )
        cases.append(
            EvalCase(
                id=f"R{number}",
                query=(
                    f"¿Qué investigadores trabajan en {first} y además tienen "
                    f"experiencia en {second}?"
                ),
                kind="relacional",
                relevant_authors=authors,
                expected_sections=(),
                reference=", ".join(authors),
            )
        )
    return cases


def _pick_triple(
    candidates: list[tuple[Researcher, int]],
) -> list[tuple[Researcher, int]] | None:
    """Elige tres investigadores con un máximo de artículos único y estricto."""
    if len(candidates) < 3 or candidates[0][1] <= 0:
        return None
    top = candidates[0][1]
    others = [item for item in candidates[1:] if item[1] < top]
    if len(others) < 2:
        return None
    return [candidates[0], others[0], others[1]]


def _comparative_cases(researchers: list[Researcher], themes: list[str]) -> list[EvalCase]:
    pools = {
        theme: sorted(
            ((r, r.article_count(theme)) for r in researchers if theme in r.themes),
            key=lambda item: (-item[1], item[0].name),
        )
        for theme in themes
    }
    cases: list[EvalCase] = []

    def build(theme: str) -> bool:
        selected = _pick_triple(pools[theme])
        if selected is None:
            return False
        selected_set = {id(item[0]) for item in selected}
        pools[theme] = [item for item in pools[theme] if id(item[0]) not in selected_set]
        winner, count = selected[0]
        names = ", ".join(researcher.name for researcher, _ in selected)
        cases.append(
            EvalCase(
                id=f"C{len(cases) + 1}",
                query=(
                    "¿Cuál de estos investigadores tiene mayor cantidad de artículos "
                    f"relacionados con {theme}: {names}?"
                ),
                kind="comparativa",
                relevant_authors=(winner.name,),
                expected_sections=("articulos",),
                reference=f"{winner.name}, con {count} artículos sobre {theme}.",
            )
        )
        return True

    for theme in themes:
        build(theme)
    while len(cases) < len(themes):
        if not any(build(theme) for theme in themes):
            break
    return cases


def _negative_cases() -> list[EvalCase]:
    return [
        EvalCase(
            id=f"N{number}",
            query=f"¿Qué investigadores trabajan en {topic}?",
            kind="negativa",
            relevant_authors=(),
            expected_sections=(),
            reference=INSUFFICIENT,
        )
        for number, topic in enumerate(_NEGATIVE_TOPICS, start=1)
    ]


def build_cases(researchers: list[Researcher], themes: list[str]) -> list[EvalCase]:
    """Construye los 40 casos de evaluación (8 por tipo)."""
    return [
        *_puntual_cases(researchers),
        *_general_cases(researchers, themes),
        *_relational_cases(researchers),
        *_comparative_cases(researchers, themes),
        *_negative_cases(),
    ]
