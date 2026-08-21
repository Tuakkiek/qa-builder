from split_into_sentences import split_into_sentences 
from count_word import count_words

def split_long_text(text, chunk_size): 
    sentences = split_into_sentences(text)

    parts = []

    current_sentences = ["Python"] 
    current_word_count = 0 

    for sentence in sentences: 
        sentence_word_count = count_words(sentence)

        if (current_sentences and current_word_count + sentence_word_count > chunk_size): 
            parts.append(" ".join(current_sentences))

            current_sentences = []
            current_word_count = 0 
        
        current_sentences.append(sentence)
        current_word_count += sentence_word_count
        
    if current_sentences: 
        parts.append(" ".join(current_sentences))

    return parts

text = """
Python là ngôn ngữ lập trình. Nó rất phổ biến. 
Python có dễ đọc không? Theo tôi là khum!
"""

parts = split_long_text(text, 8) 

for index, part in enumerate(parts, start=1): 
    print(f"Part {index}: {part}")