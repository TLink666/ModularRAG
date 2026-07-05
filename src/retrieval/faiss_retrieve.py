import faiss

def retrieve(query, model, index, docs, k):
    q_emb = model.encode([query]).astype("float32")
    faiss.normalize_L2(q_emb)
    distances, indices = index.search(q_emb, k)

    results = []

    for rank, idx in enumerate(indices[0]):
        doc = docs[idx]

        results.append({
            "chunk_id": doc["metadata"]["chunk_id"],
            "source": doc["metadata"]["source"],
            "page": doc["metadata"]["page"],
            "num_images": doc["metadata"]["num_images"],
            "text": doc["text"],
            "score": float(distances[0][rank])
        })

    return results