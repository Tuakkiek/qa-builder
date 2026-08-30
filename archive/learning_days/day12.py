import os

from dotenv import load_dotenv
from google import genai
from dataclasses import dataclass

@dataclass 
class Chunk: 
    chunk_id: str
    text: str 
    source_file: str 
    word_count: int 

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Không tìm thấy GEMINI_API_KEY")


client = genai.Client(api_key=api_key)


def generate_qa(text: str) -> str:
    prompt = f"""
        Dựa vào nội dung dưới đây, hãy tạo 3 câu hỏi và câu trả lời.
        - Chỉ sử dụng thông tin có trong nội dung.
        - Câu hỏi phải rõ ràng.
        Nội dung:
        {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response

chunk1 = Chunk( 
    chunk_id = "ai_chunk0001", 
    text = """
        Machine Learing là một nhánh của trí tuệ nhân tạo. 
        Machine Learning cho phép máy tính học từ dữ liệu. 
        Mô hình có thể tìm ra các mẫu trong dữ liệu và sử dụng chúng để đưa ra dự đoán.
    """,
    source_file = "ai.md", 
    word_count=35 
)

chunk2 = Chunk( 
    chunk_id = "algo_chunk0002", 
    text = """
        Thuật toán BFS (Breadth-First Search) là thuật toán tìm kiếm theo chiều rộng trên đồ thị hoặc cây. 
        BFS duyệt qua tất cả các đỉnh lân cận ở cùng một mức độ sâu trước khi đi xuống mức sâu hơn. 
        Thuật toán này thường sử dụng cấu trúc dữ liệu hàng đợi (Queue - FIFO) để quản lý các đỉnh cần duyệt. 
        BFS thường được ứng dụng để tìm đường đi ngắn nhất trên đồ thị không có trọng số.
    """,
    source_file = "algorithms.md",
    word_count = 65
)

chunks = [chunk1, chunk2]

for chunk in chunks: 
    print(chunk.chunk_id)

    result = generate_qa(chunk.text) 

    print(result.text)