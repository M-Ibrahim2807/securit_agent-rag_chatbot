from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from app.config import settings
from prompts.repo_assistant_prompt import (
    REPO_ASSISTANT_HUMAN_TEMPLATE,
    REPO_ASSISTANT_SYSTEM_PROMPT,
)
from rag.retriever import retrieve_relevant_chunks
from rag.vector_store import RetrievedChunk, count_repository_chunks


llm = ChatGroq(
    model=settings.MODEL_NAME,
    temperature=0,
    api_key=settings.GROQ_API_KEY,
)


def answer_repository_question(question: str) -> dict:
    if count_repository_chunks() == 0:
        raise ValueError("Repository is not indexed yet. Run /analyze first.")

    chunks = retrieve_relevant_chunks(question)
    if not chunks:
        return {
            "question": question,
            "answer": "The repository context does not contain enough information to answer that question.",
            "sources": [],
        }

    context = format_context(chunks)
    prompt = REPO_ASSISTANT_HUMAN_TEMPLATE.format(
        question=question,
        context=context,
    )

    response = llm.invoke(
        [
            SystemMessage(content=REPO_ASSISTANT_SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]
    )

    return {
        "question": question,
        "answer": response.content,
        "sources": unique_sources(chunks),
    }


def format_context(chunks: list[RetrievedChunk]) -> str:
    sections: list[str] = []

    for chunk in chunks:
        sections.append(
            "\n".join(
                [
                    f"File: {chunk.relative_path}",
                    f"Chunk: {chunk.chunk_number}",
                    f"Similarity: {chunk.similarity:.4f}",
                    "Content:",
                    chunk.content,
                ]
            )
        )

    return "\n\n---\n\n".join(sections)


def unique_sources(chunks: list[RetrievedChunk]) -> list[str]:
    sources: list[str] = []
    seen: set[str] = set()

    for chunk in chunks:
        if chunk.relative_path in seen:
            continue
        seen.add(chunk.relative_path)
        sources.append(chunk.relative_path)

    return sources
