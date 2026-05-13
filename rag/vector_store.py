from typing import List
import faiss
import numpy as np

from config.logging_config import logger


class VectorStore:
    """
    FAISS vector database for semantic retrieval.
    """

    def __init__(self):
        self.index = None
        self.chunks = []

    # =====================================
    # Build Vector Index
    # =====================================

    def build_index(
        self,
        embeddings: np.ndarray,
        chunks: List[str],
    ) -> None:
        """
        Build FAISS vector index.
        """

        logger.info("Building FAISS vector index")
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype("float32"))

        self.chunks = chunks
        logger.info(f"FAISS index built successfully with {len(chunks)} chunks")

    # =====================================
    # Semantic Search
    # =====================================

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 3,
    ) -> List[str]:
        """
        Search most relevant chunks.
        """

        logger.info("Performing semantic search")
        distances, indices = self.index.search(
            query_embedding.astype("float32"),
            top_k,
        )

        retrieved_chunks = []
        for idx in indices[0]:
            if idx < len(self.chunks):
                retrieved_chunks.append(self.chunks[idx])

        logger.info(
            f"Semantic search completed. Retrieved {len(retrieved_chunks)} chunks"
        )

        return retrieved_chunks
