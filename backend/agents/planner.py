from utils.groq_client import client

def plan_research(topic: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"You are a planning agent. Break down researching this topic into a numbered step-by-step plan. Topic: {topic}"
        }]
    )
    return response.choices[0].message.content