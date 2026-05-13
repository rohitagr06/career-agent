import re

from config.logging_config import logger


class ResponseFormatter:
    """
    Formats recruiter-facing responses.
    """

    @staticmethod
    def clean_response(text: str) -> str:
        logger.info("Formatting assistant response")

        # =====================================
        # Remove Excess Spaces
        # =====================================

        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)

        # =====================================
        # Normalize Bullet Points
        # =====================================

        text = text.replace("•", "-")

        # =====================================
        # Remove Trailing Spaces
        # =====================================

        lines = [line.strip() for line in text.split("\n")]

        text = "\n".join(lines)

        # =====================================
        # Clean Empty Lines
        # =====================================

        cleaned_lines = []
        previous_empty = False

        for line in lines:
            is_empty = not line.strip()
            if is_empty and previous_empty:
                continue

            cleaned_lines.append(line)
            previous_empty = is_empty

        formatted_text = "\n".join(cleaned_lines).strip()
        logger.info("Response formatting completed")

        return formatted_text
