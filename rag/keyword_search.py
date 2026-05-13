from config.logging_config import logger


class KeywordSearch:
    """
    Simple keyword-based retrieval.
    """

    @staticmethod
    def search(
        query: str,
        chunks: list[str],
        top_k: int = 3,
    ) -> list[str]:

        logger.info("Starting keyword retrieval")

        query_words = query.lower().split()

        scored_chunks = []

        for chunk in chunks:
            chunk_lower = chunk.lower()
            score = sum(1 for word in query_words if word in chunk_lower)

            scored_chunks.append((chunk, score))

        scored_chunks.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        top_chunks = [chunk for chunk, score in scored_chunks if score > 0][:top_k]

        logger.info(f"Keyword retrieval completed. Retrieved {len(top_chunks)} chunks")

        return top_chunks
