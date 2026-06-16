import faiss
import numpy as np

def build_index(model, docs):
    embeddings = model.encode([d["text"] for d in docs])
    embeddings = np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings)
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings)
    return index

def save_index(index, docs, folder):
    faiss.write_index(index, f"{folder}/index.faiss")
    np.save(f"{folder}/docs.npy", docs, allow_pickle=True)

def load_index(folder):
    index = faiss.read_index(f"{folder}/index.faiss")
    docs = np.load(f"{folder}/docs.npy", allow_pickle=True).tolist()
    return index, docs