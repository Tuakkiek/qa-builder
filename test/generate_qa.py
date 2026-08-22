import os 

from dotenv import load_dotenv 
from google import genai 

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key: 
    raise ValueError("Not found api_key")

client = genai.Client(api_key = api_key)

def generate_qa(text: str) -> str: 
    response = client.models.generate_content(
        model = "gemini-2.5-flash", 
        contents = text
    )

    return response

result = generate_qa("BFS là gì?")

print(result)