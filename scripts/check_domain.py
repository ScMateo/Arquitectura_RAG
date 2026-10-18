import app.domain as d
print("OK domain")
print(d.Section.ARTICULOS, d.Section.ARTICULOS.value)
print(d.QueryType.SPECIFIC)
c = d.CvLACUrl("https://x")
print("URL ok", c.value)

from app.domain.interfaces import (
    IVectorStore,
    ILLMProvider,
    IEmbeddingProvider,
    IIngestor,
    IConversationStore,
    INormalizer,
    IChunker,
    IReranker,
)
print("interfaces ok")

from app.domain.entities import Chunk, Conversation, Message, Researcher, Source
print("entities ok")

try:
    d.CvLACUrl("http://x")
except ValueError as e:
    print("validation ok:", e)
