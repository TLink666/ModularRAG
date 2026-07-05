import requests
from src.rag.prompt import build_prompt
from src.config import *
from src.rag.context import build_context
from src.rag.guard import retrieval_guard

def ask_llm(retrieved, question, model = LLM_MODEL):
    if ENABLE_GUARD:
        if not retrieval_guard(retrieved):
            return "I don't have enough information in the retrieved documents."
    context = build_context(retrieved)
    prompt = build_prompt(context, question)
    res = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]