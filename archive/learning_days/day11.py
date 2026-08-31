#import thư viện os để tương tác với hệ điều hành.
import os 
#import hàm load_dotenv để đọc các biến cấu hình từ file .env.
from dotenv import load_dotenv 
#import thư viện genai để kết nối với api của google.
from google import genai

#tải các biến môi trường từ file .env lên hệ thống.
load_dotenv() 

#lấy api key
api_key = os.getenv("GEMINI_API_KEY")

#kiểm tra api key có tồn tại ko. nếu ko -> báo lỗi dừng chương trình luôn.
if not api_key: 
    raise ValueError("Not found GEMINI_API_KEY")

#khởi tạo client kết nối với hệ thống gemini bằng api key vừa lấy.
client = genai.Client(api_key = api_key)

#gọi model gemini-2.5-flash để tự động tạo câu trả lời cho Q truyền vào.
respone = client.models.generate_content(
    model = "gemini-2.5-flash", 
    contents = "Machine Learning là gì?"
)

#in phần text của kết quả trả về ra màn hình.
print(respone.text)