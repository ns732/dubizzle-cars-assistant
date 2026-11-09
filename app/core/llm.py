
import os

from dotenv import load_dotenv
from litellm import completion


load_dotenv()

MODEL = "gemini/gemini-3.8-flash"


def ask_gemini(message: str) -> str:
    response = completion(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": message
            }
        ],
        num_retries=3,
        timeout=45,
        reasoning_effort="low"
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError("GEMINI_API_KEY is missing from .env")

    print("Testing Gemini connection...")

    answer = ask_gemini(
        "Reply with exactly: Gemini connection successful."
    )

    print(answer)
