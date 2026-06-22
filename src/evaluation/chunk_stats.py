from collections import Counter
import numpy as np

def analyze_chunks(docs):
    lengths = [
        len(d["text"])
        for d in docs
    ]
    sources = Counter(
        d["source"]
        for d in docs
    )
    tiny = [
        l
        for l in lengths
        if l < 100
    ]

    return {
        "num_chunks": len(docs),
        "avg_length":
        round(np.mean(lengths), 1),
        "min_length": min(lengths),
        "max_length": max(lengths),
        "std":
        round(np.std(lengths),1),
        "tiny_chunks": len(tiny),
        "source_stats": dict(sources)
    }


def print_chunk_stats(stats):
    print("\n=== Chunk Statistics ===")
    print(
        f"Chunks: "
        f"{stats['num_chunks']}"
    )
    print(
        f"Avg length: "
        f"{stats['avg_length']}"
    )
    print(
        f"Min length: "
        f"{stats['min_length']}"
    )
    print(
        f"Max length: "
        f"{stats['max_length']}"
    )
    print(
        f"Std: "
        f"{stats['std']}"
    )
    print(
        f"Tiny (<100): "
        f"{stats['tiny_chunks']}"
    )
    print("\nPer source:")

    for k, v in stats[
        "source_stats"
    ].items():
        print(f"{k}: {v}")