import re

def chunk_text(text, method="paragraph", chunk_size=200, overlap=50):
    if method == "naive":
        return naive_chunk(text, chunk_size, overlap)
    if method == "paragraph":
        return paragraph_chunk(text, chunk_size, overlap)
    raise ValueError()

def naive_chunk(text, chunk_size=200, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # overlap避免语义断裂
    return chunks

def split_paragraphs(text: str):
    # 1. normalize
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    # 2. split by blank line
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def paragraph_chunk(text, chunk_size=500, overlap=50):
    paragraphs = split_paragraphs(text)
    chunks = []
    chunk_id = 0
    current = ""

    def flush():
        nonlocal current, chunk_id

        if current:
            chunks.append({
                "chunk_id": chunk_id,
                "text": current
            })
            chunk_id += 1
            # 保留 overlap
            current = current[-overlap:]

    for p in paragraphs:

        # ===== 超长 paragraph =====

        if len(p) > chunk_size:

            # 输出已有内容
            if current:

                chunks.append({
                    "chunk_id": chunk_id,
                    "text": current
                })
                chunk_id += 1

            # 长句不继承旧 overlap
            current = ""
            start = 0
            while True:
                end = start + chunk_size

                # 最后一段
                if end >= len(p):
                    tail = p[start:]
                    # 不直接输出
                    current = (
                        p[max(0, start-overlap):start]
                        + tail
                    )
                    break
                chunk = p[start:end]
                chunks.append({
                    "chunk_id": chunk_id,
                    "text": chunk
                })
                chunk_id += 1
                # 滑动
                start += chunk_size - overlap
            continue

        # ===== 普通 paragraph =====

        candidate = (
            current + p
            if not current
            else current + "\n\n" + p
        )

        if len(candidate) <= chunk_size:
            current = candidate
        else:
            flush()
            current = p

    if current:
        chunks.append({
            "chunk_id": chunk_id,
            "text": current
        })
    return chunks