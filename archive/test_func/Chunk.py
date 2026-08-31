#import dataclass để tự động tạo các hàm khởi tạo __init__, __repr__ cho class dữ liệu.
from dataclasses import dataclass

#khai báo dataclass Chunk đại diện cho một đoạn văn bản sau khi chia nhỏ.
@dataclass
class Chunk:
    #id định danh duy nhất cho chunk.
    chunk_id: str
    #nội dung văn bản của chunk.
    text: str
    #tên hoặc đường dẫn file nguồn chứa đoạn văn bản này.
    source_file: str
    #tổng số từ có trong chunk.
    word_count: int