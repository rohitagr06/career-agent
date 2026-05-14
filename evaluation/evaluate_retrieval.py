import json

from rag.retriever import Retriever
from rag.vector_store import VectorStore


def evaluate():
    with open("evaluation/retrieval_eval.json") as f:
        dataset = json.load(f)

    retriever = Retriever(VectorStore())

    total = 0
    passed = 0

    for item in dataset:
        query = item["query"]
        expected_keywords = item["expected_keywords"]

        results = retriever.retrieve(
            query=query,
            final_top_k=3,
        )

        combined_text = " ".join(chunk["text"].lower() for chunk in results)

        # hit = any(keyword.lower() in combined_text for keyword in expected_keywords)
        SYNONYMS = {
            "deployment": ["deployment", "deploy", "kubernetes", "docker"],
            "infrastructure": ["infrastructure", "cloud", "kubernetes", "docker"],
            "machine learning": ["machine learning", "ml", "ai"],
        }

        matched = 0

        for keyword in expected_keywords:
            keyword = keyword.lower()

            possible_terms = SYNONYMS.get(keyword, [keyword])

            if any(term in combined_text for term in possible_terms):
                matched += 1

        hit = matched >= 2

        total += 1

        if hit:
            passed += 1

        print("=" * 60)
        print(f"Query: {query}")
        print(f"Expected: {expected_keywords}")
        print(f"Hit: {hit}")

    accuracy = (passed / total) * 100

    print("\n")
    print("=" * 60)
    print(f"Retrieval Accuracy: {accuracy:.2f}%")
    print(f"Passed: {passed}/{total}")


if __name__ == "__main__":
    evaluate()
