from dataclasses import dataclass


@dataclass
class TextUnit:
    text: str
    source_file: str
    section_title: str | None = None


@dataclass
class Chunk:
    chunk_id: str
    text: str
    source_file: str
    word_count: int

