def get_overlap_text(text, overlap_words): 
    if overlap_words <= 0: 
        return ""
    
    words = text.split() 

    return " ".join(words[-overlap_words:])

text = "Python is esay. It is popular and very useful"

print(get_overlap_text(text, 6))