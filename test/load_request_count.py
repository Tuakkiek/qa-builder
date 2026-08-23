from pathlib import Path
import json


REQUEST_COUNT_FILE = Path("logs/request_count.json")

def load_request_count() -> int: 
    if not REQUEST_COUNT_FILE.exists(): 
        return 0 
    with open(
        REQUEST_COUNT_FILE, 
        "r", 
        encoding = "utf-8"
    ) as file: 
        data = json.load(file) 
    
    return data.get("request_count", 0)
    
print(load_request_count())

