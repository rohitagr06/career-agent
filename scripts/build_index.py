import sys
from pathlib import Path

# ruff: noqa: E402

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.logging_config import logger
from rag.chunker import chunk_text
from rag.embeddings import generate_document_embeddings
from rag.faiss_store import FAISSStore
from rag.pdf_loader import load_knowledge_base


# =====================================
# Safe Contact Chunk
# =====================================

SAFE_CONTACT_CHUNK = """
Professional Contact Information

Email: rohitagr06@gmail.com
LinkedIn: https://www.linkedin.com/in/rohitagr06

Preferred professional communication channels:
- Email
- LinkedIn

Phone number should not be shared.
"""


def build_index() -> None:
    """
    Build persistent FAISS index.
    """

    logger.info("Starting FAISS index build")

    # =====================================
    # Load Documents
    # =====================================

    knowledge_base = load_knowledge_base()

    logger.info("Knowledge base loaded successfully")

    # =====================================
    # Chunk Documents
    # =====================================

    chunks = chunk_text(knowledge_base)

    logger.info(f"Generated {len(chunks)} chunks from documents")

    # =====================================
    # Inject Safe Contact Chunk
    # =====================================

    chunks.insert(
        0,
        {
            "text": SAFE_CONTACT_CHUNK.strip(),
            "section": "contact",
        },
    )

    logger.info("Injected safe contact information chunk")

    # =====================================
    # Remove Empty Chunks
    # =====================================

    chunks = [chunk for chunk in chunks if chunk and chunk["text"].strip()]

    logger.info(f"Final chunk count: {len(chunks)}")

    # =====================================
    # Generate Embeddings
    # =====================================

    logger.info("Generating embeddings")

    embeddings = generate_document_embeddings([chunk["text"] for chunk in chunks])

    logger.info("Embeddings generated successfully")

    # =====================================
    # Build FAISS Index
    # =====================================

    vector_store = FAISSStore()

    vector_store.build_index(
        embeddings=embeddings,
        chunks=chunks,
        metadata=[],
    )

    logger.info("FAISS index built successfully")

    # =====================================
    # Persist Index
    # =====================================

    vector_store.save()

    logger.info("FAISS index saved successfully")

    logger.info("FAISS index build completed successfully")


if __name__ == "__main__":
    build_index()
