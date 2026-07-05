import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.utils.ai import llm
import json

PROMPT = """
You are a research assistant who reads requests and answers.
You determine if the answer satisfies the request.
If it does, you respond that the request is done.
If not, you give specific feedback on what is missing
in the form of actionable individual todos.
"""

def llm_judge(goal: str, answer: str) -> dict:
    """
    Judge whether the answer fully resolves the goal.

    Args: 
        goal: the original goal/request
        answer: the answer to evaluate

    Returns:
        dict: {
        "done": bool,
        "feedback": list of strings (empty if done)
        }
    """

    result = llm(
        messages=[
            {
                "role": "system",
                "content": PROMPT
            },
            {
                "role": "user",
                "content": f"""## Request: {goal}
                
                ## Answer: {answer}

                Respond in JSON fromat excatly like this:
                {{"done": true, "feedback": []}} if answer is complete
                {{"done": false, "feedback: ["todo 1", "todo 2"]}}
                """
            }
        ],
        json_mode=True
    )

    check = json.loads(result)

    print("\n" + "#" * 40)
    print(f"LLM as judge: {'👍' if check['done'] else '👎'}")

    if not check["done"] and "feedback" in check:
        print("📋 Feedback:")
        for item in check["feedback"]:
            print(f" - {item}")

    return check