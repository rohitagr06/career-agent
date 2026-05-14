import numpy as np
from sentence_transformers import SentenceTransformer

from config.logging_config import logger

# =====================================
# Embedding Model
# =====================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

embedding_model = SentenceTransformer(EMBEDDING_MODEL)


# =====================================
# Generate Query Embedding
# =====================================


def generate_query_embedding(
    query: str,
) -> np.ndarray:
    """
    Generate embedding for recruiter query.
    """

    logger.info("Generating query embedding")

    embedding = embedding_model.encode(
        query,
        normalize_embeddings=True,
    )

    logger.info("Query embedding generation completed")

    return np.array(
        [embedding],
        dtype="float32",
    )


# =====================================
# Generate Document Embeddings
# =====================================


def generate_document_embeddings(
    chunks: list[str],
) -> np.ndarray:
    """
    Generate embeddings for chunks.
    """

    logger.info(f"Generating embeddings for {len(chunks)} chunks")

    embeddings = embedding_model.encode(
        chunks,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=True,
    )

    logger.info("All embeddings generated successfully")

    return np.array(
        embeddings,
        dtype="float32",
    )
