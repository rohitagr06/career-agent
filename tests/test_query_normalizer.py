from rag.query_normalizer import normalize_query


def test_aws_normalization():
    result = normalize_query("aws")

    assert "amazon web services" in result.lower()


def test_gcp_normalization():
    result = normalize_query("gcp")

    assert "google cloud platform" in result.lower()


def test_query_lowercase():
    result = normalize_query("PYTHON")

    assert result == result.lower()
