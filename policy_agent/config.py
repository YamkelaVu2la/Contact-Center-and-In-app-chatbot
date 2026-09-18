"""Application configuration."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    """Runtime settings for the local policy assistant."""

    root_dir: Path
    chat_model: str = "qwen2.5:latest"
    embed_model: str = "nomic-embed-text:latest"
    min_relevance_score: float = 0.30
    chunk_size: int = 500
    chunk_overlap: int = 100

    @property
    def knowledge_dir(self) -> Path:
        return self.root_dir / "knowledge"

    @property
    def chroma_dir(self) -> str:
        return str(self.root_dir / "chroma_db")

    @classmethod
    def from_project_root(cls, root_dir: Path | None = None) -> "Settings":
        return cls(root_dir or Path(__file__).resolve().parent.parent)