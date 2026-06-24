# ========= Path =========

HF_CACHE = r"G:\huggingface_cache"

DATA_DIR = "../data"

STORAGE_DIR = "../storage"

RESULT_DIR = "../results"

EVA_DATA_DIR = DATA_DIR + "/evaluation"

# ========= Models =========

OLLAMA_URL = "http://localhost:11434"

LLM_MODEL = "qwen2.5:7b"

EMBED_MODEL = "all-MiniLM-L6-v2"

# ========= Chunk =========

CHUNK_METHOD = "paragraph"

CHUNK_SIZE = 500

OVERLAP = 50

# ========= Retrieval =========

TOP_K = 5

HYBRID_ALPHA = 0.7

# ========= Experiment =========

DEBUG = False



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