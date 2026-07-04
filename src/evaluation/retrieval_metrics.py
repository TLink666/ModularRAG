from src.evaluation.match import match_gold

def recall_at_k(results, gold, k=5):

    hit = 0
    total = 0

    for r in results:

        q = r["query"]

        if q not in gold:
            continue

        target = gold[q]

        retrieved = r["retrieved"][:k]

        if any(
            match_gold(x, target)
            for x in retrieved
        ):
            hit += 1

        total += 1

    return hit / total if total else 0

def mrr(results, gold):

    scores = []

    for r in results:

        q = r["query"]

        if q not in gold:
            continue

        target = gold[q]

        rr = 0

        for rank, x in enumerate(r["retrieved"], 1):

            if match_gold(x,target):
                rr = 1 / rank
                break

        scores.append(rr)

    return sum(scores) / len(scores) if scores else 0