from TextUnit import TextUnit
from count_word import count_words
from split_long_text import split_long_text

def normalize_units(units: list[TextUnit], chunk_size: int) -> list[TextUnit]:
    result = [] 

    for unit in units: 
        if count_words(unit.text) <= chunk_size: 
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