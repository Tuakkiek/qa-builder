import os
import json
from json import JSONDecodeError

from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Không tìm thấy GEMINI_API_KEY")


client = genai.Client(api_key=api_key)


def generate_qa(text: str) -> str:
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

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        data = json.loads(response.text)

        return data["qa_pairs"]

    except JSONDecodeError:
        print("Lỗi: Gemini trả JSON không hợp lệ")
        return []

    except KeyError:
        print("Lỗi: Không tìm thấy qa_pairs trong JSON")
        return []

    except Exception as error:
        print("Lỗi khi gọi Gemini:", error)
        return []


text = """
Machine Learning là một nhánh của trí tuệ nhân tạo.
Machine Learning cho phép máy tính học từ dữ liệu.
Mô hình có thể tìm ra các mẫu trong dữ liệu và sử dụng chúng để đưa ra dự đoán.
"""


qa_pairs = generate_qa(text)


for qa in qa_pairs:
    print("Câu hỏi:", qa["question"])
    print("Trả lời:", qa["answer"])
    print()