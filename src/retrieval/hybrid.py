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
    for r in faiss_results:
        r["faiss_raw_score"] = r["score"]
    faiss_results = normalize_scores(faiss_results)
    for r in bm25_results:
        r["bm25_raw_score"] = r["score"]
    bm25_results = normalize_scores(bm25_results)
    merged = {}
    for r in faiss_results:
        cid = r["chunk_id"]
        merged[cid] = {
            **r,
            "retriever": "faiss",
            "faiss_score": r["score"],
            "bm25_raw_score": None,
            "bm25_score": 0
        }
    for r in bm25_results:
        cid = r["chunk_id"]
        if cid not in merged:
            merged[cid] = {
                **r,
                "retriever": "bm25",
                "faiss_raw_score": None,
                "faiss_score": 0,
                "bm25_score": r["score"]
            }
        else:
            merged[cid]["bm25_raw_score"] = r["bm25_raw_score"]
            merged[cid]["bm25_score"] = r["score"]
            if (merged[cid]["faiss_score"]>0 and r["bm25_score"]>0):
                merged[cid]["retriever"] = "hybrid"
    for cid in merged:
        merged[cid]["score"] = (alpha * merged[cid]["faiss_score"] + (1-alpha) * merged[cid]["bm25_score"])
    results = sorted(
        merged.values(),
        key=lambda x:x["score"],
        reverse=True
    )[:k]
    for i, r in enumerate(results, 1):
        r["rank"] = i
    return results