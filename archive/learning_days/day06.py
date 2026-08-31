#import hàm extract_md từ file day05.
from day05 import extract_md

#def hàm dùng để đếm số từ.
def count_words(text: str) -> int:
    return len(text.split())

#gọi hàm extract_md để xử lý file.
units = extract_md("data/giao-trinh-ttnt.md")

#in kết quả ra màn hình
#duyệt qua từng unit (đoạn văn) đã trích xuất
for unit in units:
    print("Section:", unit.section_title)
    print("Text:", unit.text)
    print("Words:", count_words(unit.text))
    print("-" * 50)