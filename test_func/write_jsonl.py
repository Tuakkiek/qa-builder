import json 

def write_jsonl(data, filepath): 

    with open(filepath, "w", encoding="utf-8") as f: 
        for item in data: 
            json_line = json.dumps(item, ensure_ascii=False)

            f.write(json_line + "\n")


students = [
    {"name": "An", "age": 20, "score": 8.5},
    {"name": "Bình", "age": 21, "score": 9.0},
    {"name": "Chi", "age": 19, "score": 7.8},
]

write_jsonl(students, "data_test/students.jsonl")

item = {
    "question": "Q1",
    "answer": "A1"
}

print(type(item))

print(type(json.dumps(item)))
