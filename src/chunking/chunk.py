from src.chunking.naive import naive_chunk
from src.chunking.paragraph import paragraph_chunk
from src.chunking.recursive import recursive_chunk
from src.config import CHUNK_METHOD, CHUNK_SIZE, OVERLAP

def chunk_text(text, method=CHUNK_METHOD, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    methods = {
        "naive": naive_chunk,
        "paragraph": paragraph_chunk,
        "recursive": recursive_chunk
    }
    if (method not in methods):
        raise ValueError(method)
    return methods[method](text, chunk_size, overlap)