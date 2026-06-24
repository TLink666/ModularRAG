def retrieval_hit(results, gold):
    hit = 0
    total = 0
    for r in results:
        q = r["query"]
        if q not in gold:
            continue
        total += 1
        target = gold[q]["source"]
        sources = [
            x["source"]
            for x in r["retrieved"]
        ]
        if target in sources:
            hit += 1
    return hit / total