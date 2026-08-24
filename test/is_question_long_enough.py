def is_question_long_enough(question: str, min_words: int = 5) -> bool: 
    word_count = len(question.split())

    return word_count >= min_words

print(is_question_long_enough("What is AI?"))