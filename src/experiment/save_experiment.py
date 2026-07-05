import os
import json
from src.config import RESULT_DIR
from datetime import datetime
from src.output.citation import resolve_citations

def save_json(data, path):
    with open(path, "w", encoding="utf8") as f:
        json.dump(
            data,
            f,
            indent=2,
            ensure_ascii=False
        )
        
def prepare_results(results):
    formatted = []

    for result in results:

        citations = resolve_citations(
            result["answer"],
            result["retrieved"]
        )

        retrieved = []

        for r in result["retrieved"]:

            retrieved.append({
                "rank": r["rank"],

                "chunk_id": r["chunk_id"],

                "source": r["source"],
                "page": r["page"],

                "text": r["text"],

                "retriever": r["retriever"],

                "score": r["score"],
                "confidence": r["confidence"],
                "rerank_score": r.get("rerank_score", None),

                "faiss_rank": r["faiss_rank"],
                "faiss_score": r["faiss_score"],
                "faiss_raw_score": r["faiss_raw_score"],

                "bm25_rank": r["bm25_rank"],
                "bm25_score": r["bm25_score"],
                "bm25_raw_score": r["bm25_raw_score"]
            })

        formatted.append({
            "query": result["query"],
            "retrieved": retrieved,
            "answer": result["answer"],
            "citations": citations
        })

    return formatted
    

def save_experiment(
    config,
    results,
    metrics,
    debug_stats,
):
    save_dir = os.path.join(
        RESULT_DIR,
        datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    
    experiment_results = prepare_results(results)

    os.makedirs(save_dir,exist_ok=True)
    
    save_json(config, os.path.join(save_dir, "config.json"))

    save_json(experiment_results, os.path.join(save_dir, "results.json"))

    save_json(metrics, os.path.join(save_dir, "metrics.json"))

    save_json(debug_stats, os.path.join(save_dir, "retrieval_stats.json"))