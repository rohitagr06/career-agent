import pickle
from pathlib import Path

import faiss

from config.logging_config import logger
from core.types import Chunk

# =====================================
# Paths
# =====================================

BASE_DIR = Path("data")

INDEX_DIR = BASE_DIR / "indexes"

FAISS_INDEX_PATH = INDEX_DIR / "faiss.index"
CHUNKS_PATH = INDEX_DIR / "chunks.pkl"
METADATA_PATH = INDEX_DIR / "metadata.pkl"


# =====================================
# Directory Setup
# =====================================

INDEX_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# =====================================
# FAISS Index Persistence
# =====================================


def save_faiss_index(index) -> None:

    logger.info("Saving FAISS index")

    faiss.write_index(
        index,
        str(FAISS_INDEX_PATH),
    )

    logger.info(f"FAISS index saved at: {FAISS_INDEX_PATH}")


def load_faiss_index():

    logger.info("Loading FAISS index")

    if not FAISS_INDEX_PATH.exists():
        raise FileNotFoundError("FAISS index not found. Run build_index.py first.")

    index = faiss.read_index(str(FAISS_INDEX_PATH))

    logger.info("FAISS index loaded successfully")

    return index


# =====================================
# Chunk Persistence
# =====================================


def save_chunks(chunks: list[str]) -> None:

    logger.info("Saving document chunks")

    with open(
        CHUNKS_PATH,
        "wb",
    ) as file:
        pickle.dump(
            chunks,
            file,
        )

    logger.info(f"Chunks saved at: {CHUNKS_PATH}")


def load_chunks() -> list[Chunk]:

    logger.info("Loading document chunks")

    if not CHUNKS_PATH.exists():
        raise FileNotFoundError("Chunks file not found. Run build_index.py first.")

    with open(
        CHUNKS_PATH,
        "rb",
    ) as file:
        chunks = pickle.load(file)

    logger.info("Chunks loaded successfully")

    return chunks


# =====================================
# Metadata Persistence
# =====================================


def save_metadata(
    metadata: list[dict],
) -> None:

    logger.info("Saving metadata")

    with open(
        METADATA_PATH,
        "wb",
    ) as file:
        pickle.dump(
            metadata,
            file,
        )

    logger.info(f"Metadata saved at: {METADATA_PATH}")


def load_metadata() -> list[dict]:

    logger.info("Loading metadata")

    if not METADATA_PATH.exists():
        raise FileNotFoundError("Metadata file not found. Run build_index.py first.")

    with open(
        METADATA_PATH,
        "rb",
    ) as file:
        metadata = pickle.load(file)

    logger.info("Metadata loaded successfully")

    return metadata


# =====================================
# Helper
# =====================================


def index_exists() -> bool:

    return FAISS_INDEX_PATH.exists() and CHUNKS_PATH.exists() and METADATA_PATH.exists()
