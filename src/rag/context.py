import src.config as config

def build_context(retrieved, max_chars=config.MAX_CONTEXT_CHARS):
    context = []
    seen = set()
    total = 0

    for idx, r in enumerate(retrieved, 1):
        key = (r["source"], r["page"], r["chunk_id"])
        if key in seen:
            continue
        text = f"""
[{idx}]
{r["text"]}
""".strip()
        if total + len(text) > max_chars:
            break
        context.append(text)
        total += len(text)
        seen.add(key)

    return "\n\n---\n\n".join(context)