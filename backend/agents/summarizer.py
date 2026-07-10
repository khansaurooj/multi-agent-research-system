from utils.groq_client import client

def summarize_research(research: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=400,
        messages=[{
            "role": "user",
            "content": f"""Summarize the text below. Your summary must be significantly shorter than the original — capture only the core point and 2-3 key supporting details. Do not repeat sentences verbatim from the original; rewrite in your own words.

Text:
{research}"""
        }]
    )
    return response.choices[0].message.content