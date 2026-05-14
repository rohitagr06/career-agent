from rag.chunker import chunk_text


def test_chunk_generation():
    text = """
    Experience

    Worked on scalable backend systems using Python, FastAPI, AWS,
    PostgreSQL, and Docker. Designed REST APIs and microservices for
    analytics workloads. Implemented CI/CD pipelines and automated testing
    strategies for production deployments.

    Skills

    Python, FastAPI, Docker, PostgreSQL, AWS, Kubernetes
    """

    chunks = chunk_text(text)

    assert len(chunks) > 0


def test_chunk_structure():
    text = """
    Experience

    Built microservices using FastAPI, PostgreSQL, Docker,
    Kubernetes, and AWS cloud infrastructure. Developed scalable APIs
    and backend services for financial analytics systems with
    production-grade deployment pipelines and automated testing.
    """

    chunks = chunk_text(text)

    assert "text" in chunks[0]
    assert "section" in chunks[0]


def test_no_empty_chunks():
    text = "Experience Python FastAPI AWS"

    chunks = chunk_text(text)

    for chunk in chunks:
        assert chunk["text"].strip() != ""
