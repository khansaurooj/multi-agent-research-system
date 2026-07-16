import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str):
    results = tavily.search(query=query, max_results=5)

    formatted_text = ""
    sources = []

    for r in results.get("results", []):
        formatted_text += f"Source: {r['title']}\nURL: {r['url']}\nContent: {r['content']}\n\n"
        sources.append({"title": r['title'], "url": r['url']})

    return formatted_text, sources