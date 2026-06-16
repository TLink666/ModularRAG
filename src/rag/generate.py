import requests
from src.rag.prompt import build_prompt

def ask_llm(context, question):
    prompt = build_prompt(context, question)
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]