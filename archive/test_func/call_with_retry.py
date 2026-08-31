#import thư viện time để dùng hàm chờ (sleep).
import time 
#import thư viện os để tương tác hệ thống (tui thêm vào để dùng được os.getenv nha).
import os
#import thư viện kết nối api gemini.
from google import genai 
#import hàm load_dotenv để đọc cấu hình từ file .env.
from dotenv import load_dotenv

#tải các biến môi trường từ file .env lên hệ thống.
load_dotenv()

#lấy api key từ hệ thống.
api_key = os.getenv("GEMINI_API_KEY")

#khởi tạo client kết nối api (tui đã sửa `Client` thành `genai.Client` cho đúng thư viện).
client = genai.Client(api_key = api_key)

#def hàm gọi api có tích hợp cơ chế tự động thử lại (retry) khi bị lỗi.
def call_with_retry(prompt: str, max_retries: int = 3): 
    #vòng lặp thử gọi api theo giới hạn số lần (max_retries).
    for attempt in range(max_retries): 
        #dùng try-except để bắt lỗi an toàn.
        try: 
            #gọi model gemini-2.5-flash xử lý prompt.
            response = client.models.generate_content(
                model = "gemini-2.5-flash", 
                contents = prompt
            )

            #nếu thành công -> trả về kết quả luôn (tui đã sửa lỗi gõ nhầm `respone` thành `response`).
            return response

        #bắt lỗi nếu gọi api thất bại.
        except Exception as error: 
            #in thông báo lỗi ra màn hình.
            print("Lỗi API: ", error)

            #nếu đã thử đến lần cuối cùng -> thoát vòng lặp (tui đã sửa `max_tries` thành `max_retries`).
            if attempt == max_retries - 1: 
                break

            #tính thời gian chờ tăng dần theo cấp số nhân (2^0=1s, 2^1=2s, 2^2=4s...).
            delay = 2 ** attempt

            #in thông báo thời gian chờ.
            print(f"Thử lại sau {delay} giây ")

            #tạm dừng chương trình trước khi thử lại (tui đã sửa `deplay` thành `delay`).
            time.sleep(delay) 

    #nếu thử hết số lần vẫn xịt -> trả về None.
    return None