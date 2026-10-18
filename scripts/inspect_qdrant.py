"""Inspect Qdrant: count, sample payloads and a raw vector search (no LLM)."""

from qdrant_client import QdrantClient

from app.core.config import get_settings
from app.infrastructure.embeddings import HuggingFaceAdapter

s = get_settings()
client = QdrantClient(url=s.qdrant_url)

info = client.get_collection(s.qdrant_collection)
print("== coleccion ==")
print("puntos       :", info.points_count)
print("tamano vector:", info.config.params.vectors.size)

print("\n== muestra de payloads (scroll) ==")
points, _ = client.scroll(s.qdrant_collection, limit=4, with_payload=True)
for p in points:
    pl = p.payload
    print(f"- {pl['author']} | {pl['section']} | {pl['content'][:55]}")

print("\n== busqueda vectorial directa (query: 'salud publica') ==")
emb = HuggingFaceAdapter(s.embedding_model_name, s.embedding_device)
qv = emb.embed_query("salud publica")
hits = client.query_points(s.qdrant_collection, query=qv, limit=3).points
for h in hits:
    pl = h.payload
    print(f"- {h.score:.3f} | {pl['author']} | {pl['section']} | {pl['content'][:50]}")
