from core.types import Chunk
from rag.retriever import Retriever


class MockRetriever(Retriever):
    def keyword_search(self, normalized_query, top_k=5):
        return [
            (
                {
                    "text": "AWS microservices experience",
                    "section": "experience",
                },
                1.0,
            )
        ]

    def semantic_search(self, normalized_query, top_k=5):
        return [
            (
                {
                    "text": "Cloud backend systems",
                    "section": "experience",
                },
                0.8,
            )
        ]


class MockVectorStore:
    index = None
    chunks: list[Chunk] = []


def test_hybrid_retrieval_returns_results(monkeypatch):
    retriever = MockRetriever(MockVectorStore())

    monkeypatch.setattr(
        "rag.retriever.Reranker.rerank",
        lambda query, chunks, top_k: chunks[:top_k],
    )

    results = retriever.retrieve(
        query="aws",
        final_top_k=2,
    )

    assert len(results) > 0


def test_hybrid_retrieval_combines_sources(monkeypatch):
    retriever = MockRetriever(MockVectorStore())

    monkeypatch.setattr(
        "rag.retriever.Reranker.rerank",
        lambda query, chunks, top_k: chunks[:top_k],
    )

    results = retriever.retrieve(
        query="aws",
        final_top_k=2,
    )

    texts = [chunk["text"] for chunk in results]

    assert "AWS microservices experience" in texts
    assert "Cloud backend systems" in texts


def test_short_query_guard():
    retriever = Retriever(MockVectorStore())

    result = retriever.retrieve(
        query="kafka",
        final_top_k=3,
    )

    assert isinstance(result, list)
