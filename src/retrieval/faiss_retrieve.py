import faiss

def retrieve(query, model, index, docs, k):
    q_emb = model.encode([query]).astype("float32")
    faiss.normalize_L2(q_emb)
    distances, indices = index.search(q_emb, k)
    results = []
    for rank, idx in enumerate(indices[0]):
        results.append({
            "chunk_id": docs[idx]["chunk_id"],
            "source": docs[idx]["source"],
            "score": float(distances[0][rank]),
            "page": docs[idx]["page"],
            "text": docs[idx]["text"]
        })
    return results