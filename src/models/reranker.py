from src.config import RERANK_MODEL, HF_CACHE
import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
os.environ["HF_HOME"] = HF_CACHE
from src.models.model_loader import load_model
from sentence_transformers import CrossEncoder

def rerank(query, results):

    if not results:
        return results

    model = load_model(
        RERANK_MODEL,
        CrossEncoder
    )

    pairs = [
        (query, r["text"])
        for r in results
    ]

    scores = model.predict(pairs)

    for r, score in zip(results, scores):
        r["rerank_score"] = float(score)

    results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return results