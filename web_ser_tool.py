from langchain_core.tools import tool
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

# Init client
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """
    Search the web using TAVILY_API_KEY.
    Args:
        query: The search query (question or keywords).
    Returns:
        A summary of relevant search results.
    """
    try:
        response = tavily.search(query, max_results=5)  
        results = [f"- {item['title']}: {item['url']}" for item in response["results"]]
        return f"🔎 Search results for: {query}\n" + "\n".join(results)
    except Exception as e:
        return f"❌ Web search failed: {str(e)}"

