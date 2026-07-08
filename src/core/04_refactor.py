import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.utils.ai import llm
from src.tools import search_web, browse_web, llm_judge, add_todos, check_todos, print_status

GOAL = "What are the latest advancements in AI in 2026?"

def search_and_browse(goal: str) -> str:
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


def answer_goal(goal: str, context: str) -> str:
    return llm([
        {
            "role": "system",
            "content": "You are a helpful research assistant. Use the provided context to answer accurately and in detail."
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nGoal: {goal}"
        }
    ])


def evaluate_answer(goal: str, answer: str) -> str:
    result = llm_judge(goal, answer)

    if not result["done"] and "feedback" in result:
        print("\n Adding feedback as todos...")
        add_todos(result["feedback"])
        print_status()
    
    return result


def main():
    print("\n" + "-" * 40)
    print(f"Goal: {GOAL}")
    
    print("\n🔎 Geathering information...")
    context = search_and_browse(GOAL)

    print("\n Generating answer...")
    answer = answer_goal(GOAL, context)

    print("\n" + "-" * 40)
    print(f"Answer:\n{answer}")

    result = evaluate_answer(GOAL, answer)

    if result["done"]:
        print("\nGoal fully completed!")
    else:
        print(f"Pending todos: {check_todos()}")

main()