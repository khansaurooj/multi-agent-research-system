from utils.groq_client import client
from agents.searcher import search_web

def research_topic(topic: str):
    search_text, sources = search_web(topic)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1200,
        messages=[{
            "role": "user",
            "content": f"""You are a research agent. Using the real search results below, first directly answer the user's question in 2-3 sentences with specific, concrete, current information.

Then provide supporting depth organized under: Key Details, Why It Matters, Considerations/Trade-offs, Additional Context.

Only use facts from the search results — don't invent information not present in them.

Question/Topic: {topic}

Search Results:
{search_text}"""
        }]
    )
    return response.choices[0].message.content, sources