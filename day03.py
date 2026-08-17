import re


def extract_md(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()

    lines = text.splitlines()
    content_lines = []

    for line in lines:
        if re.match(r"^\s{0,3}#{1,6}(\s|$)", line):
            continue
        content_lines.append(line)

    text_without_headings = "\n".join(content_lines).strip()
    raw_paragraphs = re.split(r"\n\s*\n+", text_without_headings)

    paragraphs = []
    for raw_paragraph in raw_paragraphs:
        paragraph = " ".join(
            line.strip()
            for line in raw_paragraph.splitlines()
            if line.strip()
        )
        if paragraph:
            paragraphs.append(paragraph)

    return paragraphs


if __name__ == "__main__":
    paragraphs = extract_md("sample.md")

    for index, paragraph in enumerate(paragraphs, start=1):
        print(f"Paragraph {index}: {paragraph}")
