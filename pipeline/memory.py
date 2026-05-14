from typing import TypedDict

from config.logging_config import logger


class Message(TypedDict):
    role: str
    content: str


MAX_RECENT_MESSAGES = 6
MAX_SUMMARY_CHARACTERS = 1500


class ConversationMemory:
    """
    Handles recruiter conversation memory.
    """

    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self.messages: list[Message] = []
        self.summary = ""

    # =====================================
    # Add User Message
    # =====================================

    def add_user_message(self, message: str) -> None:
        logger.info("Adding recruiter message to memory")

        self.messages.append(
            {
                "role": "user",
                "content": message,
            }
        )
        self._trim_memory()

    # =====================================
    # Add Assistant Message
    # =====================================

    def add_assistant_message(self, message: str) -> None:
        logger.info("Adding assistant response to memory")
        self.messages.append(
            {
                "role": "assistant",
                "content": message,
            }
        )

        self._trim_memory()

    # =====================================
    # Get Conversation Context
    # =====================================

    def get_context(self) -> str:

        logger.info("Building conversation memory context")
        formatted_messages = []

        # =====================================
        # Historical Summary
        # =====================================

        if self.summary:
            formatted_messages.append(f"Conversation Summary:\n{self.summary}")

        # =====================================
        # Recent Messages
        # =====================================

        recent_messages = self.messages[-MAX_RECENT_MESSAGES:]
        for message in recent_messages:
            if message["role"] == "user":
                formatted_messages.append(f"Recruiter: {message['content']}")

            elif message["role"] == "assistant":
                formatted_messages.append(f"Assistant: {message['content']}")

        return "\n\n".join(formatted_messages)

    # =====================================
    # Trim Old Messages
    # =====================================

    def _trim_memory(self) -> None:
        """
        Keep only recent conversation messages.
        """

        if len(self.messages) > self.max_messages:
            self.summarize_old_messages()

    def summarize_old_messages(self) -> None:
        """
        Compress older conversation history.
        """

        logger.info("Summarizing older memory messages")

        if len(self.messages) < self.max_messages:
            return

        old_messages = self.messages[:-MAX_RECENT_MESSAGES]
        summary_lines = []

        for message in old_messages:
            role = "Recruiter" if message["role"] == "user" else "Assistant"

            summary_lines.append(f"{role}: {message['content']}")

        summarized_text = "\n".join(summary_lines)

        self.summary += "\n" + summarized_text if self.summary else summarized_text

        self.summary = self.summary[-MAX_SUMMARY_CHARACTERS:]

        # Keep only recent messages
        self.messages = self.messages[-MAX_RECENT_MESSAGES:]

    # =====================================
    # Clear Memory
    # =====================================

    def clear(self) -> None:

        logger.info("Clearing conversation memory")

        self.messages = []
        self.summary = ""
