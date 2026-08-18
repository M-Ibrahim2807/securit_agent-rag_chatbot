from dataclasses import dataclass

from app.database import SessionLocal
from models.vector_model import RepositoryChunk as RepositoryChunkModel
from rag.chunker import RepositoryChunk


@dataclass(frozen=True)
class RetrievedChunk:
    file_name: str
    relative_path: str
    chunk_number: int
    content: str
    similarity: float


def clear_repository_chunks() -> None:
    db = SessionLocal()
    try:
        db.query(RepositoryChunkModel).delete()
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def insert_chunks(chunks: list[RepositoryChunk], embeddings: list[list[float]]) -> None:
    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must have the same length.")

    db = SessionLocal()
    try:
        for chunk, embedding in zip(chunks, embeddings, strict=True):
            db.add(
                RepositoryChunkModel(
                    file_name=chunk.file_path.rsplit("/", 1)[-1],
                    relative_path=chunk.file_path,
                    chunk_number=chunk.chunk_index,
                    content=chunk.content,
                    embedding=embedding,
                )
            )

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def similarity_search(query_embedding: list[float], top_k: int) -> list[RetrievedChunk]:
    db = SessionLocal()
    try:
        distance = RepositoryChunkModel.embedding.cosine_distance(query_embedding)
        rows = (
            db.query(RepositoryChunkModel, distance.label("distance"))
            .order_by(distance)
            .limit(top_k)
            .all()
        )

        retrieved_chunks: list[RetrievedChunk] = []
        for chunk_model, distance_value in rows:
            retrieved_chunks.append(
                RetrievedChunk(
                    file_name=chunk_model.file_name,
                    relative_path=chunk_model.relative_path,
                    chunk_number=chunk_model.chunk_number,
                    content=chunk_model.content,
                    similarity=1 - float(distance_value),
                )
            )

        return retrieved_chunks
    finally:
        db.close()


def count_repository_chunks() -> int:
    db = SessionLocal()
    try:
        return db.query(RepositoryChunkModel).count()
    finally:
        db.close()
