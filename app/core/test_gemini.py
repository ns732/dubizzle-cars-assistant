
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Gemini API key not found.")

client = genai.Client(api_key=api_key)

print("Testing direct Gemini connection...")

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Reply with: Gemini connection successful."
)

print(response.text)
