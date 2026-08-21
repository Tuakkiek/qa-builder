from split_into_sentences import split_into_sentences
from count_word import count_words

def split_by_words(text, chunk_size): 
    words = text.split()

    parts = [] 
    for i in range(0, len(words), chunk_size): 
        part_words = words[i:i + chunk_size] 

        parts.append(" ".join(part_words))

    return parts

def split_long_text(text, chunk_size): 
    sentences = split_into_sentences(text)

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

            word_parts = split_by_words(sentence, chunk_size)

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

text = "Khum chín khum chiên bò viênn khum chiên khum chín"
result = split_long_text(text, 2)

for index,part in enumerate(result, start=1): 
    print(f"Part {index}: {part}")
