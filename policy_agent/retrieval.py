"""Policy document retrieval tool."""

from typing import Any

from langchain_core.tools import tool

from .config import Settings


class PolicyRetriever:
    """Expose relevance-filtered policy passages to the chat agent."""

    def __init__(self, vector_store: Any, settings: Settings):
        self.vector_store = vector_store
        self.settings = settings

    def search(self, query: str) -> str:
        results_with_scores = self.vector_store.similarity_search_with_relevance_scores(query, k=3)
        results = [
            (document, score)
            for document, score in results_with_scores
            if score >= self.settings.min_relevance_score
        ]
        if not results:
            return "No relevant information found in the knowledge base."

        passages = []
        for document, _score in results:
            source = document.metadata.get("source", "unknown")
            passages.append(f"[Source: {source}]\n{document.page_content}")
        return "\n\n---\n\n".join(passages)

    def as_tool(self):
        retriever = self

        @tool
        def retrieve_context(query: str) -> str:
            """Search policy passages by meaning, intent, synonyms, and paraphrases, and keywords."""

            return retriever.search(query)

        return retrieve_context