from rank_bm25 import BM25Okapi

def build_bm25(docs):
    corpus = [
        d["text"].split()
        for d in docs
    ]
    bm25 = BM25Okapi(corpus)
    return bm25

def search_bm25(bm25, docs, query, k=5):
    scores = bm25.get_scores(query.split())
    ranked = sorted(
        enumerate(scores),
        key=lambda x: x[1],
        reverse=True
    )
    results = []
    for idx, score in ranked[:k]:
        doc = docs[idx]
        results.append({
            "chunk_id": doc["metadata"]["chunk_id"],
            "source": doc["metadata"]["source"],
            "page": doc["metadata"]["page"],
            "num_images": doc["metadata"]["num_images"],
            "text": doc["text"],
            "score": float(score),
            "retriever": "bm25"
        })
    return results