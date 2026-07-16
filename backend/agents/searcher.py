import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query: str) -> str:
    results = tavily.search(query=query, max_results=5)

    formatted = ""
    for r in results.get("results", []):
        formatted += f"Source: {r['title']}\nURL: {r['url']}\nContent: {r['content']}\n\n"

    return formatted if formatted else "No search results found."