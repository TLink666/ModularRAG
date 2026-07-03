import re

def resolve_citations(answer, retrieved):
    citations = []
    seen = set()

    for match in re.findall(r"\[(\d+)\]", answer):

        idx = int(match) - 1

        if not (0 <= idx < len(retrieved)):
            continue

        r = retrieved[idx]

        key = (r["source"], r["page"])

        if key in seen:
            continue

        seen.add(key)

        citations.append({
            "citation": idx + 1,
            "source": r["source"],
            "page": r["page"]
        })

    return citations