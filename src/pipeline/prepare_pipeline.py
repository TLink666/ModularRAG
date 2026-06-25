import os
from sentence_transformers import SentenceTransformer
from src.config import *
from src.loaders.document_loader import load_documents
from src.pipeline.build_docs import build_docs
from src.vector_store.faiss_store import *
from src.retrieval.bm25_store import build_bm25

def prepare_pipeline():
    os.environ["HF_HOME"] = HF_CACHE
    model = SentenceTransformer(EMBED_MODEL)
    
    if BUILD_INDEX:
        loaded_docs = load_documents(DATA_DIR)
        docs = build_docs(loaded_docs, CHUNK_METHOD, CHUNK_SIZE, OVERLAP)
        index = build_index(model, docs)
        save_index(index, docs, STORAGE_DIR)
    else:
        index, docs = load_index(STORAGE_DIR)
    bm25 = build_bm25(docs)

    return (
        model,
        docs,
        index,
        bm25
    )