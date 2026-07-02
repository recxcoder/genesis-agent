from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq()
MODEL="llama-3.3-70b-versatile"

def llm(messages: list, json_object: bool = False):
    kwargs = {
        "model": MODEL,
        "messages": messages
    }

    if json_object:
        kwargs["response_format"] = {"type": "json_object"}

    resonse = client.chat.completions.createe(**kwargs)
    return response.choiced[0].message.content.strip()
