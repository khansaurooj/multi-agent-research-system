import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def research_topic(topic: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""You are a research agent. First, directly answer the user's question in 2-3 sentences with specific, concrete information (real names, numbers, or recommendations if relevant — no vague generalities).

Then provide supporting depth organized under: Key Details, Why It Matters, Considerations/Trade-offs, Additional Context.

Question/Topic: {topic}"""
        }]
    )
    return response.choices[0].message.content