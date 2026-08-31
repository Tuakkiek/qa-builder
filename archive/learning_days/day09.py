import re 
#import dataclass để tạo class lưu trữ dữ liệu nhanh.
from dataclasses import dataclass

#tạo class TextUnit lưu nội dung, tên file và tên mục (section).
@dataclass 
class TextUnit: 
    text: str
    source_file: str
    section_title: str | None = None 

#def hàm dùng để đếm số từ.
def count_words(text: str) -> int: 
    return len(text.split())

#def hàm tách chuỗi dài thành các câu lẻ dựa vào dấu câu.
def split_sentences(text: str) -> list[str]: 
    #tách chuỗi bằng regex, giữ lại dấu chấm, hỏi, than (?<=[.!?]) và cắt tại khoảng trắng \s+
    sentences = re.split(r"(?<=[.!?])\s+", text)

    #trả về list các câu đã được làm sạch
    return [
        #xóa khoảng trắng 2 lề
        sentence.strip()
        #duyệt qua từng câu trong list sentences
        for sentence in sentences
        #chỉ lấy những câu ko bị rỗng
        if sentence.strip()
    ]

#def hàm cắt một câu quá dài thành các đoạn nhỏ theo đúng số lượng từ.
def split_by_word(text: str, chunk_size: int) -> list[str]: 
    #tách câu thành list các từ
    words = text.split() 

    #tạo list rỗng để chứa các phần nhỏ
    parts = [] 

    #duyệt từ đầu đến cuối list từ, mỗi bước nhảy = chunk_size
    for i in range(0, len(words), chunk_size): 
        #cắt lấy 1 đoạn từ vị trí i đến i + chunk_size
        part_words = words[i:i + chunk_size]

        #nối các từ lại thành chuỗi và thêm vào list parts
        parts.append(" ".join(part_words))

    #trả về list các phần đã cắt
    return parts

#def hàm chia một văn bản dài thành các phần nhỏ (ưu tiên chia theo câu).
def split_long_text(text: str, chunk_size: int) -> list[str]: 
    #gọi hàm tách văn bản thành list các câu
    sentences = split_sentences(text) 

    #tạo list rỗng chứa kết quả
    parts = [] 

    #tạo list tạm chứa các câu đang gom
    current_sentences = [] 
    #biến đếm số từ của phần đang gom
    current_word_count = 0 

    #duyệt qua từng câu
    for sentence in sentences: 
        #đếm số từ của câu hiện tại
        sentence_word_count = count_words(sentence)

        #nếu bản thân câu này dài hơn mức cho phép (chunk_size)
        if sentence_word_count > chunk_size: 
            #nếu đang có gom câu nào dở dang thì chốt luôn
            if current_sentences: 
                #nối các câu lại và thêm vào parts
                parts.append(" ".join(current_sentences))

                #reset list tạm
                current_sentences = [] 
                #reset biến đếm
                current_word_count = 0 
            
            #gọi hàm cắt gắt theo số từ để băm nhỏ câu siêu dài này
            word_parts = split_by_word(sentence, chunk_size)

            #thêm tất cả các phần vừa băm vào list parts
            parts.extend(word_parts)

            #bỏ qua các bước dưới, đi đến câu tiếp theo
            continue 
        
        #nếu list tạm có chữ VÀ cộng thêm câu này bị lố chunk_size -> chốt phần cũ
        if (current_sentences and sentence_word_count + current_word_count > chunk_size): 
            #nối các câu trong list tạm và thêm vào parts
            parts.append(" ".join(current_sentences))

            #reset list tạm
            current_sentences = [] 
            #reset biến đếm
            current_word_count = 0 

        #thêm câu hiện tại vào list tạm
        current_sentences.append(sentence)
        #cộng dồn số từ
        current_word_count += sentence_word_count

    #nếu chạy hết vòng lặp mà list tạm vẫn còn chữ -> chốt nốt phần cuối
    if current_sentences: 
        parts.append(" ".join(current_sentences))

    #trả về list các phần văn bản đã chia
    return parts

#def hàm chuẩn hóa danh sách units, đảm bảo ko có unit nào lố chunk_size.
def normalize_units( units: list[TextUnit], chunk_size: int) -> list[TextUnit]: 
    #tạo list rỗng chứa kết quả
    result = [] 

    #duyệt qua từng unit
    for unit in units: 
        #đếm số từ của unit
        word_count = count_words(unit.text)

        #nếu số từ nhỏ hơn hoặc bằng chunk_size -> ok, giữ nguyên
        if word_count <= chunk_size: 
            #thêm unit vào kết quả
            result.append(unit)
            #chuyển sang unit tiếp theo
            continue
        
        #nếu unit quá dài -> gọi hàm cắt nhỏ văn bản
        parts = split_long_text(unit.text, chunk_size) 

        #duyệt qua từng phần văn bản vừa cắt
        for part in parts: 
            #tạo unit mới cho từng phần, kế thừa thông tin từ unit gốc
            result.append(
                TextUnit(
                    #gán nội dung mới
                    text = part, 
                    #giữ nguyên tên file
                    source_file = unit.source_file, 
                    #giữ nguyên tiêu đề
                    section_title = unit.section_title
                )
            )

    #trả về danh sách unit đã chuẩn hóa
    return result


#Code bên dưới dùng để tạo dữ liệu giả và test logic chuẩn hóa
#tạo 1 câu mẫu
sentence = (
    "Khum chín khum chiên bò viênn khum chiên khum chín"
    "Chuồn chuồn bay thấp thì cao, bay cao thì thấp, bay vừa thì thôi."
)

#nhân câu mẫu lên 50 lần để tạo text siêu dài
long_text = " ".join(
    sentence
    for _ in range(50)
)

#tạo object TextUnit chứa câu siêu dài đó
unit = TextUnit(
    text=long_text,
    source_file="python.md",
    section_title="Python"
)

#đưa unit vào list
units = [unit]

#chạy hàm normalize_units để ép dung lượng từng unit xuống chuẩn 300 từ
normalized_units = normalize_units(
    units,
    chunk_size=300
)

#duyệt qua list đã chuẩn hóa và in ra
for index, item in enumerate(
    normalized_units,
    start=1
):
    #in ra màn hình thứ tự và số từ của từng phần
    print(
        f"Part {index}: "
        f"{count_words(item.text)} words"
    )