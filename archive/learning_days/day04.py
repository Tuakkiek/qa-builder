#thư viện re dùng xử lý chuỗi.
import re
#import hàm Path để xử lý đường dẫn file.
from pathlib import Path

#def hàm kiểm tra dòng có phải là tiêu đề ko.
def is_heading(line: str) -> bool: 
    return bool(re.match(r"^\s{0,3}#{1,6}(\s|$)", line))

#def hàm dọn dẹp và gộp các dòng lẻ thành 1 đoạn
def clean_paragraph(text: str) -> str: 
    # tách 1 chuỗi (text) thành (list) các dòng lẻ 
    lines = text.splitlines(text) 
    #tạo list rỗng để chứa các dòng đã làm sạch.
    clean_lines = []

    #duyệt qua từng dòng.
    for line in lines:
        #xóa khoảng trắng 2 lề trái phải. 
        line = line.strip() 

        #nếu dòng ko trắng -> thêm vào clean_lines.
        if line: 
            clean_lines.append(line)

    #join cách nhau bởi dấu cách.
    return " ".join(clean_lines) 

#def hàm chính xử lý file .md (tách file md thành list paragraphs)
def extract_md(filepath: str) -> list[str]:
    #mở file và đọc file.
    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()

    #tách dòng.
    lines = text.splitlines()
    #tạo 1 list rỗng để chứa nội dung (sau khi đã lọc tiêu đề).
    content_lines = []

    #Loại bỏ các dòng tiêu đề (Headings):
    for line in lines:
        #gọi hàm kiểm tra tiêu đề.
        if is_heading(line):
            #bỏ qua dòng là tiêu đề
            continue
        #nếu ko -> thêm vào danh sách content_lines.
        content_lines.append(line)

#Tách thành các đoạn văn bản:
    #nối các dòng văn bản (đã bỏ heading) lại với nhau.
    text_without_headings = "\n".join(content_lines).strip()
    #tách đoạn tại nơi có dấu hiệu chuyển đoạn
    raw_paragraphs = re.split(r"\n\s*\n+", text_without_headings)

#Dọn dẹp và gộp dòng
    #tạo một list rỗng chứa thành phẩm
    paragraphs = []
    #duyệt qua từng đoạn thô
    for raw_paragraph in raw_paragraphs:
        #gọi hàm để làm sạch đoạn
        paragraph = clean_paragraph(raw_paragraph) 

        #nếu paragraph có chữ thì thêm vào list paragraphs
        if paragraph:
            paragraphs.append(paragraph)

    return paragraphs

#Code bên dưới chỉ chạy khi file này được gọi trực tiếp.
if __name__ == "__main__":
    #khai báo đường dẫn
    filepath = Path("sample.md")

    #gọi hàm extract_md để xử lý file
    paragraphs = extract_md(filepath)

    #in ra màn hình
    for index, paragraph in enumerate(paragraphs, start=1):
        print(f"Paragraph {index}: {paragraph}")
