from src.config import *
from src.models.model_loader import load_model
from src.loaders.document_loader import load_documents
from src.pipeline.build_docs import build_docs
from src.vector_store.faiss_store import *
from src.retrieval.bm25_store import build_bm25

def prepare_pipeline():
    model = load_model(EMBED_MODEL)
    
    if BUILD_INDEX:
        loaded_docs = load_documents(DATA_DIR)
        docs = build_docs(loaded_docs)
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