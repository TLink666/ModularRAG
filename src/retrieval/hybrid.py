from src.retrieval.bm25_store import *
from src.retrieval.faiss_retrieve import retrieve
from src.retrieval.score import calibrate_score
from src.models.reranker import rerank
import src.config as config

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

def retrieve_candidates(query, model, index, bm25, docs):

    faiss_results = retrieve(query, model, index, docs, config.RETRIEVE_TOP_K)

    bm25_results = search_bm25(bm25, docs, query, config.RETRIEVE_TOP_K)

    return faiss_results, bm25_results

def normalize_candidates(faiss_results, bm25_results):

    for r in faiss_results:
        r["faiss_raw_score"] = r["score"]

    normalize_scores(faiss_results)

    for r in bm25_results:
        r["bm25_raw_score"] = r["score"]

    normalize_scores(bm25_results)

    return faiss_results, bm25_results

def merge_candidates(faiss_results, bm25_results):

    merged = {}

    for rank, r in enumerate(faiss_results, 1):
        cid = r["chunk_id"]
        merged[cid] = {
            **r,
            "faiss_rank": rank,
            "bm25_rank": None,
            "retriever": "faiss",
            "faiss_score": r["score"],
            "bm25_raw_score": None,
            "bm25_score": 0
        }
    for rank, r in enumerate(bm25_results, 1):
        cid = r["chunk_id"]
        if cid not in merged:
            merged[cid] = {
                **r,
                "faiss_rank": None,
                "bm25_rank": rank,
                "retriever": "bm25",
                "faiss_raw_score": None,
                "faiss_score": 0,
                "bm25_score": r["score"]
            }

    return merged

def compute_fusion_scores(merged, alpha):

    for cid in merged:

        if config.RETRIEVAL_METHOD == "weighted":
            merged[cid]["score"] = (alpha * merged[cid]["faiss_score"] + (1-alpha) * merged[cid]["bm25_score"])

        elif config.RETRIEVAL_METHOD == "rrf":
            score = 0
            if (merged[cid]["faiss_rank"]is not None):
                score += (1 /(config.RRF_K+merged[cid]["faiss_rank"]))
            if (merged[cid]["bm25_rank"]is not None):
                score += (1 /(config.RRF_K+merged[cid]["bm25_rank"]))
            merged[cid]["score"]=score

    return merged

def finalize_results(results, k):
    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )[:k]
    results = calibrate_score(results)
    for rank, result in enumerate(results, 1):
        result["rank"] = rank

    return results

def finalize_results(results, query):

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    results = results[:config.RETRIEVE_TOP_K]

    results = calibrate_score(results)

    if config.USE_RERANKER:
        results = rerank(query, results)

    results = results[:config.FINAL_TOP_K]

    for rank, result in enumerate(results, 1):
        result["rank"] = rank

    return results


def hybrid_retrieve(query, model, index, bm25, docs, alpha=config.HYBRID_ALPHA):

    faiss_results, bm25_results = retrieve_candidates(query, model, index, bm25, docs)

    faiss_results, bm25_results = normalize_candidates(
        faiss_results,
        bm25_results
    )

    merged = merge_candidates(
        faiss_results,
        bm25_results
    )

    merged = compute_fusion_scores(
        merged,
        alpha
    )

    return finalize_results(
        list(merged.values()),
        query
    )