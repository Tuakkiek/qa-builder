import os 
from dotenv import load_dotenv 
from google import genai

load_dotenv() 

api_key = os.getenv("GEMINI_API_KEY")

if not api_key: 
    raise ValueError("Not found GEMINI_API_KEY")

client = genai.Client(api_key = api_key)

respone = client.models.generate_content(
    model = "gemini-2.5-flash", 
    contents = "Machine Learning là gì?"
)

print(respone.text)