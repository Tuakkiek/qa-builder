#import hàm extract_md và class TextUnit từ file day05.
from day05 import extract_md, TextUnit

#def hàm dùng để đếm số từ.
def count_words(text: str) -> int:
    return len(text.split())

#def hàm gom các đoạn văn (units) thành các khối lớn (chunks) theo giới hạn số từ.
def chunk_text(
    units: list[TextUnit],
    #giới hạn mặc định mỗi chunk là 300 từ.
    chunk_size: int = 300
) -> list[str]:

    #tạo list rỗng chứa các chunk thành phẩm
    chunks: list[str] = []

    #list tạm để gom chữ cho chunk hiện tại.
    current_chunk: list[str] = []
    #biến đếm tổng số từ của chunk tạm.
    current_word_count = 0

    for unit in units:
        #đếm số từ của đoạn văn đang xét
        unit_word_count = count_words(unit.text)

        #Nếu như chunk tạm đang có chữ + việc thêm đoạn mới vào bị vượt giới hạn 300 từ -> chốt chunk cũ
        if current_chunk and current_word_count + unit_word_count > chunk_size:

            #nối các đoạn trong list tạm thành 1 chuỗi, cách nhau 2 lần xuống dòng
            chunk_text_value = "\n\n".join(current_chunk)

            #lưu chunk vừa chốt vào list thành phẩm
            chunks.append(chunk_text_value)

            #reset list tạm và biến đếm để chuẩn bị gom chunk mới
            current_chunk = []
            current_word_count = 0

        #gom đoạn văn hiện tại vào list tạm
        current_chunk.append(unit.text)
        #cộng dồn số từ.
        current_word_count += unit_word_count

    #gọi thêm lần cuối để lưu chunk còn đang gom dở khi hết vòng lặp.
    if current_chunk:
        chunk_text_value = "\n\n".join(current_chunk)
        chunks.append(chunk_text_value)

    return chunks

#gọi hàm extract_md để xử lý file.
units = extract_md("data/giao-trinh-ttnt.md")
#gọi hàm chunk_text để gom đoạn với giới hạn 300 từ.
chunks = chunk_text(units, chunk_size=300)
#in ra màn hình các chunk đã chia.
for index, chunk in enumerate(chunks, start=1):
    print(f"chunk {index}")
    print(f"Word count: {count_words(chunk)}")
    print(chunk)
    print()