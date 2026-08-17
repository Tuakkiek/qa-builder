import re
from pathlib import Path

def is_heading(line: str) -> bool: 
    return bool(re.match(r"^\s{0,3}#{1,6}(\s|$)", line))

def clean_paragraph(text: str) -> str: 
    lines = text.splitlines(text) # tách 1 chuỗi (text) thành (list) các dòng lẻ 
    clean_lines = []

    for line in lines: 
        line = line.strip() 

        if line: 
            clean_lines.append(line)

    return " ".join(clean_lines) # join cách nhau bởi dấu cách  

def extract_md(filepath: str) -> list[str]:
    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()

    lines = text.splitlines()
    content_lines = []

    for line in lines:
        if is_heading(line):
            continue
        content_lines.append(line)

    text_without_headings = "\n".join(content_lines).strip()
    raw_paragraphs = re.split(r"\n\s*\n+", text_without_headings)

    paragraphs = []
    for raw_paragraph in raw_paragraphs:
        paragraph = clean_paragraph(raw_paragraph) 

        if paragraph:
            paragraphs.append(paragraph)

    return paragraphs


if __name__ == "__main__":

    filepath = Path("sample.md")

    paragraphs = extract_md(filepath)

    for index, paragraph in enumerate(paragraphs, start=1):
        print(f"Paragraph {index}: {paragraph}")
