import re
#import dataclass để tạo class lưu trữ dữ liệu nhanh.
from dataclasses import dataclass
from pathlib import Path

#tạo class TextUnit lưu nội dung, tên file và tên mục (section).
@dataclass
class TextUnit:
    text: str
    source_file: str
    section_title: str | None = None

#def hàm kiểm tra xem dòng có phải là tiêu đề (heading) ko.
def is_heading(line: str) -> bool:
    return bool(re.match(r"^\s{0,3}#{1,6}(\s|$)", line))

#def hàm lấy nội dung chữ của tiêu đề (xóa các dấu # đi).
def get_heading_title(line: str) -> str:
    return re.sub(r"^\s{0,3}#{1,6}\s*", "", line).strip()

#def hàm dọn dẹp và gộp các dòng lẻ thành 1 đoạn.
def clean_paragraph(text: str) -> str:
    return " ".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )

#def hàm chính dùng để xử lý và trích xuất dữ liệu từ file md.
def extract_md(filepath: str) -> list[TextUnit]:
    #chuyển string thành đối tượng Path để tiện xử lý.
    path = Path(filepath)

    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    lines = text.splitlines()

    #tạo list rỗng chứa các object TextUnit.
    units: list[TextUnit] = []

    #biến lưu tên mục (heading) hiện tại.
    current_section: str | None = None
    #list tạm để gom các dòng liền kề nhau thành 1 đoạn.
    paragraph_lines: list[str] = []

    #hàm lưu lại paragraph (nếu có).
    def save_paragraph():
        #nếu list tạm đang rỗng thì ko làm gì cả
        if not paragraph_lines:
            return

        paragraph = clean_paragraph("\n".join(paragraph_lines))

        if paragraph:
            #tạo object TextUnit và đưa vào list
            units.append(
                TextUnit(
                    text=paragraph, #chỉ lấy nội dung chữ
                    source_file=path.name, #chỉ lấy tên file gốc
                    section_title=current_section #chỉ lấy tên mục
                )
            )

        #xóa sạch list tạm để chuẩn bị gom đoạn mới.
        paragraph_lines.clear()

    for line in lines:
        if is_heading(line):
            #gặp heading mới -> chốt và lưu đoạn cũ đang gom dở (nếu có)
            save_paragraph()
            #cập nhật lại tên section hiện tại.
            current_section = get_heading_title(line)
            continue

        #nếu gặp dòng trắng -> chốt paragraph cũ (nếu có)
        if not line.strip():
            save_paragraph()
            continue

        #nếu là dòng chữ bình thường -> gom vào list tạm.
        paragraph_lines.append(line)

    #gọi thêm 1 lần cuối để lưu đoạn văn cuối cùng của file.
    save_paragraph()

    return units

#Code bên dưới chỉ chạy khi file này được gọi trực tiếp.
if __name__ == "__main__":
    #gọi hàm extract_md để xử lý file.
    units = extract_md("data/sample.md")

    #in ra màn hình kết quả.
    for unit in units:
        print("Text:", unit.text)
        print("Source:", unit.source_file)
        print("Section:", unit.section_title)
        print("-" * 50)