def analyze_overlap(docs):

    overlaps = []

    for i in range(len(docs) - 1):

        a = docs[i]["text"]
        b = docs[i + 1]["text"]

        max_overlap = 0

        for k in range(1, min(len(a), len(b)) + 1):
            if a[-k:] == b[:k]:
                max_overlap = k

        if max_overlap > 0:
            overlaps.append({
                "idx": i,
                "overlap": max_overlap
            })

    return overlaps

def print_overlap(overlaps):

    print("\n=== Chunk Overlap (non-zero) ===")

    for o in overlaps:
        print(f"Chunk {o['idx']} -> {o['overlap']}")