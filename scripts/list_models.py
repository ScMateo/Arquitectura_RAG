from google import genai

from app.core.config import get_settings

s = get_settings()
client = genai.Client(api_key=s.google_api_key.get_secret_value())

print("== modelos disponibles (flash/pro) ==")
for m in client.models.list():
    name = m.name or ""
    if "flash" in name or "pro" in name:
        print(name)
