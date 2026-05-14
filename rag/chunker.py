import re

from config.logging_config import logger
from core.types import Chunk

# =====================================
# Chunk Filtering Rules
# =====================================


MIN_CHUNK_LENGTH = 40

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
        r"(?=professional summary)",
        r"(?=work experience)",
        r"(?=technical skills)",
        r"(?=achievements)",
        r"(?=patents)",
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
    Split text into sentences and resume bullets.
    """

    return re.split(
        r"(?<=[.!?])\s+|\n+|(?=•)",
        text,
    )


def split_large_section(
    section: str,
    chunk_size: int = 350,
    overlap: int = 1,
) -> list[str]:
    """
    Sentence-aware chunking.
    """

    sentences = sentence_split(section)

    chunks = []

    current_chunk: list[str] = []
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


def detect_section_name(section: str) -> str:
    """
    Detect resume section type.
    """

    section_lower = section.lower()

    if "experience" in section_lower:
        return "experience"

    if "project" in section_lower:
        return "projects"

    if "skill" in section_lower:
        return "skills"

    if "certification" in section_lower:
        return "certifications"

    if "education" in section_lower:
        return "education"

    return "general"


def chunk_text(text: str) -> list[Chunk]:
    """
    Production-style semantic chunking.
    """

    logger.info("Starting semantic document chunking")

    cleaned_text = clean_text(text)

    sections = split_sections(cleaned_text)

    final_chunks: list[Chunk] = []

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

            # if any(noise in clean_chunk.lower() for noise in NOISE_PATTERNS):
            #     continue

            section_name = detect_section_name(section)

            chunk_final: Chunk = {
                "text": clean_chunk,
                "section": section_name,
            }

            final_chunks.append(chunk_final)

    # =====================================
    # Final Noise Cleanup
    # =====================================

    final_chunks = remove_noisy_chunks(final_chunks)

    logger.info(f"Chunking completed. Total chunks: {len(final_chunks)}")

    return final_chunks


def remove_noisy_chunks(
    chunks: list[Chunk],
) -> list[Chunk]:
    """
    Remove low-value chunks.
    """

    blocked_terms = [
        "cooking",
        "hobbies",
        "languages",
        "mobile",
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
        "madhya pradesh",
    ]

    filtered_chunks: list[Chunk] = []

    for chunk in chunks:
        text = chunk["text"]
        normalized = text.lower()
        word_count = len(text.split())
        if word_count < 5:
            continue

        if any(term in normalized for term in blocked_terms):
            continue

        filtered_chunks.append(chunk)

    return filtered_chunks
