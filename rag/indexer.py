from pathlib import Path

from rag.chunker import chunk_repository
from rag.embedder import get_embedder
from rag.vector_store import clear_repository_chunks, insert_chunks


def index_repository(repository_path: Path) -> int:
    clear_repository_chunks()

    chunks = chunk_repository(repository_path)
    if not chunks:
        return 0

    embedder = get_embedder()
    embeddings = embedder.embed_texts([chunk.content for chunk in chunks])

    insert_chunks(chunks=chunks, embeddings=embeddings)
    return len(chunks)
