import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TextUnit:
    text: str
    source_file: str
    section_title: str | None = None


def is_heading(line: str) -> bool:
    return bool(re.match(r"^\s{0,3}#{1,6}(\s|$)", line))


def get_heading_title(line: str) -> str:
    return re.sub(r"^\s{0,3}#{1,6}\s*", "", line).strip()


def clean_paragraph(text: str) -> str:
    return " ".join(
        line.strip()
        for line in text.splitlines()
        if line.strip()
    )


def extract_md(filepath: str) -> list[TextUnit]:
    path = Path(filepath)

    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    lines = text.splitlines()

    units: list[TextUnit] = []

    current_section: str | None = None
    paragraph_lines: list[str] = []

    def save_paragraph():
        if not paragraph_lines:
            return

        paragraph = clean_paragraph("\n".join(paragraph_lines))

        if paragraph:
            units.append(
                TextUnit(
                    text=paragraph,
                    source_file=path.name,
                    section_title=current_section
                )
            )

        paragraph_lines.clear()

    for line in lines:

        if is_heading(line):

            save_paragraph()

            current_section = get_heading_title(line)

            continue

        if not line.strip():

            save_paragraph()

            continue

        paragraph_lines.append(line)

    save_paragraph()

    return units


if __name__ == "__main__":
    units = extract_md("data/sample.md")

    for unit in units:
        print("Text:", unit.text)
        print("Source:", unit.source_file)
        print("Section:", unit.section_title)
        print("-" * 50)