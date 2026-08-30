import re
from dataclasses import dataclass
from pathlib import Path


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


def count_words(text: str) -> int:
    return len(text.split())


def split_sentences(text: str) -> list[str]:

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def split_by_words(
    text: str,
    chunk_size: int
) -> list[str]:

    words = text.split()

    parts = []

    for i in range(0, len(words), chunk_size):

        part_words = words[i:i + chunk_size]

        parts.append(
            " ".join(part_words)
        )

    return parts


def split_long_text(
    text: str,
    chunk_size: int
) -> list[str]:

    sentences = split_sentences(text)

    parts = []

    current_sentences = []
    current_word_count = 0

    for sentence in sentences:

        sentence_word_count = count_words(sentence)

        if sentence_word_count > chunk_size:

            if current_sentences:

                parts.append(
                    " ".join(current_sentences)
                )

                current_sentences = []
                current_word_count = 0

            parts.extend(
                split_by_words(
                    sentence,
                    chunk_size
                )
            )

            continue

        if (
            current_word_count + sentence_word_count
            > chunk_size
        ):

            parts.append(
                " ".join(current_sentences)
            )

            current_sentences = [sentence]
            current_word_count = sentence_word_count

        else:

            current_sentences.append(sentence)

            current_word_count += sentence_word_count

    if current_sentences:

        parts.append(
            " ".join(current_sentences)
        )

    return parts


def chunk_text(
    units: list[TextUnit],
    chunk_size: int = 300
) -> list[Chunk]:

    chunk_texts = []

    current_parts = []
    current_word_count = 0

    for unit in units:

        unit_parts = split_long_text(
            unit.text,
            chunk_size
        )

        for part in unit_parts:

            part_word_count = count_words(part)

            if (
                current_word_count + part_word_count
                > chunk_size
            ):

                if current_parts:

                    chunk_texts.append(
                        " ".join(current_parts)
                    )

                current_parts = [part]
                current_word_count = part_word_count

            else:

                current_parts.append(part)

                current_word_count += part_word_count

    if current_parts:

        chunk_texts.append(
            " ".join(current_parts)
        )

    if not units:
        return []

    source_file = units[0].source_file

    file_name = Path(source_file).stem

    chunks = []

    for i, text in enumerate(
        chunk_texts,
        start=1
    ):

        chunk = Chunk(
            chunk_id=f"{file_name}_chunk{i:04d}",
            text=text,
            source_file=source_file,
            word_count=count_words(text)
        )

        chunks.append(chunk)

    return chunks


units = [
    TextUnit(
        text="Machine Learning là một nhánh của AI.",
        source_file="ai.md",
        section_title="Machine Learning"
    ),

    TextUnit(
        text="Machine Learning cho phép máy tính học từ dữ liệu.",
        source_file="ai.md",
        section_title="Machine Learning"
    ),

    TextUnit(
        text="Học có giám sát là sử dụng tập dữ liệu có nhãn.",
        source_file="ai.md",
        section_title="Deep Learning"
    )
]


chunks = chunk_text(
    units,
    chunk_size=20
)


for chunk in chunks:

    print("ID:", chunk.chunk_id)

    print(
        "Source:",
        chunk.source_file
    )

    print(
        "Words:",
        chunk.word_count
    )

    print(
        "Text:",
        chunk.text
    )

    print("-" * 50)