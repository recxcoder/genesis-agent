import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", '..'))

from src.utils.ai import llm
from src.tools import search_web, llm_judge, add_todos, print_status

GOAL = "I want to but a hoodie with a fur lined hood. It needs to be full zipper. Near Taj Hotal in Mumbai. Where can I buy one today at 12 PM?"

def main():
    print("\n" + "-" * 40)
    print(f"Goal: {GOAL}")

    search_decision = llm([
    {
        "role": "system",
        "content": "You are a helpful assistant. Answer only YES or NO."
    },
    {
        "role": "user",
        "content": f"Do you need to search the web to answer this accurately?\n\nQuestion: {GOAL}"
    }
    ])

    print(f"\n🤔 Search needed: {search_decision}")

    context = ""
    if "YES" in search_decision.upper():
        context = search_web(GOAL)
        print("\n📄 Search Results:")
        print(context)

    messages = [
        {
            "role": "system",
            "content": "You are helpful research assistant. Use the provided context to answer correctely."
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {GOAL}" if context else GOAL
        }
    ]

    answer = llm(messages)

    print("\n" + "-" * 40)
    print(f"Answer: {answer}")

    result = llm_judge(GOAL, answer)

    if not result["done"] and "feedback" in result:
        print("\n Adding feedback as todos...")
        add_todos(result["feedback"])
        print_status()
    else:
        print("\nGoal fully completed!")

main()