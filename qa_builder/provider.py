import json
import os
import time
from json import JSONDecodeError
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai

from .models import Chunk


REQUEST_COUNT_FILE = Path("logs/request_count.json")


def load_request_count() -> int:
    if not REQUEST_COUNT_FILE.exists():
        return 0

    with open(REQUEST_COUNT_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("request_count", 0)


def save_request_count(count: int) -> None:
    REQUEST_COUNT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(REQUEST_COUNT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            {"request_count": count},
            file,
            ensure_ascii=False,
            indent=4,
        )


def create_client():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Không tìm thấy GEMINI_API_KEY trong file .env")

    return genai.Client(api_key=api_key)


def call_with_retry(
    prompt: str,
    max_retries: int = 3,
    model: str = "gemini-2.5-flash",
):
    client = create_client()
    request_count = load_request_count()

    for attempt in range(max_retries):
        try:
            request_count += 1
            save_request_count(request_count)

            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )

            return response

        except Exception as error:
            print("Lỗi API:", error)

            if attempt == max_retries - 1:
                break

            delay = 2 ** attempt
            print(f"Thử lại sau {delay} giây...")
            time.sleep(delay)

    return None


def build_prompt(text: str, num_questions: int = 3) -> str:
    return f"""
        Dựa vào nội dung dưới đây, hãy tạo {num_questions} câu hỏi
        và câu trả lời.

        Yêu cầu:
        - Chỉ sử dụng thông tin trong nội dung.
        - Không tự thêm kiến thức bên ngoài.
        - Câu hỏi phải rõ ràng.
        - Câu trả lời phải chính xác.
        - Chỉ trả về JSON hợp lệ.
        - Không dùng Markdown code block.
        - Không giải thích thêm.

        JSON:
        {{
            "qa_pairs": [
                {{
                    "question": "...",
                    "answer": "..."
                }}
            ]
        }}

        Nội dung:
        {text}
    """


def clean_json_text(text: str) -> str:
    text = text.strip()

    if text.startswith("```json"):
        text = text.removeprefix("```json").strip()

    if text.startswith("```"):
        text = text.removeprefix("```").strip()

    if text.endswith("```"):
        text = text.removesuffix("```").strip()

    return text


def normalize_qa_pairs(
    qa_pairs: list[dict[str, Any]],
    chunk: Chunk | None = None,
) -> list[dict]:
    normalized = []

    for qa in qa_pairs:
        question = str(qa.get("question", "")).strip()
        answer = str(qa.get("answer", "")).strip()

        if not question or not answer:
            continue

        item = {
            "question": question,
            "answer": answer,
        }

        if chunk is not None:
            item["chunk_id"] = chunk.chunk_id
            item["source_file"] = chunk.source_file

        normalized.append(item)

    return normalized


def generate_qa(
    chunk_or_text: Chunk | str,
    num_questions: int = 3,
    max_retries: int = 3,
) -> list[dict]:
    chunk = chunk_or_text if isinstance(chunk_or_text, Chunk) else None
    text = chunk_or_text.text if isinstance(chunk_or_text, Chunk) else chunk_or_text
    prompt = build_prompt(text, num_questions=num_questions)
    response = call_with_retry(prompt, max_retries=max_retries)

    if response is None:
        print("Không thể gọi Gemini sau nhiều lần thử")
        return []

    try:
        data = json.loads(clean_json_text(response.text))
        qa_pairs = data["qa_pairs"]

        if not isinstance(qa_pairs, list):
            return []

        return normalize_qa_pairs(qa_pairs, chunk=chunk)

    except JSONDecodeError:
        print("Gemini trả JSON không hợp lệ")
        return []

    except KeyError:
        print("Không tìm thấy qa_pairs trong JSON")
        return []
