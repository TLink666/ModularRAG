import os
from src.config import HF_CACHE
from sentence_transformers import CrossEncoder

os.environ["HF_HOME"] = HF_CACHE

model = CrossEncoder("BAAI/bge-reranker-base")

def rerank(query, results):
    return results