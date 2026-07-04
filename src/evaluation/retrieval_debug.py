from collections import Counter
import numpy as np

def retrieval_debug_stats(results):
    all_conf = []
    sources = []
    chunks = []
    for r in results:
        retrieved = r["retrieved"]
        for x in retrieved:
            all_conf.append(x["confidence"])
            sources.append(x["source"])
            chunks.append(x["chunk_id"])
    return {
        "num_queries": len(results),
        "avg_confidence":
            round(np.mean(all_conf),3),
        "min_confidence":
            round(min(all_conf),3),
        "max_confidence":
            round(max(all_conf),3),
        "unique_sources":
            len(set(sources)),
        "top_chunks":
            Counter(chunks).most_common(5)
    }