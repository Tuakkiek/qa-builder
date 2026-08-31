import os
from dotenv import load_dotenv
from google import genai
#import dataclass để tạo class lưu trữ dữ liệu nhanh.
from dataclasses import dataclass


#tạo class Chunk lưu thông tin của đoạn văn bản đã cắt.
@dataclass 
class Chunk: 
    #mã định danh chunk.
    chunk_id: str
    #nội dung văn bản.
    text: str 
    #tên file gốc.
    source_file: str 
    #số từ trong chunk.
    word_count: int 


#tải các cấu hình từ file .env lên hệ thống.
load_dotenv()

#lấy api key từ biến môi trường.
api_key = os.getenv("GEMINI_API_KEY")

#kiểm tra nếu ko có api key -> báo lỗi dừng chương trình.
if not api_key:
    raise ValueError("Không tìm thấy GEMINI_API_KEY")


#khởi tạo client kết nối api bằng key vừa lấy.
client = genai.Client(api_key=api_key)


#def hàm tự động tạo câu hỏi và trả lời từ văn bản đầu vào.
def generate_qa(text: str) -> str:
    #tạo câu lệnh (prompt) hướng dẫn ai tạo 3 câu hỏi dựa trên nội dung truyền vào.
    prompt = f"""
        Dựa vào nội dung dưới đây, hãy tạo 3 câu hỏi và câu trả lời.
        - Chỉ sử dụng thông tin có trong nội dung.
        - Câu hỏi phải rõ ràng.
        Nội dung:
        {text}
    """

    #gọi model gemini-2.5-flash để xử lý prompt.
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    #trả về nguyên object response chứa kết quả.
    return response


#tạo object chunk1 chứa kiến thức về machine learning.
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


#tạo object chunk2 chứa kiến thức về thuật toán bfs.
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


#đưa 2 chunk vừa tạo vào một list.
chunks = [chunk1, chunk2]


#duyệt qua từng chunk trong list.
for chunk in chunks: 
    #in ra mã id của chunk hiện tại.
    print(chunk.chunk_id)

    #gọi hàm generate_qa truyền vào nội dung của chunk để tạo q&a.
    result = generate_qa(chunk.text) 

    #in ra màn hình phần văn bản (text) của kết quả trả về.
    print(result.text)