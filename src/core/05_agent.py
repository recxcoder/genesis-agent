import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from datetime import datetime
from src.utils.ai import llm
from src.tools import (
    search_web,
    browse_web,
    llm_judge,
)

GOAL = input("Enter prompt: ")

SYSTEM_PROMPT = f"""
You are a helpful assistant working for a busy executive.
Your tone is friendly but direct, they prefer short clear and direct writing.
You try to accoplish the specific task you are given.
You can use any of the tools available to you.
You always check if the goal is done. If done you send the report to the user.
Today is {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""

MAX_ITERATIONS = 5

def needs_search(goal: str) -> bool:
    decision = llm([
        {
            "role": "system",
            "content": "You are a helpful assistant. Answer in YES or NO."
        },
        {
            "role": "user",
            "content": f"Do you need to search the web to answer this accurately?\n\nQuestion: {goal}"
        }
    ])
    return "YES" in decision.upper()

def gather_context(goal: str) -> str:
    search_results = search_web(goal)

    top_3_url = []
    for line in search_results.splitlines():
        if line.startswith("URL:"):
            top_3_url.append(line.replace("URL:", "").strip())

        if len(top_3_url) == 3:
            break

    page_content = []
    print("\n🌐 Browsing top 3 URLs...")
    for url in top_3_url:
        print(f" -> {url}")
        page_content.append(browse_web(url))
    
    return f"Search Results:\n{search_results}\n\nPage Content:\n{'\n\n'.join(page_content)}"

def run_agent(goal: str):
    """
    Run the agent loop.
    The agent plans, uses tools, judges itself,
    and loops util the goal is complete.
    """
    print("\n" + "-" * 40)
    print(f"Goal: {goal}")
    print("-" * 40)

    context = ""
    if needs_search(goal):
        print("\n🔍 Search needed - gathering context...")
        context = gather_context(goal)
        print("\n Context gathered!")
    else:
        print("\n No search needed - using LLM knowledge directly")


    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nGoal: {goal}" if context else goal
        }
    ]

    iteration = 0

    while iteration < MAX_ITERATIONS:
        iteration += 1
        print(f"\n🔄 Iteration {iteration}/{MAX_ITERATIONS}")

        response = llm(messages)
        print(f"\n🤖 Agent: {response[:300]}...")

        messages.append({
            "role": "assistant",
            "content": response
        })

        result = llm_judge(goal, response)

        if result["done"]:
            print("\n" + "-" * 40)
            print("😊 GOAL COMPLETED!")
            print("-" * 40)
            print(f"\n🧾 Final Answer:\n{response}")
            break

        if "feedback" in result and result["feedback"]:
            feedback_msg = f"Feedback: You still need to complete these tasks: {result['feedback']}"
            messages.append({
                "role": "user",
                "content": feedback_msg
            })
        
        if iteration == MAX_ITERATIONS:
            print("\n⚠️ Max iterations reached!")
            print(f"\n📋 Partial Answer:\n{response}")

def main():
    run_agent(GOAL)

main()