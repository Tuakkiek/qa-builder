import re
from pathlib import Path

from .models import TextUnit


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


def extract_md(filepath: str | Path) -> list[TextUnit]:
    path = Path(filepath)

    if path.suffix.lower() != ".md":
        raise ValueError(f"Chỉ hỗ trợ file .md: {path}")

    with open(path, "r", encoding="utf-8") as file:
        text = file.read()

    units: list[TextUnit] = []
    current_section: str | None = None
    paragraph_lines: list[str] = []

    def save_paragraph() -> None:
        if not paragraph_lines:
            return

        paragraph = clean_paragraph("\n".join(paragraph_lines))

        if paragraph:
            units.append(
                TextUnit(
                    text=paragraph,
                    source_file=path.name,
                    section_title=current_section,
                )
            )

        paragraph_lines.clear()

    for line in text.splitlines():
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
