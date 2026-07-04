from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()
client = Groq()
MODEL="llama-3.3-70b-versatile"

prompt = "When did the name of twitter changed to X?"

def main():
    print("\n" + "#" * 40)
    print(f"Question: {prompt}")
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", 
             "content": prompt
            }
        ]
    )

    answer = completion.choices[0].message.content.strip()

    print("\n" + "#" * 40)
    print(f"Answer: {answer}")

    check = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an expert evaluator. You must respond in valid JSON only. No extra text."
            },
            {
                "role": "user",
                "content": f"""Given the following question, determine if the answer fully resolves the question.

                Question: {prompt}
                Answer: {answer}

                Respond with this exact JSON format:
                {{"done": true}} if the answer is complete
                {{"done": false}} if the answer is incomplete"""
            }
        ],
        response_format={"type": "json_object"}
    )
    
    result = json.loads(check.choices[0].message.content)

    print("\n" + "#" * 40)
    print(f"LLM as judge: {'👍' if result['done'] else '👎'}")

main()