"""Synthetic evaluation corpus (PLAN_VALIDACION.md §4).

Builds a deterministic corpus of 50 researchers conforming to the CvLAC CSV
contract (REGLAS_DATOS_CSV.md). Content is varied in richness and length to
resemble real CvLAC profiles, and the corpus is designed so that ground truth
for the 40 evaluation cases can be derived by construction.
"""

from __future__ import annotations

import csv
import random
from dataclasses import dataclass, field
from pathlib import Path

CSV_HEADER = [
    "identificacion",
    "url_cvlac",
    "formacion_academica",
    "experiencia_profesional",
    "articulos",
    "proyectos",
    "identificadores_autor",
    "software",
    "productos_tecnologicos",
    "formacion_complementaria",
    "trabajos_dirigidos",
    "evento_cientifico",
    "libros",
    "capitulos_libro",
    "procesos_tecnicas",
    "asesorias",
    "redes_conocimiento",
    "patentes",
    "insumos_politica",
    "desarrollos_web",
    "manuales_guias",
    "redes_sociales",
    "par_evaluador",
]

THEMES = [
    "inteligencia artificial",
    "aprendizaje automático",
    "procesamiento de lenguaje natural",
    "visión por computador",
    "ciencia de datos",
    "desarrollo de software",
    "salud pública",
    "energías renovables",
]

_THEME_SKILLS = {
    "inteligencia artificial": [
        "aprendizaje profundo",
        "agentes inteligentes",
        "razonamiento automático",
        "sistemas expertos",
    ],
    "aprendizaje automático": [
        "clasificación supervisada",
        "aprendizaje por refuerzo",
        "modelos de ensamble",
        "optimización de hiperparámetros",
    ],
    "procesamiento de lenguaje natural": [
        "modelos de lenguaje",
        "análisis de sentimiento",
        "traducción automática",
        "extracción de información",
    ],
    "visión por computador": [
        "segmentación de imágenes",
        "detección de objetos",
        "reconocimiento de patrones",
        "procesamiento de video",
    ],
    "ciencia de datos": [
        "analítica predictiva",
        "minería de datos",
        "visualización de datos",
        "series de tiempo",
    ],
    "desarrollo de software": [
        "arquitecturas de microservicios",
        "integración continua",
        "aplicaciones web",
        "calidad de software",
    ],
    "salud pública": [
        "vigilancia epidemiológica",
        "promoción de la salud",
        "políticas de salud",
        "salud comunitaria",
    ],
    "energías renovables": [
        "energía solar fotovoltaica",
        "bioenergía",
        "eficiencia energética",
        "redes inteligentes",
    ],
}

_ARTICLE_TEMPLATES = [
    "Avances en {theme} mediante {skill}",
    "Aplicación de {skill} en {domain}",
    "Estudio comparativo de técnicas de {theme}",
    "Metodologías de {theme} para {domain}",
    "Modelo basado en {skill} orientado a {domain}",
    "Revisión sistemática de {theme} y {skill}",
]

_PROJECT_TEMPLATES = [
    "Fortalecimiento de capacidades en {theme}",
    "Desarrollo de una plataforma de {theme} para {domain}",
    "Investigación aplicada en {theme}",
    "Análisis de {theme} orientado a {domain}",
    "Sistema de apoyo a decisiones en {theme}",
]

_DOMAINS = [
    "la salud",
    "la educación",
    "la agricultura",
    "el sector financiero",
    "la industria manufacturera",
    "el medio ambiente",
    "la movilidad urbana",
    "la seguridad alimentaria",
]

_INSTITUTIONS = [
    ("Universidad Nacional de Colombia", "UNAL"),
    ("Universidad de Antioquia", "UdeA"),
    ("Universidad del Valle", None),
    ("Universidad de los Andes", None),
    ("Pontificia Universidad Javeriana", None),
    ("Universidad Industrial de Santander", "UIS"),
    ("Universidad del Cauca", "Unicauca"),
    ("Instituto Nacional de Salud", "INS"),
    ("Universidad de Nariño", None),
    ("Universidad Pedagógica y Tecnológica de Colombia", "UPTC"),
]

