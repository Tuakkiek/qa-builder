from dataclasses import dataclass 

@dataclass 
class TextUnit: 
    text: str
    source_file: str
    section_title: str | None = None 