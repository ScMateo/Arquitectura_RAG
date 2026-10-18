import importlib

modules = [
    "app.infrastructure.llm",
    "app.infrastructure.llm.gemini_adapter",
]

for name in modules:
    try:
        importlib.import_module(name)
        print(f"OK   {name}")
    except Exception as exc:
        print(f"FAIL {name}: {type(exc).__name__}: {exc}")
