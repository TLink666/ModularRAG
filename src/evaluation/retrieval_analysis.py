from src.evaluation.match import match_gold

def analyze_retrieval_errors(results, gold):

    errors = []

    for result in results:

        query = result["query"]

        if query not in gold:
            continue

        target = gold[query]
        retrieved = result["retrieved"]

        gold_rank = None

        for r in retrieved:
            if match_gold(r, target):
                gold_rank = r["rank"]
                break

        if (
            len(retrieved) > 0
            and match_gold(retrieved[0], target)
        ):
            continue
        
        if gold_rank is None:
            error_type = "miss"
        else:
            error_type = "low_rank"

        errors.append({
            "query": query,
            "type": error_type,
            "gold": target,
            "gold_rank": gold_rank,
            "retrieved": [
                {
                    "rank": r["rank"],
                    "source": r["source"],
                    "score": r["score"]
                }
                for r in retrieved
            ]
        })

    return errors