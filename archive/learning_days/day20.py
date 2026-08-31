#import thư viện json để xử lý dữ liệu.
import json 


#def hàm ghi danh sách dữ liệu ra file định dạng jsonl (mỗi dòng là 1 object json).
def write_jsonl( 
    data: list[dict],
    filepath: str 
) -> None: 
    #mở file ở chế độ ghi đè ("w") với bảng mã utf-8 để ko bị lỗi font tiếng Việt.
    with open(filepath, "w", encoding="utf-8") as f: 
        #duyệt qua từng phần tử (object) trong danh sách dữ liệu.
        for item in data: 
            #chuyển object python thành chuỗi json, ensure_ascii=False giúp giữ nguyên dấu tiếng Việt.
            line = json.dumps(item, ensure_ascii=False)

            #ghi chuỗi json vừa tạo vào file, cộng thêm "\n" để ngắt dòng (đây là quy tắc bắt buộc của chuẩn jsonl).
            f.write(line + "\n")
        

#Code test tạo dữ liệu giả.
#tạo list chứa các cặp q&a mẫu.
qa_pairs = [
    {
        "question": "Q1",
        "answer": "A1",
        "chunk_id": "chunk_001"
    },
    {
        "question": "Q2",
        "answer": "A2",
        "chunk_id": "chunk_001"
    }
]


#gọi hàm để ghi list qa_pairs ra file qa.jsonl (lưu ý: thư mục JSONL phải được tạo sẵn trước thì code mới ko báo lỗi).
write_jsonl(qa_pairs, "JSONL/qa.jsonl")