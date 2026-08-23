import os 
import json

from dotenv import load_dotenv 
from google import genai 

load_dotenv() 

api_key = os.getenv("GEMINI_API_KEY")

if not api_key: 
    raise ValueError("Not found api_key")

client = genai.Client(api_key = api_key) 

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
    """ + text, 
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    data = json.loads(response.text)

    return data

text = """
Python là một ngôn ngữ lập trình cấp cao.
Python có cú pháp dễ đọc.
Python được sử dụng trong phát triển web, trí tuệ nhân tạo và phân tích dữ liệu.
"""

result = generate_qa(text)

print(result)
