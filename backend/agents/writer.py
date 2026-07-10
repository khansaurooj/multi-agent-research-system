from utils.groq_client import client

def write_report(topic: str, summary: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1200,
        messages=[{
            "role": "user",
            "content": f"""You are a professional writer. Using the summary below, write clear, polished content on "{topic}".

If the topic is broad enough for a full report, use these sections: Introduction, Key Concepts, Applications, Challenges, Conclusion.
If the topic is narrow, a quick fact, or a simple question, just write 2-4 well-written paragraphs instead — don't force artificial sections.

Summary:
{summary}"""
        }]
    )
    return response.choices[0].message.content