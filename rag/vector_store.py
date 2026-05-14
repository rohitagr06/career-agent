import faiss
import numpy as np

from config.logging_config import logger
from core.types import Chunk
from rag.storage import (
    index_exists,
    load_chunks,
    load_faiss_index,
    load_metadata,
)


class VectorStore:
    """
    FAISS vector database for semantic retrieval.
    """

    def __init__(self):

        self.index = None
        self.chunks: list[Chunk] = []
        self.metadata: list[dict] = []

        # =====================================
        # Load Persisted Index
        # =====================================

        if index_exists():

            logger.info("Loading persisted vector store")

            self.index = load_faiss_index()
            self.chunks = load_chunks()
            self.metadata = load_metadata()

            logger.info(f"Loaded vector store with {len(self.chunks)} chunks")

    # =====================================
    # Build Vector Index
    # =====================================

    def build_index(
        self,
        embeddings: np.ndarray,
        chunks: list[Chunk],
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
    ) -> list[Chunk]:
        """
        Search most relevant chunks.
        """

        logger.info("Performing semantic search")

        assert self.index is not None
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
