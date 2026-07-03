from src.evaluation.retrieval_metrics import recall_at_k, mrr

def compute_metrics(results, gold, chunk_stats, errors):
    total = 0

    for item in results:
        if item["query"] in gold:
            total += 1

    return {
        "retrieval":{
            "recall@1": recall_at_k(results, gold, k=1),
            "recall@5": recall_at_k(results, gold, k=5),
            "mrr": mrr(results, gold),
            "top1_failures": len(errors),
            "evaluated_queries": total
        },
        "chunk":{
            "num_chunks": chunk_stats["num_chunks"],
            "avg_length": chunk_stats["avg_length"]
        }
    }