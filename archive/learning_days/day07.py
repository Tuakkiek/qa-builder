from day05 import extract_md, TextUnit


def count_words(text: str) -> int:
    return len(text.split())


def chunk_text(
    units: list[TextUnit],
    chunk_size: int = 300
) -> list[str]:

    chunks: list[str] = []

    current_chunk: list[str] = []
    current_word_count = 0

    for unit in units:
        unit_word_count = count_words(unit.text)

        if current_chunk and current_word_count + unit_word_count > chunk_size:

            chunk_text_value = "\n\n".join(current_chunk)

            chunks.append(chunk_text_value)

            current_chunk = []
            current_word_count = 0

        current_chunk.append(unit.text)
        current_word_count += unit_word_count

    if current_chunk:
        chunk_text_value = "\n\n".join(current_chunk)
        chunks.append(chunk_text_value)

    return chunks


units = extract_md("data/giao-trinh-ttnt.md")

chunks = chunk_text(units, chunk_size=300)

for index, chunk in enumerate(chunks, start=1):
    print(f"chunk {index}")
    print(f"Word count: {count_words(chunk)}")
    print(chunk)
    print()