#import class Path để xử lý đường dẫn và lấy tên file.
from pathlib import Path 
#import dataclass Chunk từ file Chunk.
from Chunk import Chunk
#import hàm count_words để đếm số từ.
from count_word import count_words 

#def hàm đóng gói danh sách chuỗi văn bản thành danh sách đối tượng Chunk có định danh id.
def create_chunks(chunk_texts: list[str], source_file: str) -> list[Chunk]:
    
    #tạo danh sách rỗng chứa các đối tượng Chunk.
    chunks = []

    #lấy tên file bỏ phần mở rộng (ví dụ "ai.md" -> "ai").
    file_name = Path(source_file).stem

    #duyệt qua từng chuỗi văn bản kèm số thứ tự bắt đầu từ 1.
    for i, text in enumerate(chunk_texts, start=1):

        #tạo id định danh cho chunk với định dạng 4 chữ số (ví dụ ai_chunk0001).
        chunk_id = f"{file_name}_chunk{i:04d}"

        #khởi tạo đối tượng Chunk với đầy đủ thông tin.
        chunk = Chunk(
            chunk_id=chunk_id,
            text=text,
            source_file=source_file,
            word_count=count_words(text)
        )

        #thêm chunk vào danh sách kết quả.
        chunks.append(chunk)

    #trả về danh sách các chunk.
    return chunks

#danh sách các đoạn văn bản mẫu.
chunk_texts = [
    "Chọn xoài đừng để xoài chua chọn bạn đừng để bạn chọn xoài chua", 
    "Chuồn chuồn buy thấp thì cao, buy cao thì thấp, buy vừa thì thôi", 
    "Có công mài sắc có ngày nên xà beng"
]

#gọi hàm tạo chunks từ danh sách văn bản và tên file nguồn.
chunks = create_chunks(
    chunk_texts,
    "ai.md"
)

#duyệt và in ra thông tin từng chunk.
for chunk in chunks:
    print(chunk)

