from rag.retriever import Retriever


def test_deduplicate_chunks():
    chunks = [
        {
            "text": "python aws",
            "section": "experience",
        },
        {
            "text": "python aws",
            "section": "experience",
        },
        {
            "text": "fastapi docker",
            "section": "skills",
        },
    ]

    result = Retriever.deduplicate_chunks(chunks)

    assert len(result) == 2

    assert result[0]["text"] == "python aws"
    assert result[1]["text"] == "fastapi docker"

    assert result[0]["section"] == "experience"
    assert result[1]["section"] == "skills"