_POSITIONS = [
    "Profesor titular",
    "Profesor asociado",
    "Profesor asistente",
    "Investigador principal",
    "Investigador asociado",
    "Coordinador de grupo de investigación",
]

_JOURNALS = [
    "Revista Colombiana de Ingeniería",
    "Revista de la Academia Colombiana de Ciencias",
    "Revista Facultad de Ingeniería",
    "Journal of Applied Research",
    "Revista de Salud Pública",
]

_FEMALE_NAMES = [
    "María Camila", "Laura", "Ana María", "Diana", "Sara", "Valentina",
    "Carolina", "Juliana", "Paula", "Daniela", "Natalia", "Sofía",
    "Marta", "Andrea", "Isabella",
]

_MALE_NAMES = [
    "Juan Diego", "Carlos Andrés", "Andrés", "José", "Sebastián", "Felipe",
    "Alejandro", "Diego", "Luis", "Miguel", "Santiago", "Óscar",
    "Camilo", "Julián", "Fernando",
]

_LAST_NAMES = [
    "Rodríguez", "Gómez", "Pérez", "Martínez", "López", "García",
    "Hernández", "Ramírez", "Moreno", "Castillo", "Vargas", "Rojas",
    "Navarro", "Cárdenas", "Peña", "Suárez", "Ospina", "Quintero",
    "Betancourt", "Villalba",
]

# 50 theme assignments: overlaps are intentional to enable relational and
# comparative queries (PLAN_VALIDACION.md §4.2).
_THEME_ASSIGNMENTS: list[tuple[str, ...]] = [
    ("inteligencia artificial", "aprendizaje automático"),
    ("inteligencia artificial", "procesamiento de lenguaje natural"),
    ("inteligencia artificial", "visión por computador"),
    ("inteligencia artificial", "aprendizaje automático", "procesamiento de lenguaje natural"),
    ("inteligencia artificial",),
    ("inteligencia artificial", "ciencia de datos"),
    ("inteligencia artificial", "desarrollo de software"),
    ("inteligencia artificial", "visión por computador", "aprendizaje automático"),
    ("inteligencia artificial", "procesamiento de lenguaje natural"),
    ("inteligencia artificial",),
    ("aprendizaje automático",),
    ("aprendizaje automático", "ciencia de datos"),
    ("aprendizaje automático", "salud pública"),
    ("aprendizaje automático", "ciencia de datos"),
    ("aprendizaje automático", "desarrollo de software"),
    ("aprendizaje automático",),
    ("aprendizaje automático", "energías renovables"),
    ("aprendizaje automático", "ciencia de datos"),
    ("procesamiento de lenguaje natural",),
    ("procesamiento de lenguaje natural", "inteligencia artificial"),
    ("procesamiento de lenguaje natural", "desarrollo de software"),
    ("procesamiento de lenguaje natural",),
    ("procesamiento de lenguaje natural", "aprendizaje automático"),
    ("visión por computador",),
    ("visión por computador", "inteligencia artificial"),
    ("visión por computador",),
    ("visión por computador", "aprendizaje automático"),
    ("visión por computador", "salud pública"),
    ("ciencia de datos",),
    ("ciencia de datos", "salud pública"),
    ("ciencia de datos", "desarrollo de software"),
    ("ciencia de datos",),
    ("ciencia de datos", "energías renovables"),
    ("ciencia de datos", "aprendizaje automático"),
    ("ciencia de datos",),
    ("ciencia de datos", "inteligencia artificial"),
    ("desarrollo de software",),
    ("desarrollo de software", "inteligencia artificial"),
    ("desarrollo de software",),
    ("desarrollo de software", "ciencia de datos"),
    ("desarrollo de software", "aprendizaje automático"),
    ("desarrollo de software",),
    ("desarrollo de software", "energías renovables"),
    ("desarrollo de software",),
    ("salud pública",),
    ("salud pública", "ciencia de datos"),
    ("salud pública", "aprendizaje automático"),
    ("energías renovables",),
    ("energías renovables", "inteligencia artificial"),
    ("energías renovables", "aprendizaje automático"),
]


