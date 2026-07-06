import src.config as config
from src.models.model_loader import load_model
from sentence_transformers import CrossEncoder

def rerank(query, results):

    if not results:
        return results

    model = load_model(
        config.RERANK_MODEL,
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