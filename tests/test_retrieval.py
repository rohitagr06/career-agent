from core.types import Chunk
from rag.retriever import Retriever


class MockIndex:
    def search(self, embedding, top_k):
        return (
            [[1.2, 1.4]],
            [[0, 1]],
        )


class MockVectorStore:
    def __init__(self):
        self.index = MockIndex()

        self.chunks: list[Chunk] = [
            {
                "text": "Worked on AWS microservices and backend APIs.",
                "section": "experience",
            },
            {
                "text": "Built Kubernetes deployment pipelines.",
                "section": "experience",
            },
        ]


def test_deduplicate_chunks():
    chunks: list[Chunk] = [
        {
            "text": "python aws",
            "section": "skills",
        },
        {
            "text": "python aws",
            "section": "skills",
        },
        {
            "text": "fastapi docker",
            "section": "skills",
        },
    ]

    result = Retriever.deduplicate_chunks(chunks)

    assert len(result) == 2


def test_semantic_search_returns_results():
    retriever = Retriever(MockVectorStore())

    results = retriever.semantic_search(
        normalized_query="aws cloud",
        top_k=2,
    )

    assert len(results) > 0


def test_semantic_search_score_range():
    retriever = Retriever(MockVectorStore())

    results = retriever.semantic_search(
        normalized_query="aws",
        top_k=2,
    )

    for _, score in results:
        assert 0 <= score <= 1


def test_semantic_search_chunk_structure():
    retriever = Retriever(MockVectorStore())

    results = retriever.semantic_search(
        normalized_query="aws",
        top_k=2,
    )

    chunk, score = results[0]

    assert "text" in chunk
    assert "section" in chunk
    assert isinstance(score, float)


def test_similarity_score_formula():
    distance = 1.5

    similarity = 1 / (1 + distance)

    assert round(similarity, 4) == 0.4
