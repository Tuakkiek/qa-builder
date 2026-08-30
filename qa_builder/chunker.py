import re
from pathlib import Path

from .models import Chunk, TextUnit


def count_words(text: str) -> int:
    return len(text.split())


def split_sentences(text: str) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def split_by_words(text: str, chunk_size: int) -> list[str]:
    words = text.split()
    parts = []

    for i in range(0, len(words), chunk_size):
        part_words = words[i:i + chunk_size]
        parts.append(" ".join(part_words))

    return parts


def split_long_text(text: str, chunk_size: int) -> list[str]:
    sentences = split_sentences(text)
    parts = []
    current_sentences = []
    current_word_count = 0

    for sentence in sentences:
        sentence_word_count = count_words(sentence)

        if sentence_word_count > chunk_size:
            if current_sentences:
                parts.append(" ".join(current_sentences))
                current_sentences = []
                current_word_count = 0

            parts.extend(split_by_words(sentence, chunk_size))
            continue

        if current_word_count + sentence_word_count > chunk_size:
            parts.append(" ".join(current_sentences))
            current_sentences = [sentence]
            current_word_count = sentence_word_count
        else:
            current_sentences.append(sentence)
            current_word_count += sentence_word_count

    if current_sentences:
        parts.append(" ".join(current_sentences))

    return parts


def get_overlap_text(text: str, overlap_size: int) -> str:
    if overlap_size <= 0:
        return ""

    words = text.split()
    overlap_words = words[-overlap_size:]

    return " ".join(overlap_words)


def chunk_text(
    units: list[TextUnit],
    chunk_size: int = 300,
    overlap_ratio: float = 0.15,
) -> list[Chunk]:
    if not units:
        return []

    chunk_texts: list[str] = []
    current_parts: list[str] = []
    current_word_count = 0
    overlap_size = int(chunk_size * overlap_ratio)

    for unit in units:
        unit_parts = split_long_text(unit.text, chunk_size)

        for part in unit_parts:
            part_word_count = count_words(part)

            if current_word_count + part_word_count > chunk_size:
                if current_parts:
                    saved_text = " ".join(current_parts)
                    chunk_texts.append(saved_text)
                    overlap_text = get_overlap_text(saved_text, overlap_size)

                    current_parts = []
                    current_word_count = 0

                    if overlap_text:
                        current_parts.append(overlap_text)
                        current_word_count = count_words(overlap_text)

                current_parts.append(part)
                current_word_count += part_word_count
            else:
                current_parts.append(part)
                current_word_count += part_word_count

    if current_parts:
        chunk_texts.append(" ".join(current_parts))

    source_file = units[0].source_file
    file_name = Path(source_file).stem
    chunks: list[Chunk] = []

    for i, text in enumerate(chunk_texts, start=1):
        chunks.append(
            Chunk(
                chunk_id=f"{file_name}_chunk{i:04d}",
                text=text,
                source_file=source_file,
                word_count=count_words(text),
            )
        )

    return chunks
