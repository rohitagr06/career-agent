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
    "microservices": ("microservices distributed systems backend architecture"),
    "testing": ("testing unit tests integration tests pact tests"),
    "architecture": ("software architecture backend system design"),
    "backend": ("backend engineering distributed systems microservices"),
}


def normalize_query(query: str) -> str:
    """
    Normalize recruiter queries for better retrieval quality.
    """

    query = query.lower().strip()

    # Remove excessive punctuation
    query = re.sub(r"[^\w\s]", " ", query)

    # Normalize whitespace
    query = re.sub(r"\s+", " ", query).strip()

    words = query.split()

    expanded_words = []

    for word in words:
        expanded_words.append(TECH_ALIASES.get(word, word))

    normalized_query = " ".join(expanded_words)

    return normalized_query
