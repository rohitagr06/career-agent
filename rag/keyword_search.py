from __future__ import annotations

import re

from rank_bm25 import BM25Okapi

from config.logging_config import logger


class KeywordSearch:
    @staticmethod
    def tokenize(
        text: str,
    ) -> list[str]:

        text = text.lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text,
        )

        return text.split()

    @classmethod
    def search(
        cls,
        query: str,
        chunks: list[dict],
        top_k: int = 5,
    ) -> list[tuple[dict, float]]:
        """
        BM25 keyword retrieval.
        """

        logger.info("Starting keyword retrieval")

        if not chunks:
            logger.warning("No chunks available for keyword retrieval")
            return []

        tokenized_chunks = [cls.tokenize(chunk["text"]) for chunk in chunks]

        if not tokenized_chunks:
            logger.warning("Tokenized chunks are empty")
            return []

        bm25 = BM25Okapi(tokenized_chunks)

        tokenized_query = cls.tokenize(query)

        scores = bm25.get_scores(tokenized_query)

        scored_chunks = list(
            zip(
                chunks,
                scores,
            )
        )

        scored_chunks.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        filtered_chunks = [
            (chunk, float(score)) for chunk, score in scored_chunks if score > 0
        ]

        logger.info(
            f"Keyword retrieval completed. Retrieved {len(filtered_chunks[:top_k])} chunks"
        )

        return filtered_chunks[:top_k]
