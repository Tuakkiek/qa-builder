from day05 import extract_md


def count_words(text: str) -> int:
    return len(text.split())


units = extract_md("data/giao-trinh-ttnt.md")

for unit in units:
    print("Section:", unit.section_title)
    print("Text:", unit.text)
    print("Words:", count_words(unit.text))
    print("-" * 50)