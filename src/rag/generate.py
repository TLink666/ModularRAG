import requests
from src.rag.prompt import build_prompt
from src.config import *
from src.rag.context import build_context

def ask_llm(retrieved, question):
    context = build_context(retrieved)
    prompt = build_prompt(context, question)
    res = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": "qwen2.5:7b",
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]