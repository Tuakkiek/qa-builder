import re 
from dataclasses import dataclass

@dataclass 
class TextUnit: 
    text: str
    source_file: str
    section_title: str | None = None 

def count_words(text: str) -> int: 
    return len(text.split())

def split_sentences(text: str) -> list[str]: 
    sentences = re.split(r"(?<=[.!?])\s+", text)

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

def split_by_word(text: str, chunk_size: int) -> list[str]: 
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
            
            word_parts = split_by_word(sentence, chunk_size)

            parts.extend(word_parts)

            continue 
        
        if (current_sentences and sentence_word_count + current_word_count > chunk_size): 
            parts.append(" ".join(current_sentences))

            current_sentences = [] 
            current_word_count = 0 

        current_sentences.append(sentence)
        current_word_count += sentence_word_count

    if current_sentences: 
        parts.append(" ".join(current_sentences))

    return parts

def normalize_units( units: list[TextUnit], chunk_size: int) -> list[TextUnit]: 
    result = [] 

    for unit in units: 
        word_count = count_words(unit.text)

        if word_count <= chunk_size: 
            result.append(unit)
            continue
        
        parts = split_long_text(unit.text, chunk_size) 

        for part in parts: 
            result.append(
                TextUnit(
                    text = part, 
                    source_file = unit.source_file, 
                    section_title = unit.section_title
                )
            )

    return result


sentence = (
    "Khum chín khum chiên bò viênn khum chiên khum chín"
    "Chuồn chuồn bay thấp thì cao, bay cao thì thấp, bay vừa thì thôi."
)

long_text = " ".join(
    sentence
    for _ in range(50)
)

unit = TextUnit(
    text=long_text,
    source_file="python.md",
    section_title="Python"
)

units = [unit]

normalized_units = normalize_units(
    units,
    chunk_size=300
)

for index, item in enumerate(
    normalized_units,
    start=1
):
    print(
        f"Part {index}: "
        f"{count_words(item.text)} words"
    )