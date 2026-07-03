def print_retrieval_stats(stats):

    print("\n=== Retrieval Statistics ===")

    print(f"Queries: {stats['num_queries']}")
    print(f"Avg confidence: {stats['avg_confidence']}")
    print(f"Min confidence: {stats['min_confidence']}")
    print(f"Max confidence: {stats['max_confidence']}")
    print(f"Unique sources: {stats['unique_sources']}")

    print("\nTop reused chunks:")

    for cid, count in stats["top_chunks"]:
        print(f"Chunk {cid}: {count}")