@dataclass
class Researcher:
    """Perfil sintético con los metadatos necesarios para derivar el ground truth."""

    name: str
    nationality: str
    sex: str
    cod_rh: str
    themes: tuple[str, ...]
    sections: dict[str, str] = field(default_factory=dict)
    articles: list[tuple[str, str]] = field(default_factory=list)
    projects: list[tuple[str, str]] = field(default_factory=list)

    def article_count(self, theme: str | None = None) -> int:
        if theme is None:
            return len(self.articles)
        return sum(1 for tagged, _ in self.articles if tagged == theme)

    def project_count(self, theme: str | None = None) -> int:
        if theme is None:
            return len(self.projects)
        return sum(1 for tagged, _ in self.projects if tagged == theme)


def _build_name(index: int, rng: random.Random) -> tuple[str, str]:
    first_names = [(name, "Femenino") for name in _FEMALE_NAMES]
    first_names += [(name, "Masculino") for name in _MALE_NAMES]
    first, sex = first_names[index % len(first_names)]
    # The mixed-radix combination of first, first surname and second surname is
    # unique for the 50 indices, so every researcher gets a distinct full name.
    first_surname = _LAST_NAMES[index % len(_LAST_NAMES)]
    second_surname = _LAST_NAMES[(index // len(_LAST_NAMES) + 1) % len(_LAST_NAMES)]
    return f"{first} {first_surname} {second_surname}", sex


def _institution(index: int, rng: random.Random) -> str:
    full, acronym = _INSTITUTIONS[index % len(_INSTITUTIONS)]
    if acronym and index % 3 == 0:
        return f"{full} ({acronym})"
    if acronym and index % 3 == 1:
        return acronym
    return full


def _sentence(theme: str, index: int, rng: random.Random) -> tuple[str, str]:
    skill = _THEME_SKILLS[theme][(index + rng.randrange(3)) % len(_THEME_SKILLS[theme])]
    domain = _DOMAINS[(index * 3 + rng.randrange(3)) % len(_DOMAINS)]
    return skill, domain


def build_researchers(seed: int = 20261018) -> list[Researcher]:
    """Construye los 50 investigadores del corpus de evaluación."""
    rng = random.Random(seed)
    researchers: list[Researcher] = []

    for index in range(50):
        name, sex = _build_name(index, rng)
        themes = _THEME_ASSIGNMENTS[index]
        nationality = "Colombiana"
        cod_rh = f"{100000000 + index * 137:010d}"

        formation_items: list[str] = []
        for degree_index, degree in enumerate(["Pregrado", "Maestría", "Doctorado"]):
            if degree_index > len(themes):
                break
            theme = themes[degree_index % len(themes)]
            institution = _institution(index + degree_index, rng)
            year = 2000 + (index + degree_index * 4) % 22
            formation_items.append(
                f"{degree} en {theme}, {institution}, {year}. "
                f"Trabajo de grado orientado a {_DOMAINS[(index + degree_index) % len(_DOMAINS)]}."
            )

        experience_items: list[str] = []
        position = _POSITIONS[index % len(_POSITIONS)]
        experience_items.append(
            f"{position} en {_institution(index + 2, rng)} desde "
            f"{2005 + index % 15}."
        )
        if index % 2 == 0:
            experience_items.append(
                f"Miembro del grupo de investigación en {themes[0]}."
            )

        article_total = 2 + (index * 7) % 10
        articles: list[tuple[str, str]] = []
        for article_index in range(article_total):
            theme = themes[article_index % len(themes)]
            skill, domain = _sentence(theme, index + article_index, rng)
            template = _ARTICLE_TEMPLATES[(index + article_index) % len(_ARTICLE_TEMPLATES)]
            title = template.format(theme=theme, skill=skill, domain=domain)
            journal = _JOURNALS[(index + article_index) % len(_JOURNALS)]
            year = 2012 + (index + article_index) % 13
            articles.append((theme, f"{title}. {journal}, {year}."))

        project_total = 1 + (index * 5) % 6
        projects: list[tuple[str, str]] = []
        for project_index in range(project_total):
            theme = themes[project_index % len(themes)]
            skill, domain = _sentence(theme, index + project_index + 1, rng)
            template = _PROJECT_TEMPLATES[(index + project_index) % len(_PROJECT_TEMPLATES)]
            title = template.format(theme=theme, skill=skill, domain=domain)
            role = "investigador principal" if project_index % 2 == 0 else "coinvestigador"
            year = 2014 + (index + project_index) % 11
            projects.append((theme, f"{title}. Rol: {role}. {year}."))

        complementaria = (
            f"Curso de {_THEME_SKILLS[themes[0]][0]} avanzada, "
            f"{_institution(index + 4, rng)}, {2015 + index % 8}."
        )
        if index % 2 == 0:
            complementaria += (
                f" Diplomado en gestión de la investigación, "
                f"{_institution(index + 5, rng)}, {2018 + index % 6}."
            )

        sections: dict[str, str] = {
            "identificacion": (
                f"Nombre {name} Nacionalidad {nationality} Sexo {sex}"
            ),
            "formacion_academica": " ".join(formation_items),
            "experiencia_profesional": " ".join(experience_items),
            "articulos": " ".join(text for _, text in articles),
            "proyectos": " ".join(text for _, text in projects),
            "identificadores_autor": f"ORCID 0000-000{index:02d}-{index * 3:04d}-{index * 7:04d}",
            "formacion_complementaria": complementaria,
        }

        if index % 3 == 0:
            sections["software"] = (
                f"Software para {themes[0]}. Registro ante la Dirección Nacional "
                f"de Derecho de Autor, {2016 + index % 7}."
            )
        if index % 4 == 0:
            sections["libros"] = (
                f"Fundamentos de {themes[0]}. Editorial Académica, {2015 + index % 9}."
            )
        if index % 5 == 0:
            sections["evento_cientifico"] = (
                f"Ponente en el Congreso Nacional de {themes[0]}, {2017 + index % 6}."
            )
        if index % 3 == 1:
            sections["trabajos_dirigidos"] = (
                f"Dirección de trabajo de grado en {themes[0]}, {2019 + index % 6}."
            )
        if index % 6 == 0:
            sections["redes_sociales"] = "Google Scholar; ResearchGate."
        if index % 7 == 0:
            sections["par_evaluador"] = (
                f"Par evaluador de la Revista Colombiana de {themes[0]}."
            )

        researchers.append(
            Researcher(
                name=name,
                nationality=nationality,
                sex=sex,
                cod_rh=cod_rh,
                themes=themes,
                sections=sections,
                articles=articles,
                projects=projects,
            )
        )

    return researchers


def to_row(researcher: Researcher) -> dict[str, str]:
    """Convierte un investigador a una fila del contrato CSV."""
    row = {column: "" for column in CSV_HEADER}
    row["identificacion"] = researcher.sections["identificacion"]
    row["url_cvlac"] = (
        "https://scienti.minciencias.gov.co/cvlac/visualizador/"
        f"generarCurriculoCv.do?cod_rh={researcher.cod_rh}"
    )
    for section, content in researcher.sections.items():
        if section in row:
            row[section] = content
    return row


def write_csv(researchers: list[Researcher], path: str | Path) -> Path:
    """Escribe el corpus en un CSV conforme al contrato de datos."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=CSV_HEADER,
            delimiter="|",
            quoting=csv.QUOTE_ALL,
        )
        writer.writeheader()
        for researcher in researchers:
            writer.writerow(to_row(researcher))

    return destination


if __name__ == "__main__":
    corpus = build_researchers()
    target = write_csv(corpus, "data/processed/eval_corpus.csv")
    lengths = [len(r.sections.get("articulos", "")) for r in corpus]
    print(f"investigadores: {len(corpus)}")
    print(f"csv: {target}")
    print(f"longitud articulos min/media/max: {min(lengths)}/{sum(lengths)//len(lengths)}/{max(lengths)}")
