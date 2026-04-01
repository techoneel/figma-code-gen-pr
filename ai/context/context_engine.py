# Context Engine (RAG for Repo Awareness)

from typing import List

class ContextEngine:
    def __init__(self):
        # Placeholder for vector DB / embeddings
        self.index = {}

    def index_repo(self, files: dict):
        """Index repository files (simple in-memory for now)"""
        for path, content in files.items():
            self.index[path] = content

    def search(self, query: str, top_k: int = 3) -> List[str]:
        """Naive search (replace with embeddings later)"""
        results = []
        for path, content in self.index.items():
            if query.lower() in content.lower():
                results.append((path, content))

        return [r[1] for r in results[:top_k]]

    def get_context(self, task: str) -> str:
        """Fetch relevant context for a task"""
        snippets = self.search(task)
        return "\n\n".join(snippets)
