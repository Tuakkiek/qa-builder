from day05 import extract_md, TextUnit


def count_words(text: str) -> int:
    return len(text.split())


def get_overlap_text(text: str, overlap_words: int) -> str:
    if overlap_words <= 0:
        return ""

    words = text.split()

    return " ".join(words[-overlap_words:])


def chunk_text(
    units: list[TextUnit],
    chunk_size: int = 300,
    overlap_ratio: float = 0.15
) -> list[str]:

    chunks: list[str] = []

    current_chunk: list[str] = []
    current_word_count = 0

    overlap_words = int(chunk_size * overlap_ratio)

    for unit in units:
        unit_word_count = count_words(unit.text)

        if (
            current_chunk
            and current_word_count + unit_word_count > chunk_size
        ):
            chunk_text_value = "\n\n".join(current_chunk)

            chunks.append(chunk_text_value)

            overlap_text = get_overlap_text(
                chunk_text_value,
                overlap_words
            )

            if overlap_text:
                current_chunk = [overlap_text]
                current_word_count = count_words(overlap_text)
            else:
                current_chunk = []
                current_word_count = 0

        current_chunk.append(unit.text)
        current_word_count += unit_word_count

    if current_chunk:
        chunk_text_value = "\n\n".join(current_chunk)
        chunks.append(chunk_text_value)

    return chunks


units = extract_md("data/giao-trinh-ttnt.md")

chunks = chunk_text(
    units,
    chunk_size=300,
    overlap_ratio=0.15
)

for index, chunk in enumerate(chunks, start=1):
    print(f"===== CHUNK {index} =====")
    print(f"Word count: {count_words(chunk)}")
    print(chunk)
    print()