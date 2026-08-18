from app.config import settings
from rag.embedder import get_embedder
from rag.vector_store import RetrievedChunk, similarity_search


def retrieve_relevant_chunks(question: str, top_k: int | None = None) -> list[RetrievedChunk]:
    limit = top_k or settings.RAG_TOP_K
    query_embedding = get_embedder().embed_text(question)

    return similarity_search(
        query_embedding=query_embedding,
        top_k=limit,
    )
