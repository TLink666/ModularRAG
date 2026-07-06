import requests
from src.rag.prompt import build_prompt
import src.config as config
from src.rag.context import build_context
from src.rag.guard import retrieval_guard

def ask_llm(retrieved, question, model = config.LLM_MODEL):
    if config.ENABLE_GUARD:
        if not retrieval_guard(retrieved):
            return "I don't have enough information in the retrieved documents."
    context = build_context(retrieved)
    prompt = build_prompt(context, question)
    res = requests.post(
        f"{config.OLLAMA_URL}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]