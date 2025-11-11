# src/providers/tavily.py

import os
import requests

class TavilyWebSearch:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("TAVILY_API_KEY")

    def search(self, query, max_results=3):
        """Performs a web search and returns summarized snippets."""
        url = "https://api.tavily.com/search"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "query": query,
            "max_results": max_results,
            "include_links": True,
            "include_answer": True
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        # Return the summary plus top links (adjust as per actual API response)
        answer = data.get("answer", "")
        links = "\n".join([result['url'] for result in data.get("results", [])])
        return f"{answer}\n\nTop Links:\n{links}"
