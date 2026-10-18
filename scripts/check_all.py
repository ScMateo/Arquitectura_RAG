import importlib

modules = [
    "app.domain",
    "app.core.config",
    "app.core.constants",
    "app.infrastructure.embeddings",
    "app.infrastructure.vectorstore",
    "app.infrastructure.llm",
    "app.infrastructure.ingestion",
    "app.infrastructure.conversation",
    "app.infrastructure.reranking",
    "app.application",
    "app.api.dependencies",
    "app.api.v1.endpoints.chat",
    "app.api.v1.endpoints.health",
    "app.main",
]

ok = True
for name in modules:
    try:
        importlib.import_module(name)
        print(f"OK   {name}")
    except Exception as exc:
        ok = False
        print(f"FAIL {name}: {type(exc).__name__}: {exc}")

print("ALL OK" if ok else "SOME FAILED")
