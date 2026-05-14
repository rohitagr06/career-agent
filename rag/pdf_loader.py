from pathlib import Path

import pypdf

from config.logging_config import logger

# =====================================
# Data Paths
# =====================================

DATA_DIR = Path("data")

LINKEDIN_PDF = DATA_DIR / "linkedin.pdf"
SUMMARY_FILE = DATA_DIR / "summary.txt"

# =====================================
# PDF Extraction
# =====================================


def extract_pdf_text(pdf_path: Path) -> str:
    """
    Extract text from PDF document.
    """
    logger.info(f"Extracting PDF text from: {pdf_path}")

    reader = pypdf.PdfReader(str(pdf_path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)
    combined_text = "\n".join(pages)
    logger.info("PDF extraction completed")
    return combined_text


# =====================================
# Text File Extraction
# =====================================


def extract_text_file(file_path: Path) -> str:
    """
    Extract text from plain text file.
    """
    logger.info(f"Loading text file: {file_path}")
    text = file_path.read_text(encoding="utf-8")
    logger.info("Text file extraction completed")
    return text


# =====================================
# Combined Knowledge Loader
# =====================================


def load_knowledge_base() -> str:
    """
    Load and combine all knowledge sources.
    """
    logger.info("Loading knowledge base")
    linkedin_text = extract_pdf_text(LINKEDIN_PDF)
    summary_text = extract_text_file(SUMMARY_FILE)

    combined_knowledge = f"""
================ LINKEDIN PROFILE ================
{linkedin_text}
================ PERSONAL SUMMARY ================
{summary_text}
"""

    logger.info("Knowledge base loaded successfully")
    return combined_knowledge
