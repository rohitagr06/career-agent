import re

from config.logging_config import logger

# =====================================
# Chunk Filtering Rules
# =====================================

MIN_CHUNK_LENGTH = 120

NOISE_PATTERNS = [
    "linkedin",
    "mobile",
    "contact",
    "languages",
    "page 3 of",
    "page 2 of",
    "page 1 of",
]


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.
    """

    text = re.sub(r"\n{2,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def split_sections(
    text: str,
) -> list[str]:
    """
    Split resume into meaningful sections.
    """

    patterns = [
        r"(?=summary)",
        r"(?=experience)",
        r"(?=projects)",
        r"(?=skills)",
        r"(?=education)",
        r"(?=certifications)",
    ]

    combined_pattern = "|".join(patterns)

    sections = re.split(
        combined_pattern,
        text,
        flags=re.IGNORECASE,
    )

    cleaned_sections = []

    for section in sections:
        section = section.strip()

        if len(section) < 80:
            continue

        cleaned_sections.append(section)

    return cleaned_sections


def sentence_split(
    text: str,
) -> list[str]:
    """
    Split text into sentences.
    """

    return re.split(
        r"(?<=[.!?])\s+",
        text,
    )


def split_large_section(
    section: str,
    chunk_size: int = 700,
    overlap: int = 2,
) -> list[str]:
    """
    Sentence-aware chunking.
    """

    sentences = sentence_split(section)

    chunks = []

    current_chunk = []
    current_length = 0

    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue

        sentence_length = len(sentence)

        # if chunk becomes too large
        if current_length + sentence_length > chunk_size:
            chunks.append(" ".join(current_chunk))

            # keep overlap sentences
            current_chunk = current_chunk[-overlap:]

            current_length = len(" ".join(current_chunk))

        current_chunk.append(sentence)

        current_length += sentence_length

    # last chunk
    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks


def chunk_text(text: str) -> list[str]:
    """
    Production-style semantic chunking.
    """

    logger.info("Starting semantic document chunking")

    cleaned_text = clean_text(text)

    sections = split_sections(cleaned_text)

    final_chunks = []

    for section in sections:
        section_chunks = split_large_section(section)

        for chunk in section_chunks:
            clean_chunk = chunk.strip()

            # =====================================
            # Skip Tiny Chunks
            # =====================================

            if len(clean_chunk) < MIN_CHUNK_LENGTH:
                continue

            # =====================================
            # Skip Noisy Chunks
            # =====================================

            if any(noise in clean_chunk.lower() for noise in NOISE_PATTERNS):
                continue

            final_chunks.append(clean_chunk)

    # =====================================
    # Final Noise Cleanup
    # =====================================

    final_chunks = remove_noisy_chunks(final_chunks)

    logger.info(f"Chunking completed. Total chunks: {len(final_chunks)}")

    return final_chunks


def remove_noisy_chunks(
    chunks: list[str],
) -> list[str]:
    """
    Remove low-value chunks.
    """

    blocked_terms = [
        "cooking",
        "hobbies",
        "languages",
        "mobile",
        "linkedin",
        "email",
        "page 1 of",
        "page 2 of",
        "page 3 of",
        "page 4 of",
        "schooling",
        "city central",
        "1995",
        "2008",
        "intermediate",
        "h.s. school",
    ]

    filtered_chunks = []

    for chunk in chunks:
        normalized = chunk.lower()

        if any(term in normalized for term in blocked_terms):
            continue

        filtered_chunks.append(chunk)

    return filtered_chunks
