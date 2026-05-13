from config.logging_config import logger

from rag.embeddings import (
    generate_query_embedding,
)


class Retriever:
    """
    Semantic retriever using FAISS.
    """

    def __init__(self, vector_store):

        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[str]:
        """
        Retrieve most relevant chunks.
        """

        logger.info("Starting semantic retrieval")

        query_embedding = generate_query_embedding(query)

        logger.info("Performing semantic search")

        distances, indices = self.vector_store.index.search(
            query_embedding,
            top_k,
        )

        retrieved_chunks = []

        for index in indices[0]:
            if index == -1:
                continue

            retrieved_chunks.append(self.vector_store.chunks[index])

        logger.info(
            f"Semantic search completed. Retrieved {len(retrieved_chunks)} chunks"
        )

        return retrieved_chunks
