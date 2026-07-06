from src.chunking.naive import naive_chunk
from src.chunking.paragraph import paragraph_chunk
from src.chunking.recursive import recursive_chunk
from src.chunking.semantic import semantic_chunk
import src.config as config

def chunk_text(text, method=config.CHUNK_METHOD, chunk_size=config.CHUNK_SIZE, overlap=config.OVERLAP):
    methods = {
        "naive": naive_chunk,
        "paragraph": paragraph_chunk,
        "recursive": recursive_chunk,
        "semantic": semantic_chunk
    }
    if (method not in methods):
        raise ValueError(method)
    return methods[method](text, chunk_size, overlap)