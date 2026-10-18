"""End-to-end chat smoke test (retrieval + Gemini + conversation memory)."""

import sys

from app.api.dependencies import get_chat_use_case
from app.application.dto.chat import ChatRequest


def show(tag: str, resp) -> None:
    print(f"[{tag}] RESPONSE:\n{resp.answer.strip()}\n")
    print(f"[{tag}] SOURCES: {len(resp.sources)}")
    seen: set[tuple[str, str]] = set()
    for s in resp.sources:
        key = (s.author, s.section)
        if key in seen:
            continue
        seen.add(key)
        print(f"    - {s.author} | {s.section} | {s.url}")
    print("=" * 70)


def main() -> int:
    uc = get_chat_use_case()
    cases = [
        ("general", "¿Quién ha investigado sobre salud pública?", None),
        ("especifica", "¿Cuál es la formación académica de Carlos Andres Perez?", None),
        ("memoria-1", "¿Qué proyectos tiene Maria Camila Rodriguez?", "s1"),
        ("memoria-2", "¿Y esa persona en qué institución trabaja?", "s1"),
    ]
    for tag, question, session_id in cases:
        print(f">>> {tag}: {question}")
        try:
            resp = uc.execute(ChatRequest(message=question, session_id=session_id))
            show(tag, resp)
        except Exception as exc:  # noqa: BLE001
            print(f"[{tag}] ERROR: {type(exc).__name__}: {exc}")
            print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
