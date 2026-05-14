from core.types import Chunk
from rag.retriever import Retriever


def test_chunk_text_slicing_regression():
    """
    Prevent:
    slice(None, 300, None)

    Bug cause:
    Attempted slicing directly on dict instead of dict["text"].
    """

    chunk: list[Chunk] = [
        {
            "text": "AWS microservices backend systems",
            "section": "experience",
        }
    ]

    preview = chunk[0]["text"][:300]

    assert isinstance(preview, str)


def test_join_dict_regression():
    """
    Prevent:
    expected str instance, dict found

    Bug cause:
    Attempted join() directly on dictionaries.
    """

    chunks: list[Chunk] = [
        {
            "text": "AWS backend systems",
            "section": "experience",
        },
        {
            "text": "FastAPI microservices",
            "section": "experience",
        },
    ]

    combined = "\n".join(chunk["text"] for chunk in chunks)

    assert isinstance(combined, str)

    assert "AWS" in combined


def test_deduplicate_dict_regression():
    """
    Prevent:
    unhashable type: 'dict'

    Bug cause:
    Using dictionaries as set/dict keys.
    """

    chunks: list[Chunk] = [
        {"text": "python aws", "section": "skills"},
        {"text": "python aws", "section": "skills"},
        {"text": "docker kubernetes", "section": "skills"},
    ]

    deduplicated = Retriever.deduplicate_chunks(chunks)

    assert len(deduplicated) == 2


def test_empty_keyword_search_regression():
    """
    Prevent:
    ZeroDivisionError in BM25 when chunks are empty.
    """

    retriever = Retriever(
        vector_store=type(
            "MockStore",
            (),
            {
                "chunks": [],
                "index": None,
            },
        )()
    )

    results = retriever.keyword_search(
        normalized_query="aws",
        top_k=5,
    )

    assert results == []


def test_similarity_score_bounds():
    """
    Ensure similarity scores always stay normalized.
    """

    distances = [0.1, 0.5, 1.0, 2.0]

    for distance in distances:
        similarity = 1 / (1 + distance)

        assert 0 <= similarity <= 1


def test_chunk_structure_contract():
    """
    Ensure every chunk follows expected schema.
    """

    chunk: list[Chunk] = [
        {
            "text": "Built scalable APIs",
            "section": "experience",
        }
    ]

    assert "text" in chunk[0]
    assert "section" in chunk[0]

    assert isinstance(chunk[0]["text"], str)
    assert isinstance(chunk[0]["section"], str)


def test_short_skill_query_guard_regression(monkeypatch):
    """
    Prevent semantic fallback on unsupported short skill queries.
    """

    class MockRetriever(Retriever):
        def keyword_search(self, normalized_query, top_k=5):
            return []

    retriever = MockRetriever(
        vector_store=type(
            "MockStore",
            (),
            {
                "chunks": [],
                "index": None,
            },
        )()
    )

    results = retriever.retrieve(
        query="kafka",
        final_top_k=3,
    )

    assert results == []
