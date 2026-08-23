import os
import json
import time

from json import JSONDecodeError
from pathlib import Path

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Không tìm thấy GEMINI_API_KEY")


client = genai.Client(api_key=api_key)


REQUEST_COUNT_FILE = Path("logs/request_count.json")


def load_request_count() -> int:
    if not REQUEST_COUNT_FILE.exists():
        return 0

    with open(
        REQUEST_COUNT_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    return data.get("request_count", 0)


def save_request_count(count: int) -> None:
    REQUEST_COUNT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        REQUEST_COUNT_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            {"request_count": count},
            file,
            ensure_ascii=False,
            indent=4
        )


request_count = load_request_count()


def call_with_retry(
    prompt: str,
    max_retries: int = 3
):
    global request_count

    for attempt in range(max_retries):
        try:
            request_count += 1
            save_request_count(request_count)

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response

        except Exception as error:
            print(f"Lỗi API: {error}")

            if attempt == max_retries - 1:
                break

            delay = 2 ** attempt

            print(
                f"Thử lại sau {delay} giây..."
            )

            time.sleep(delay)

    return None


def generate_qa(text: str) -> list[dict]:
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

    response = call_with_retry(prompt)

    if response is None:
        print("Không thể gọi Gemini sau nhiều lần thử")
        return []

    try:
        data = json.loads(response.text)

        return data["qa_pairs"]

    except JSONDecodeError:
        print("Gemini trả JSON không hợp lệ")
        return []

    except KeyError:
        print("Không tìm thấy qa_pairs")
        return []


text = """
Machine Learning là một nhánh của trí tuệ nhân tạo.
Machine Learning cho phép máy tính học từ dữ liệu.
Mô hình có thể tìm ra các mẫu trong dữ liệu và
sử dụng chúng để đưa ra dự đoán.
"""


qa_pairs = generate_qa(text)


for qa in qa_pairs:
    print("Câu hỏi:", qa["question"])
    print("Trả lời:", qa["answer"])
    print()


print("Tổng số request:", request_count)