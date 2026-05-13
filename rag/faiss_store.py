import faiss
import numpy as np

from config.logging_config import logger
from rag.storage import (
    load_chunks,
    load_faiss_index,
    load_metadata,
    save_chunks,
    save_faiss_index,
    save_metadata,
)


class FAISSStore:
    """
    Handles FAISS vector storage operations.
    """

    def __init__(self):

        self.index = None
        self.chunks = []
        self.metadata = []

    # =====================================
    # Build Index
    # =====================================

    def build_index(
        self,
        embeddings: np.ndarray,
        chunks: list[str],
        metadata: list[dict] | None = None,
    ) -> None:

        logger.info("Building FAISS vector index")

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings.astype("float32"))

        self.chunks = chunks

        self.metadata = metadata or []

        logger.info(f"FAISS index built successfully with {len(chunks)} chunks")

    # =====================================
    # Save
    # =====================================

    def save(self) -> None:

        if self.index is None:
            raise ValueError("FAISS index is not initialized")

        logger.info("Persisting FAISS index and chunks")

        save_faiss_index(self.index)

        save_chunks(self.chunks)

        save_metadata(self.metadata)

        logger.info("FAISS persistence completed")

    # =====================================
    # Load
    # =====================================

    def load(self) -> None:

        logger.info("Loading persisted FAISS store")

        self.index = load_faiss_index()

        self.chunks = load_chunks()

        self.metadata = load_metadata()

        logger.info("Persisted FAISS store loaded successfully")

    # =====================================
    # Search
    # =====================================

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 3,
    ) -> list[str]:

        if self.index is None:
            raise ValueError("FAISS index is not loaded")

        logger.info("Performing semantic search")

        distances, indices = self.index.search(
            query_embedding.astype("float32"),
            top_k,
        )

        retrieved_chunks = []

        for index in indices[0]:
            if 0 <= index < len(self.chunks):
                retrieved_chunks.append(self.chunks[index])

        logger.info(
            f"Semantic search completed. Retrieved {len(retrieved_chunks)} chunks"
        )

        return retrieved_chunks
