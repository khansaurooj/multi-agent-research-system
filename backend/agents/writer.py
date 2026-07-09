import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def write_report(topic: str, summary: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1200,
        messages=[{
            "role": "user",
            "content": f"""You are a professional report writer. Using the summary below, write a well-structured report on "{topic}" with these sections: Introduction, Key Concepts, Applications, Challenges, Conclusion. Use clear, professional language.

Summary:
{summary}"""
        }]
    )
    return response.choices[0].message.content