# Context Engine V2 (Embeddings + Vector DB)

from ai.context.vector_store import VectorStore
from ai.context.embedding_model import EmbeddingModel

class ContextEngineV2:
    def __init__(self):
        self.vector_store = VectorStore()
        self.embedder = EmbeddingModel()

    def index_repo(self, files: dict):
        texts = list(files.values())
        embeddings = self.embedder.encode(texts)
        self.vector_store.add(embeddings, texts)

    def get_context(self, task: str, top_k=3):
        query_embedding = self.embedder.encode(task)[0]
        results = self.vector_store.search(query_embedding, top_k)
        return "\n\n".join(results)
