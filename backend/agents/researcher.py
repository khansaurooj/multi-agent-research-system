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
            "content": f"""You are a research agent. Provide detailed, factual information on the following topic, organized under these headings: Definition, History, How it Works, Applications, Advantages, Disadvantages.

Topic: {topic}"""
        }]
    )
    return response.choices[0].message.content