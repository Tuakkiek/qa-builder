#thư viện re dùng xử lý chuỗi.
import re
# def hàm dùng để xử lý file md.
def extract_md(filepath):
    #mở file và đọc file.
    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()
    #tách dòng
    lines = text.splitlines()
    #tạo 1 list rỗng để chứa nội dung (sau khi đã lọc tiêu đề)
    content_lines = []

#Loại bỏ các dòng tiêu đề (Headings):
    #duyệt qua từng dòng
    for line in lines:
        #nhận diện tiêu đề
        if re.match(r"^\s{0,3}#{1,6}(\s|$)", line):
            #bỏ qua dòng tiêu đề
            continue
        #nếu ko -> thêm vào danh sách content_lines.
        content_lines.append(line)

#Tách thành các đoạn văn bản:
    #nối các dòng văn bản (đã bỏ heading) lại với nhau
    text_without_headings = "\n".join(content_lines).strip()
    #Tách đoạn tại nơi có dấu hiệu chuyển đoạn
    raw_paragraphs = re.split(r"\n\s*\n+", text_without_headings)

#Dọn dẹp và gộp dòng
    #tạo một list rỗng chứa thành phẩm
    paragraphs = []
    #duyệt qua từng dòng bên trong đoạn
    for raw_paragraph in raw_paragraphs:
        #kỹ thuật làm sạch nội dung: nối các dòng (đã cắt) lại với nhau bằng 1 khoảng trắng.
        paragraph = " ".join(
            #xóa khoảng trắng 2 lề trái phải
            line.strip()
            #cắt đoạn thành dòng nhỏ
            for line in raw_paragraph.splitlines()
            #xóa dòng hoàn toàn trắng
            if line.strip()
        )
        #nếu paragraph có chữ thì thêm vào list paragraphs
        if paragraph:
            paragraphs.append(paragraph)

    return paragraphs

#Code bên dưới chỉ chạy khi file này được gọi trực tiếp (ko phải khi import từ file khác)
if __name__ == "__main__":
    #gọi hàm extract_md để xử lý file sample.md
    paragraphs = extract_md("sample.md")

    #in ra màn hình các đoạn đã xử lý
    for index, paragraph in enumerate(paragraphs, start=1):
        print(f"Paragraph {index}: {paragraph}")
