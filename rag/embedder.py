# rag/embedder.py
from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.config import settings


class RepositoryEmbedder:
    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

    def embed_text(self, text: str) -> list[float]:
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()

    def embed_texts(self, texts: list[str], batch_size: int = 32) -> list[list[float]]:
        if not texts:
            return []

        vectors = self.model.encode(
            texts,
            batch_size=batch_size,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        return [vector.tolist() for vector in vectors]


@lru_cache
def get_embedder() -> RepositoryEmbedder:
    return RepositoryEmbedder()
