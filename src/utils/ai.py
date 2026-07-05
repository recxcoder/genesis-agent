from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()
MODEL="llama-3.3-70b-versatile"

def llm(messages: list, json_mode: bool = False) -> str:
    kwargs = {
        "model": MODEL,
        "messages": messages
    }

    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content.strip()
