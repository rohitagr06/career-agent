from pydantic import BaseModel, Field
from typing import Optional

# =====================================
# Chat Request Schema
# =====================================


class ChatRequest(BaseModel):
    """
    Incoming recruiter/user query.
    """

    message: str = Field(
        ...,
        description="User input message",
        min_length=1,
        max_length=4000,
    )


# =====================================
# Chat Response Schema
# =====================================


class ChatResponse(BaseModel):
    """
    Final AI assistant response.
    """

    answer: str = Field(
        ...,
        description="Assistant response",
    )

    model_used: str = Field(
        ...,
        description="Model used for generation",
    )

    fallback_triggered: bool = Field(
        default=False,
        description="Whether fallback model was used",
    )


# =====================================
# Retrieval Chunk Schema
# =====================================


class RetrievalChunk(BaseModel):
    """
    Retrieved RAG document chunk.
    """

    content: str = Field(
        ...,
        description="Chunk content",
    )

    source: str = Field(
        ...,
        description="Document source",
    )

    score: Optional[float] = Field(
        default=None,
        description="Retrieval similarity score",
    )
