#import thư viện json để xử lý chuyển đổi object sang chuỗi JSON.
import json 
#def hàm ghi danh sách dữ liệu ra file định dạng JSONL (mỗi phần tử là 1 dòng JSON).
def write_jsonl(data, filepath): 
    #mở file ở chế độ ghi ("w") với bảng mã UTF-8.
    with open(filepath, "w", encoding="utf-8") as f: 
        #lặp qua từng item (dictionary) trong danh sách dữ liệu.
        for item in data: 
            #chuyển dictionary thành chuỗi JSON, giữ nguyên tiếng Việt không bị mã hóa (ensure_ascii=False).
            json_line = json.dumps(item, ensure_ascii=False)
            #ghi chuỗi json kèm ký tự xuống dòng vào file.
            f.write(json_line + "\n")
#tạo danh sách sinh viên mẫu.
students = [
    {"name": "An", "age": 20, "score": 8.5},
    {"name": "Bình", "age": 21, "score": 9.0},
    {"name": "Chi", "age": 19, "score": 7.8},
]
#gọi hàm ghi danh sách sinh viên vào file JSONL trong thư mục data_test.
write_jsonl(students, "data_test/students.jsonl")
#tạo dictionary mẫu cho 1 cặp Q&A.
item = {
    "question": "Q1",
    "answer": "A1"
}
#in ra kiểu dữ liệu gốc của item (dict).
print(type(item))