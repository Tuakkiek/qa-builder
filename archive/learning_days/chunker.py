#import một thành phần từ file khác.
from day04 import extract_md
#def hàm dùng đếm số lượng từ trong một đoạn văn bản.
def count_word(text: str) -> int: 
    #tách chuỗi text thành 1 list các từ.
    return len(text.split())