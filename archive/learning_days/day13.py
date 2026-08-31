#import thư viện os để tương tác với hệ thống.
import os 
#import thư viện json để xử lý dữ liệu định dạng json.
import json

#import hàm đọc cấu hình từ file .env.
from dotenv import load_dotenv 
#import thư viện kết nối api gemini.
from google import genai 


#tải các biến môi trường từ file .env lên hệ thống.
load_dotenv() 

#lấy api key từ hệ thống.
api_key = os.getenv("GEMINI_API_KEY")

#kiểm tra nếu ko có key -> quăng lỗi dừng chương trình.
if not api_key: 
    raise ValueError("Not found api_key")

#khởi tạo client kết nối bằng api key.
client = genai.Client(api_key = api_key) 


#def hàm tự động tạo q&a và chuyển đổi kết quả thành object python.
def generate_qa(text: str) -> dict: # (đã sửa type hint thành dict cho chuẩn)
    #tạo prompt ép model phải trả về đúng cấu trúc json, ko bọc trong markdown.
    prompt = """
        Dựa vào nội dung dưới đây, hãy tạo 3 câu hỏi và câu trả lời.
        Yêu cầu:
        - Chỉ sử dụng thông tin trong nội dung.
        - Không tự thêm kiến thức bên ngoài.
        - Câu hỏi phải rõ ràng.
        - Câu trả lời phải chính xác.
        - Chỉ trả về JSON.
        - Không giải thích thêm.
        - Không dùng Markdown code block.
        JSON phải có đúng cấu trúc:
        {
            "qa_pairs": [
                {
                    "question": "...",
                    "answer": "..."
                }
            ]
        }
        Nội dung:
    """ + text

    #gọi model xử lý prompt
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    #chuyển chuỗi json trả về thành kiểu dictionary (dict) của python để dễ dùng.
    data = json.loads(response.text)

    #trả về object dict.
    return data


#tạo đoạn text mẫu về python
text = """
Python là một ngôn ngữ lập trình cấp cao.
Python có cú pháp dễ đọc.
Python được sử dụng trong phát triển web, trí tuệ nhân tạo và phân tích dữ liệu.
"""

#gọi hàm tạo q&a dựa trên text mẫu
result = generate_qa(text)

#in ra kết quả (lúc này nó là 1 dict hoàn chỉnh của python).
print(result)