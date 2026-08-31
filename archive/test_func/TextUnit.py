#import dataclass để tạo class lưu trữ dữ liệu dạng đơn vị văn bản (unit).
from dataclasses import dataclass
#khai báo dataclass TextUnit đại diện cho một đơn vị văn bản thô được trích xuất từ file.
@dataclass
class TextUnit:
    #nội dung văn bản của unit.
    text: str
    #tên hoặc đường dẫn file nguồn chứa unit này.
    source_file: str
    #tiêu đề mục/chương chứa đoạn văn (nếu có, mặc định là None).
    section_title: str | None = None