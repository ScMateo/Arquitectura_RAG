import importlib

modules = [
    "app.application",
    "app.application.dto.chat",
    "app.application.services.retrieval_service",
    "app.application.services.generation_service",
    "app.application.use_cases.chat_use_case",
    "app.infrastructure.conversation",
    "app.infrastructure.conversation.in_memory_conversation_store",
]

for name in modules:
    try:
        importlib.import_module(name)
        print(f"OK   {name}")
    except Exception as exc:
        print(f"FAIL {name}: {type(exc).__name__}: {exc}")
