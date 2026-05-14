from __future__ import annotations

import re

TECH_ALIASES = {
    "k8s": "kubernetes container orchestration",
    "kubernetes": "kubernetes k8s container orchestration",
    "genai": "generative ai llm ai",
    "llm": "large language model ai",
    "ai": "artificial intelligence machine learning",
    "ml": "machine learning ai",
    "aws": "amazon web services cloud",
    "gcp": "google cloud platform",
    "api": "rest api graphql api",
    "apis": "rest apis graphql apis",
    "db": "database postgres sql",
    "ui": "user interface frontend",
    "kafka": "kafka distributed event streaming messaging",
    "fastapi": "fastapi python backend rest api microservices",
    "rag": "retrieval augmented generation vector search embeddings llm",
    "faiss": "faiss vector database semantic search embeddings",
    "vector": "vector database embeddings semantic retrieval",
    "deployment": "deployment cloud docker kubernetes infrastructure",
    "cloud": "cloud aws infrastructure deployment kubernetes",
    "docker": "docker containers kubernetes deployment",
    "embeddings": "vector embeddings semantic search retrieval",
    "microservices": "microservices distributed systems backend architecture",
    "testing": "testing unit tests integration tests pact tests",
    "architecture": "software architecture backend system design",
    "backend": "backend engineering distributed systems microservices",
    # multi-word aliases
    "cloud deployment": "aws kubernetes docker cloud infrastructure deployment",
    "machine learning": "machine learning ai ml",
    "rest api": "rest api graphql api backend service",
    "post graduation": "post graduate diploma data science masters education",
    "data science": "analytics machine learning predictive analytics",
    "predictive analytics": "machine learning analytics",
    "diploma": "pgdds post graduate diploma",
    "pgdds": "post graduate diploma data science",
}


def normalize_query(query: str) -> str:
    """
    Normalize recruiter queries for better retrieval quality.
    """

    query = query.lower().strip()

    query = re.sub(r"[^\w\s]", " ", query)
    query = re.sub(r"\s+", " ", query).strip()

    # =====================================
    # Multi-word replacements FIRST
    # =====================================

    normalized_query = query

    # longest phrases first
    sorted_aliases = sorted(
        TECH_ALIASES.items(),
        key=lambda x: len(x[0]),
        reverse=True,
    )

    for alias, expansion in sorted_aliases:
        pattern = rf"\b{re.escape(alias)}\b"

        normalized_query = re.sub(
            pattern,
            expansion,
            normalized_query,
        )

    normalized_query = re.sub(
        r"\s+",
        " ",
        normalized_query,
    ).strip()

    return normalized_query
