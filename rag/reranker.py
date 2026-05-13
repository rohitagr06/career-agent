from sentence_transformers import util

from config.logging_config import logger
from rag.embeddings import embedding_model


class Reranker:
    """
    Reranks retrieved chunks based on semantic similarity.
    """

    @staticmethod
    def rerank(
        query: str,
        chunks: list[str],
        top_k: int = 3,
    ) -> list[str]:

        logger.info("Starting reranking process")

        if not chunks:
            return []

        query_embedding = embedding_model.encode(
            query,
            convert_to_tensor=True,
        )

        chunk_embeddings = embedding_model.encode(
            chunks,
            convert_to_tensor=True,
        )

        similarity_scores = util.cos_sim(
            query_embedding,
            chunk_embeddings,
        )[0]

        scored_chunks = list(zip(chunks, similarity_scores))

        scored_chunks.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        reranked_chunks = [chunk for chunk, score in scored_chunks[:top_k]]

        logger.info(f"Reranking completed. Final chunks: {len(reranked_chunks)}")

        return reranked_chunks
