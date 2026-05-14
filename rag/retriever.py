from __future__ import annotations

from config.logging_config import logger

from rag.embeddings import generate_query_embedding
from rag.keyword_search import KeywordSearch
from rag.query_normalizer import normalize_query
from rag.reranker import Reranker


class Retriever:
    """
    Hybrid retriever using:
    - semantic FAISS retrieval
    - keyword retrieval
    - reranking
    """

    def __init__(self, vector_store):

        self.vector_store = vector_store

    def semantic_search(
        self,
        normalized_query: str,
        top_k: int = 5,
    ) -> list[tuple[dict, float]]:
        """
        Perform semantic vector search with scores.
        """

        logger.info("Starting semantic retrieval")

        query_embedding = generate_query_embedding(normalized_query)

        distances, indices = self.vector_store.index.search(
            query_embedding,
            top_k,
        )

        scored_chunks = []

        MAX_DISTANCE = 2.2

        for distance, index in zip(
            distances[0],
            indices[0],
        ):
            if index == -1:
                continue

            if distance > MAX_DISTANCE:
                logger.info(f"Filtered distant chunk: {distance:.4f}")
                continue

            similarity_score = 1 / (1 + distance)

            chunk = self.vector_store.chunks[index]
            logger.info(f"distance={distance:.4f} similarity={similarity_score:.4f}")

            scored_chunks.append(
                (
                    chunk,
                    float(similarity_score),
                )
            )

        logger.info(
            f"Semantic retrieval completed. Retrieved {len(scored_chunks)} chunks"
        )

        return scored_chunks

    def keyword_search(
        self,
        normalized_query: str,
        top_k: int = 5,
    ) -> list[str]:
        """
        Perform keyword retrieval.
        """

        return KeywordSearch.search(
            query=normalized_query,
            chunks=self.vector_store.chunks,
            top_k=top_k,
        )

    @staticmethod
    def deduplicate_chunks(
        chunks: list[dict],
    ) -> list[dict]:
        """
        Remove duplicate chunks while preserving order.
        """

        seen = set()

        unique_chunks = []

        for chunk in chunks:
            chunk_text = chunk["text"]

            if chunk_text in seen:
                continue

            seen.add(chunk_text)

            unique_chunks.append(chunk)

        return unique_chunks

    def retrieve(
        self,
        query: str,
        semantic_top_k: int = 5,
        keyword_top_k: int = 5,
        final_top_k: int = 3,
        top_k: int | None = None,
    ) -> list[tuple[str, float]]:
        """
        Hybrid retrieval pipeline.
        """

        logger.info("Starting hybrid retrieval pipeline")

        if top_k is not None:
            final_top_k = top_k

        normalized_query = normalize_query(query)

        logger.info(f"Normalized query: {normalized_query}")

        keyword_results = self.keyword_search(
            normalized_query=normalized_query,
            top_k=keyword_top_k,
        )

        # =====================================
        # Skill Query Precision Guard
        # =====================================

        query_tokens = query.lower().split()

        is_short_skill_query = len(query_tokens) <= 3

        if is_short_skill_query and not keyword_results:
            logger.info(
                "Short skill query with no keyword hits. Skipping semantic fallback."
            )

            return []

        # =====================================
        # Semantic Retrieval
        # =====================================

        semantic_results = self.semantic_search(
            normalized_query=normalized_query,
            top_k=semantic_top_k,
        )

        # =====================================
        # Weighted Hybrid Fusion
        # =====================================

        combined_scores = {}

        SEMANTIC_WEIGHT = 0.7
        KEYWORD_WEIGHT = 0.3

        for chunk, semantic_score in semantic_results:
            chunk_text = chunk["text"]

            if chunk_text not in combined_scores:
                combined_scores[chunk_text] = {
                    "chunk": chunk,
                    "score": 0.0,
                }

            combined_scores[chunk_text]["score"] += semantic_score * SEMANTIC_WEIGHT

        for chunk, keyword_score in keyword_results:
            chunk_text = chunk["text"]

            if chunk_text not in combined_scores:
                combined_scores[chunk_text] = {
                    "chunk": chunk,
                    "score": 0.0,
                }

            combined_scores[chunk_text]["score"] += keyword_score * KEYWORD_WEIGHT

        logger.info(f"Combined scored chunks: {len(combined_scores)}")

        # =====================================
        # Sort By Final Score
        # =====================================

        sorted_chunks = sorted(
            [(value["chunk"], value["score"]) for value in combined_scores.values()],
            key=lambda x: x[1],
            reverse=True,
        )

        MIN_RETRIEVAL_SCORE = 0.25

        filtered_chunks = [
            (chunk, score)
            for chunk, score in sorted_chunks
            if score >= MIN_RETRIEVAL_SCORE
        ]

        unique_chunks = [chunk for chunk, score in filtered_chunks]
        logger.info(f"Filtered chunk count: {len(unique_chunks)}")

        for rank, (chunk, score) in enumerate(
            sorted_chunks[:5],
            start=1,
        ):
            logger.info(
                f"[Hybrid Score {rank}] "
                f"score={score:.4f} "
                f"section={chunk['section']} "
                f"chunk={chunk['text'][:120]}"
            )

        if not unique_chunks:
            logger.warning("No chunks passed retrieval threshold")

            return []

        # =====================================
        # Reranking
        # =====================================

        reranked_chunks = Reranker.rerank(
            query=query,
            chunks=unique_chunks,
            top_k=final_top_k,
        )

        logger.info(f"Final retrieved chunks: {len(reranked_chunks)}")

        return reranked_chunks
