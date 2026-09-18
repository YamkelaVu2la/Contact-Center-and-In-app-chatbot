"""Document loading, chunking, embedding, and vector-store persistence."""

from importlib import import_module

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .config import Settings


class KnowledgeBase:
    """Build the Chroma vector store from the local policy documents."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def build(self):
        try:
            chroma = import_module("langchain_chroma").Chroma
            ollama_embeddings = import_module("langchain_ollama").OllamaEmbeddings
        except (ImportError, AttributeError) as exc:
            raise RuntimeError(
                "langchain-chroma and langchain-ollama are required; install project dependencies first."
            ) from exc

        documents = [
            Document(page_content=path.read_text(encoding="utf-8"), metadata={"source": path.name})
            for path in self.settings.knowledge_dir.glob("*.txt")
        ]
        if not documents:
            raise ValueError(f"No .txt files found in {self.settings.knowledge_dir}")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
            length_function=len,
        )
        chunks = splitter.split_documents(documents)
        embeddings = ollama_embeddings(model=self.settings.embed_model)
        vector_store = chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=self.settings.chroma_dir,
            collection_name="knowledge_base",
        )
        print(f"Indexed {len(chunks)} chunks from {len(documents)} documents")
        return vector_store