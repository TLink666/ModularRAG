import re
from src.chunking.naive import naive_chunk
from src.chunking.paragraph import split_paragraphs


def split_sentences(text):
    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    return [
        s.strip()
        for s in sentences
        if s.strip()
    ]


def recursive_chunk(text, chunk_size=500, overlap=50):

    paragraphs = split_paragraphs(text)
    chunks = []
    current = ""

    for p in paragraphs:
        # 当前chunk还能放
        if (len(current)+len(p)<=chunk_size):
            if current:
                current += "\n\n"
            current += p
            continue
        # 当前先结束
        if current:
            chunks.append(current)
            current = ""
        # 整段可放
        if (len(p)<=chunk_size):
            current = p
            continue

        # ===== 长段处理 =====
        sentences = split_sentences(p)
        for s in sentences:
            # 当前chunk还能放
            if (len(current)+len(s)<=chunk_size):
                if current:
                    current += " "
                current += s
                continue
            # 当前先输出
            if current:
                chunks.append(current)
                current = ""
            # ===== 超长句 =====
            if (len(s)>chunk_size):
                long_chunks = naive_chunk(s, chunk_size, overlap)
                chunks.extend(long_chunks[:-1])
                current = (long_chunks[-1])
            else:
                if current:
                    current += " "
                current += s
    if current:
        chunks.append(current)
    return chunks
                