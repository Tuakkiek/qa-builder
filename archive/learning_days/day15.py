#import thư viện os để tương tác hệ thống.
import os
#import thư viện json xử lý dữ liệu.
import json
#import thư viện time để dùng hàm chờ (sleep).
import time

#import class bắt lỗi parse json.
from json import JSONDecodeError
#import Path để xử lý đường dẫn file/thư mục.
from pathlib import Path

#import hàm load_dotenv đọc file .env.
from dotenv import load_dotenv
#import thư viện kết nối api gemini.
from google import genai


#tải cấu hình từ file .env lên.
load_dotenv()

#lấy api key.
api_key = os.getenv("GEMINI_API_KEY")

#kiểm tra api key, ko có -> quăng lỗi.
if not api_key:
    raise ValueError("Không tìm thấy GEMINI_API_KEY")


#khởi tạo client kết nối api.
client = genai.Client(api_key=api_key)


#khai báo hằng số lưu đường dẫn tới file ghi log số lượng request.
REQUEST_COUNT_FILE = Path("logs/request_count.json")


#def hàm đọc tổng số request đã lưu từ file.
def load_request_count() -> int:
    #nếu file chưa tồn tại -> trả về 0.
    if not REQUEST_COUNT_FILE.exists():
        return 0

    #mở file ở chế độ đọc ("r").
    with open(
        REQUEST_COUNT_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        #đọc nội dung file chuyển thành biến dict.
        data = json.load(file)

    #trả về giá trị của key "request_count", nếu ko tìm thấy thì mặc định là 0.
    return data.get("request_count", 0)


#def hàm lưu số lượng request mới cập nhật xuống file.
def save_request_count(count: int) -> None:
    #tạo thư mục cha (thư mục logs) nếu chưa có, exist_ok=True để ko báo lỗi nếu đã tạo rồi.
    REQUEST_COUNT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    #mở file ở chế độ ghi đè ("w").
    with open(
        REQUEST_COUNT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        #ghi dict chứa số count vào file định dạng json.
        json.dump(
            #tạo dict chứa số đếm
            {"request_count": count},
            file,
            #giữ nguyên dấu tiếng Việt (ko biến thành mã ascii).
            ensure_ascii=False,
            #thêm khoảng trắng 4 lề cho file json dễ đọc.
            indent=4
        )


#khởi tạo biến đếm toàn cục bằng cách gọi hàm đọc file lúc bắt đầu chạy code.
request_count = load_request_count()


#def hàm gọi api có tích hợp cơ chế tự động thử lại (retry) khi bị lỗi mạng/server.
def call_with_retry(
    prompt: str,
    max_retries: int = 3 #giới hạn số lần thử tối đa.
):
    #khai báo sử dụng biến request_count toàn cục (đã khai báo ở ngoài hàm).
    global request_count

    #vòng lặp thử gọi api theo số max_retries.
    for attempt in range(max_retries):
        try:
            #tăng biến đếm lên 1 mỗi khi bắt đầu gửi request mới.
            request_count += 1
            #lưu ngay số đếm vừa tăng xuống file json.
            save_request_count(request_count)

            #gọi model gemini xử lý prompt.
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            #nếu thành công -> trả về kết quả luôn (thoát khỏi hàm).
            return response

        #bắt lỗi nếu gọi api thất bại.
        except Exception as error:
            print(f"Lỗi API: {error}")

            #nếu đã thử đến lần cuối cùng (attempt chạy từ 0) -> thoát vòng lặp.
            if attempt == max_retries - 1:
                break

            #tính thời gian chờ (delay) tăng dần theo cấp số nhân (2^0=1s, 2^1=2s...).
            delay = 2 ** attempt

            print(
                f"Thử lại sau {delay} giây..."
            )

            #tạm dừng chương trình vài giây trước khi vòng lặp qua lần thử tiếp theo.
            time.sleep(delay)

    #nếu thử hết số lần vẫn xịt -> trả về None.
    return None


#def hàm tạo q&a trả về list các dictionary.
def generate_qa(text: str) -> list[dict]:
    #tạo chuỗi prompt.
    prompt = """
        Dựa vào nội dung dưới đây, hãy tạo 3 câu hỏi
        và câu trả lời.
        
        Yêu cầu:
        - Chỉ sử dụng thông tin trong nội dung.
        - Không tự thêm kiến thức bên ngoài.
        - Chỉ trả về JSON hợp lệ.
        - Không dùng Markdown code block.
        - Không giải thích thêm.
        
        JSON:
        
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

    #gọi api thông qua hàm retry vừa tạo ở trên.
    response = call_with_retry(prompt)

    #nếu kết quả là None (gọi thất bại toàn tập) -> báo lỗi, trả về list rỗng.
    if response is None:
        print("Không thể gọi Gemini sau nhiều lần thử")
        return []

    #dùng try-except xử lý chuỗi json api trả về.
    try:
        #chuyển string json thành dict python.
        data = json.loads(response.text)

        #trả về list cặp q&a.
        return data["qa_pairs"]

    #lỗi ko parse được json.
    except JSONDecodeError:
        print("Gemini trả JSON không hợp lệ")
        return []

    #lỗi json chuẩn nhưng ko có key qa_pairs.
    except KeyError:
        print("Không tìm thấy qa_pairs")
        return []


#tạo đoạn text mẫu để test.
text = """
Machine Learning là một nhánh của trí tuệ nhân tạo.
Machine Learning cho phép máy tính học từ dữ liệu.
Mô hình có thể tìm ra các mẫu trong dữ liệu và
sử dụng chúng để đưa ra dự đoán.
"""


#gọi hàm tạo q&a.
qa_pairs = generate_qa(text)


#duyệt list q&a để in ra màn hình.
for qa in qa_pairs:
    print("Câu hỏi:", qa["question"])
    print("Trả lời:", qa["answer"])
    print()


#in tổng số lần đã request api (cộng dồn từ các lần chạy trước nhờ đọc/ghi file).
print("Tổng số request:", request_count)