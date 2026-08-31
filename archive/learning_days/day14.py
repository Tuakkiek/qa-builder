#import thư viện os để tương tác với hệ thống.
import os
#import thư viện json để xử lý dữ liệu.
import json
#import class JSONDecodeError để bắt lỗi khi phân tích chuỗi json.
from json import JSONDecodeError

#import hàm load_dotenv để đọc file .env.
from dotenv import load_dotenv
#import thư viện kết nối api gemini.
from google import genai


#tải các cấu hình từ file .env lên.
load_dotenv()

#lấy api key từ hệ thống.
api_key = os.getenv("GEMINI_API_KEY")

#kiểm tra nếu ko có key -> quăng lỗi dừng chương trình.
if not api_key:
    raise ValueError("Không tìm thấy GEMINI_API_KEY")


#khởi tạo client kết nối bằng api key.
client = genai.Client(api_key=api_key)


#def hàm tự tạo q&a và xử lý lỗi (type hint ở đây nên đổi thành list thay vì str nha).
def generate_qa(text: str) -> str:
    #tạo prompt ép model trả về đúng cấu trúc json.
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

    #dùng try-except để bắt lỗi nếu api trả về kết quả ko như ý.
    try:
        #gọi model gemini-2.5-flash xử lý prompt.
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        #chuyển kết quả text thành dictionary của python.
        data = json.loads(response.text)

        #lấy và trả về riêng list chứa các cặp câu hỏi - câu trả lời.
        return data["qa_pairs"]

    #nếu chuỗi trả về ko phải json chuẩn -> báo lỗi và trả về list rỗng.
    except JSONDecodeError:
        print("Lỗi: Gemini trả JSON không hợp lệ")
        return []

    #nếu json hợp lệ nhưng lại ko có key "qa_pairs" -> báo lỗi và trả về list rỗng.
    except KeyError:
        print("Lỗi: Không tìm thấy qa_pairs trong JSON")
        return []

    #bắt tất cả các lỗi bất ngờ khác (như rớt mạng, lỗi server...).
    except Exception as error:
        print("Lỗi khi gọi Gemini:", error)
        return []


#tạo đoạn text mẫu về machine learning.
text = """
Machine Learning là một nhánh của trí tuệ nhân tạo.
Machine Learning cho phép máy tính học từ dữ liệu.
Mô hình có thể tìm ra các mẫu trong dữ liệu và sử dụng chúng để đưa ra dự đoán.
"""


#gọi hàm tạo q&a, biến qa_pairs lúc này sẽ là 1 list.
qa_pairs = generate_qa(text)


#duyệt qua từng cặp q&a trong list để in ra.
for qa in qa_pairs:
    #in câu hỏi.
    print("Câu hỏi:", qa["question"])
    #in câu trả lời.
    print("Trả lời:", qa["answer"])
    #in dòng trống để phân cách cho dễ nhìn.
    print()