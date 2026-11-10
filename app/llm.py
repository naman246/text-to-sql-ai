import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing from .env")


client = Groq(api_key=api_key)


def ask_llm(prompt: str) -> str:
    """Send a prompt to Groq and return the response."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )

    return response.choices[0].message.content


if __name__ == "__main__":

    answer = ask_llm(
        "In one sentence, explain what Text-to-SQL means."
    )

    print(answer)