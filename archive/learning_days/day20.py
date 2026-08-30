import json 

def write_jsonl( 
    data: list[dict],
    filepath: str 
) -> None: 
    with open(filepath, "w", encoding="utf-8") as f: 
        for item in data: 
            line = json.dumps(item, ensure_ascii=False)

            f.write(line + "\n")
        
qa_pairs = [
    {
        "question": "Q1",
        "answer": "A1",
        "chunk_id": "chunk_001"
    },
    {
        "question": "Q2",
        "answer": "A2",
        "chunk_id": "chunk_001"
    }
]

write_jsonl(qa_pairs, "JSONL/qa.jsonl")

