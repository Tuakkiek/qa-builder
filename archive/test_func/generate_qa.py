#import thư viện os để tương tác với hệ thống.
import os 

#import hàm load_dotenv đọc file .env.
from dotenv import load_dotenv 
#import thư viện kết nối api gemini.
from google import genai 

#tải cấu hình các biến môi trường từ file .env.
load_dotenv()

#lấy api key từ biến môi trường.
api_key = os.getenv("GEMINI_API_KEY")

#kiểm tra api key, nếu không có -> quăng lỗi dừng chương trình.
if not api_key: 
    raise ValueError("Not found api_key")

#khởi tạo client kết nối api gemini.
client = genai.Client(api_key = api_key)

#def hàm gọi api gemini để sinh câu trả lời cho đoạn văn bản đầu vào.
def generate_qa(text: str) -> str: 
    #gọi model gemini-2.5-flash xử lý nội dung.
    response = client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = text
    )

    #trả về đối tượng response nhận được.
    return response

#gọi thử hàm với câu hỏi mẫu "BFS là gì?".
result = generate_qa("BFS là gì?")

#in ra kết quả trả về từ api.
print(result)