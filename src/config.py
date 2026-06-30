from pathlib import Path

# ========= Path =========

ROOT_DIR = (Path(__file__).parent.parent)

HF_CACHE = r"G:/huggingface_cache"

DATA_DIR = ROOT_DIR/"data"

STORAGE_DIR = ROOT_DIR/"storage"

RESULT_DIR = ROOT_DIR/"results"

EVA_DATA_DIR = DATA_DIR/"evaluation"

# ========= Models =========

OLLAMA_URL = "http://localhost:11434"

LLM_MODEL = "qwen2.5:7b"

EMBED_MODEL = "all-MiniLM-L6-v2"

# ========= Chunk =========

CHUNK_METHOD = "recursive"

CHUNK_SIZE = 500

OVERLAP = 50

# ========= Retrieval =========

TOP_K = 5

HYBRID_ALPHA = 0.7

RETRIEVAL_METHOD = "rrf"

RRF_K = 5

ENABLE_GUARD=True

RETRIEVAL_THRESHOLD=0.5

# ========= Experiment =========

DEBUG = False

BUILD_INDEX = True

MAX_CONTEXT_CHARS = 3000



def print_config():
    print("\n===== CONFIG =====")
    print(
        f"Chunk:"
        f" {CHUNK_METHOD}"
    )
    print(
        f"Size:"
        f" {CHUNK_SIZE}"
    )
    print(
        f"Overlap:"
        f" {OVERLAP}"
    )
    print(
        f"TopK:"
        f" {TOP_K}"
    )
    print(
        f"Hybrid:"
        f" {HYBRID_ALPHA}"
    )
    
def export_config():
    return {
        "chunk_size":CHUNK_SIZE,
        "overlap":OVERLAP,
        "method":CHUNK_METHOD,
        "top_k":TOP_K,
        "alpha":HYBRID_ALPHA,
        "max_context_chars":MAX_CONTEXT_CHARS
    }