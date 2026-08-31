import sys
from pathlib import Path

#cấu hình in tiếng Việt trên console Windows
sys.stdout.reconfigure(encoding='utf-8')

#thêm thư mục gốc vào sys.path để import được qa_builder
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from qa_builder.filter import filter_qa

#tập dữ liệu test gồm 4 trường hợp đặc biệt:
# 1 & 2: Ngược nghĩa nhau (1 câu CÓ "không", 1 câu KHÔNG có) -> Cần GIỮ LẠI CẢ HAI
# 2 & 3: Cùng nghĩa hoàn toàn (chỉ khác cách diễn đạt) -> Cần LOẠI BỎ BỚT 1 CÂU
# 4: Khác chủ đề hoàn toàn -> Cần GIỮ LẠI
test_cases = [
    {
        "question": "Thuật toán BFS không tìm được đường đi ngắn nhất trên đồ thị có trọng số âm?",
        "answer": "Đúng, BFS không hỗ trợ trọng số âm."
    },
    {
        "question": "Thuật toán BFS tìm được đường đi ngắn nhất trên đồ thị có trọng số âm?",
        "answer": "Sai, BFS chỉ áp dụng cho trọng số bằng nhau."
    },
    {
        "question": "BFS có thể tìm đường đi ngắn nhất trên đồ thị có trọng số âm hay không?",
        "answer": "Không thể, BFS không hoạt động với trọng số âm."
    },
    {
        "question": "Thuật toán DFS hoạt động theo nguyên lý nào?",
        "answer": "DFS duyệt theo chiều sâu sử dụng ngăn xếp."
    }
]

print("=" * 60)
print(f"Tổng số câu hỏi đầu vào: {len(test_cases)} câu")
print("=" * 60)

#chạy qua bộ lọc Hybrid
results = filter_qa(test_cases, duplicate_threshold=0.85)

print(f"\n=> Tổng số câu hỏi sau khi lọc Hybrid: {len(results)} câu\n")
for i, qa in enumerate(results, start=1):
    print(f"[{i}] {qa['question']}")
    print(f"    Đáp án: {qa['answer']}\n")
