from typing import TypedDict


class Chunk(TypedDict):
    text: str
    section: str


class RetrievedChunk(TypedDict):
    text: str
    section: str
    score: float
