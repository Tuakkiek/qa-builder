import time 
from google import genai 
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = Client(api_key = api_key)

def call_with_retry(prompt: str, max_retries: int = 3): 
    for attempt in range(max_retries): 
        try: 
            response = client.models.generate_content(
                model = "gemini-2.5-flash", 
                contents = prompt
            )

            return respone

        except Exception as error: 
            print("Lỗi API: ", error)

            if attempt == max_tries - 1: 
                break

            delay = 2 ** attempt

            print(f"Thử lại sau {delay} giây ")

            time.sleep(deplay) 

    return None

