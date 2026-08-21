def split_by_words(text, chunk_size): 
    words = text.split() 

    parts = [] 

    for i in range(0, len(words), chunk_size): 
        part_words = words[i:i + chunk_size] 

        parts.append(" ".join(part_words))

    return parts 

text = "Không chín không chiên bò viên không chiên không chín"
print(split_by_words(text, 2))

