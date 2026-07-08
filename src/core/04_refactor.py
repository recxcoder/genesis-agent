import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.utlis.ai import llm
from src.tools import search_web, browse_web, llm_judge, add_todos, check_todos, print_status

GOAL = "What are the lastest advancements in AI in 2026?"

def search_web(goal: str) -> str:
    search_results = search_web(goal)

    first_url = None

    for line in search_results.splitlines():
        if line.startswith("URL:"):
            first_url = line.replace("URL:", "").strip()
            break

    page_content = ""

    if first_url:
        page_content = browse_web(first_url)

    return f"Search Results:\n{search_results}\n\nPage Content:\n{page_content}"

