from sentence_transformers import SentenceTransformer
import numpy as np
from src.chunking.paragraph import split_paragraphs
from src.chunking.recursive import split_sentences
from src.chunking.naive import naive_chunk
from src.config import BREAK_THRESHOLD, SEMANTIC_MODEL

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(SEMANTIC_MODEL)
    return _model


def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def semantic_chunk(text, chunk_size=500, overlap=0, break_threshold=BREAK_THRESHOLD):
    paragraphs = split_paragraphs(text)

    sentences = []
    for p in paragraphs:
        sentences.extend(split_sentences(p))

    if not sentences:
        return []

    model = get_model()
    embeddings = model.encode(sentences)

    chunks = []
    current = ""
    current_emb = None

    for sentence, emb in zip(sentences, embeddings):

        # -------------------------
        # 1. 第一条
        # -------------------------
        if not current:
            current = sentence
            current_emb = emb
            continue

        candidate = (
            sentence
            if not current
            else current + " " + sentence
        )

        # -------------------------
        # 2. 硬约束：太长必须切
        # -------------------------
        if len(candidate) > chunk_size:
            chunks.append(current)
            current = sentence
            current_emb = emb
            continue

        # -------------------------
        # 3. 软约束：语义断裂
        # -------------------------
        sim = cosine(current_emb, emb)

        if sim < break_threshold:
            chunks.append(current)
            current = sentence
            current_emb = emb
            continue

        # -------------------------
        # 4. 否则继续融合
        # -------------------------
        current = candidate
        current_emb = emb  # 更新语义中心

    if current:
        chunks.append(current)

    return chunks