from src.config import MAX_CONTEXT_CHARS

def build_context(retrieved, max_chars=MAX_CONTEXT_CHARS):
    context=[]
    seen=set()
    total=0
    
    for r in retrieved:
        source=(
            f"{r['source']}"
            if r["page"] is None
            else
            f"{r['source']} Page {r['page']}"
        )
        if (source, r["chunk_id"]) in seen:
            continue
        text=(
f"""
[Source]
{source}

{r["text"]}
"""
        )
        if (total+len(text)>max_chars):
            break
        context.append(text)
        total += len(text)
        seen.add((source,r["chunk_id"]))
    return "\n---\n".join(context)