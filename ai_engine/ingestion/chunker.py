"""Overlapping fixed-size text chunking with exact source-span metadata,
so any chunk handed to the model (and any excerpt it quotes back) can be
traced to a precise [char_start, char_end) slice of the original document.
"""

from dataclasses import dataclass

DEFAULT_CHUNK_SIZE = 1500
DEFAULT_OVERLAP = 200


@dataclass
class Chunk:
    source_url: str
    institution: str
    chunk_index: int
    char_start: int
    char_end: int
    text: str


def chunk_text(
    text: str,
    source_url: str,
    institution: str,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[Chunk]:
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    chunks: list[Chunk] = []
    start = 0
    index = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk_str = text[start:end]
        if chunk_str.strip():
            chunks.append(
                Chunk(
                    source_url=source_url,
                    institution=institution,
                    chunk_index=index,
                    char_start=start,
                    char_end=end,
                    text=chunk_str,
                )
            )
            index += 1
        if end == text_length:
            break
        start = end - overlap

    return chunks
