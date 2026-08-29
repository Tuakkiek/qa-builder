import json 

def read_jsonl(filepath: str)-> dict:
    with open(filepath, "r", encoding="utf-8") as f: 
        for line in f:
            item = json.loads(line)
            print(item)

read_jsonl("data_test/students.jsonl")
         
