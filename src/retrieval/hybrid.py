from src.retrieval.bm25_store import *

def normalize_scores(results):
    scores = [r["score"] for r in results]
    mx = max(scores)
    mn = min(scores)
    if mx == mn:
        for r in results:
            r["score"] = 0.5
        return results
    for r in results:
        r["score"] = (r["score"]-mn) / (mx-mn)
    return results

def hybrid_retrieve(query, retrieve_fn, bm25, docs, k=5, alpha=0.7):
    faiss_results = retrieve_fn(query, k=k)
    bm25_results = search_bm25(bm25, docs, query, k=k)
    faiss_results = normalize_scores(faiss_results)
    bm25_results = normalize_scores(bm25_results)
    merged = {}

    for r in faiss_results:
        cid = r["chunk_id"]
        merged[cid] = {
            **r,

            "faiss_score": r["score"],

            "bm25_score": 0
        }

    for r in bm25_results:
        cid = r["chunk_id"]
        if cid not in merged:
            merged[cid] = {
                **r,

                "faiss_score": 0,

                "bm25_score": r["score"]
            }
        else:
            merged[cid]["bm25_score"] = r["score"]

    for cid in merged:
        merged[cid]["score"] = (alpha * merged[cid]["faiss_score"] + (1-alpha) * merged[cid]["bm25_score"])
    return sorted(merged.values(), key=lambda x:x["score"], reverse=True)[:k]