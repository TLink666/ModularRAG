def analyze_retrieval_errors(results, gold):
    errors = []

    for result in results:
        query = result["query"]

        if query not in gold:
            continue

        target = gold[query]
        retrieved = result["retrieved"]

        gold_rank = None   # ← 放到这里

        for r in retrieved:
            if r["source"] == target:
                gold_rank = r["rank"]
                break

        if (
            len(retrieved) > 0 and
            retrieved[0]["source"] == target
        ):
            continue

        errors.append({
            "query": query,
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