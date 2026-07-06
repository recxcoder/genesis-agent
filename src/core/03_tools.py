import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", '..'))

from src.utils.ai import llm
from src.tools import search_web, llm_judge, add_todos, print_status

GOAL = "I want to but a hoodi with a fur lined hood. It needs to be full zipper. Near Taj Hotal in Mumbai. Where can I buy one today at 12 PM?"

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
        "content": f"Do you need to search the wen to answer this accurately?\n\nQuestion: {GOAL}"
    }
    ])

    print(f"\n🤔 Search needed: {search_decision}")

    content = ""
    if "YES" in search_decision.upper():
        search_results = search_web(GOAL)
        print("\n📄 Search Results:")
        print(search_results)
        context = search_results

    messages = [
        {
            "role": "system",
            "content": "You are helpful research assistant. Use the provided context to answer correctely."
        },
        {
            "role": "user",
            "content": f"Context:\n\nQuestion: {GOAL}" if context else GOAL
        }
    ]

    answer = llm(messages)

    print("\n" + "-" * 40)
    print(f"Answer: {answer}")

    result = llm_judge(GOAL, answer)

    if not result["done"] and "feedback" in result:
        print("\n Adding feedback as todos...")
        add_todos(result["feedback"])
        print_status
    else:
        print("\nGoal fully completed!")

main()