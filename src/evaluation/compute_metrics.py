from src.evaluation.retrieval_metrics import recall_at_k, mrr
from src.evaluation.match import match_gold

def compute_metrics(results, gold, chunk_stats, errors):
    total = 0
    per_query = {}

    for item in results:
        q = item["query"]
        if q in gold:
            total += 1

    global_metrics = {
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
    
    for r in results:
        q = r["query"]
        if r["query"] not in gold:
            continue

        target = gold[q]
        retrieved = r["retrieved"]

        hit_at_1 = False
        rr = 0
        gold_rank = None

        for i, x in enumerate(retrieved, 1):
            # match
            if match_gold(x, target):
                if not hit_at_1 and i == 1:
                    hit_at_1 = True

                if rr == 0:
                    rr = 1 / i
                    gold_rank = i

        per_query[q] = {
            "hit@1": hit_at_1,
            "mrr": rr,
            "gold_rank": gold_rank,
            "top1_source": retrieved[0]["source"] if retrieved else None
        }

    return {
        **global_metrics,
        "per_query": per_query
    }