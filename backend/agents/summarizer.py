import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_research(research: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": f"""Summarize the following research into a concise summary (150-200 words), keeping the most important facts only.

Research:
{research}"""
        }]
    )
    return response.choices[0].message.content