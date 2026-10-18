import importlib

modules = [
    "app.domain",
    "app.core.config",
    "app.core.constants",
    "app.infrastructure.ingestion",
    "app.infrastructure.ingestion.cleaner",
    "app.infrastructure.ingestion.normalizer",
    "app.infrastructure.ingestion.chunker",
    "app.infrastructure.ingestion.ingestor",
    "app.infrastructure.ingestion.indexer",
    "app.infrastructure.embeddings",
    "app.infrastructure.vectorstore",
]

for name in modules:
    try:
        importlib.import_module(name)
        print(f"OK   {name}")
    except Exception as exc:
        print(f"FAIL {name}: {type(exc).__name__}: {exc}")
