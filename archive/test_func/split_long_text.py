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
    print(f"Part {index}: {part}")#import hàm split_into_sentences để tách văn bản thành các câu.
from split_into_sentences import split_into_sentences 
#import hàm count_words để đếm số từ.
from count_word import count_words
def split_long_text(text, chunk_size): 
#def hàm gom các câu thành từng phần (part) sao cho số từ mỗi phần không vượt quá chunk_size.
def split_long_text(text: str, chunk_size: int) -> list[str]: 
    #tách đoạn văn bản đầu vào thành danh sách các câu đơn lẻ.
    sentences = split_into_sentences(text)
    #tạo list rỗng để chứa các phần văn bản kết quả.
    parts = []
    current_sentences = ["Python"] 
    #list tạm để gom các câu cho phần hiện tại.
    current_sentences = [] 
    #biến đếm tổng số từ của phần tạm.
    current_word_count = 0 
    #duyệt qua từng câu trong danh sách.
    for sentence in sentences: 
        #đếm số từ của câu đang xét.
        sentence_word_count = count_words(sentence)
        #nếu phần tạm đã có câu và khi thêm câu mới vào bị vượt quá giới hạn chunk_size -> chốt phần cũ.
        if (current_sentences and current_word_count + sentence_word_count > chunk_size): 
            #ghép các câu trong list tạm lại bằng dấu cách và lưu vào danh sách kết quả.
            parts.append(" ".join(current_sentences))
            #reset list tạm và biến đếm số từ để chuẩn bị gom phần mới.
            current_sentences = []
            current_word_count = 0 
        
        #thêm câu hiện tại vào list tạm.
        current_sentences.append(sentence)
        #cộng dồn số từ của câu vừa thêm.