from pathlib import Path 
from Chunk import Chunk
from count_word import count_words 

def create_chunks(chunk_texts: list[str], source_file: str) -> list[Chunk]:
    
    chunks = []

    file_name = Path(source_file).stem

    for i, text in enumerate(chunk_texts, start=1):

        chunk_id = f"{file_name}_chunk{i:04d}"

        chunk = Chunk(
            chunk_id=chunk_id,
            text=text,
            source_file=source_file,
            word_count=count_words(text)
        )

        chunks.append(chunk)

    return chunks

chunk_texts = [
    "Chọn xoài đừng để xoài chua chọn bạn đừng để bạn chọn xoài chua", 
    "Chuồn chuồn buy thấp thì cao, buy cao thì thấp, buy vừa thì thôi", 
    "Có công mài sắc có ngày nên xà beng"
]

chunks = create_chunks(
    chunk_texts,
    "ai.md"
)


for chunk in chunks:
    print(chunk)

