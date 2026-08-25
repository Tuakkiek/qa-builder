from dataclasses import dataclass

@dataclass
class Chunk:
    chunk_id: str
    text: str
    source_file: str
    word_count: int