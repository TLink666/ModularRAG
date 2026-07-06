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

SEMANTIC_MODEL = EMBED_MODEL

RERANK_MODEL="BAAI/bge-reranker-base"

TESSERACT = r"G:/tools/Tesseract-OCR/tesseract.exe"

HF_ENDPOINT = "https://hf-mirror.com"

HF_OFFLINE = True

# ========= Loader =========

ENABLE_OCR = True

OCR_MIN_LENGTH = 20

OCR_MIN_LETTERS = 5

# ========= Chunk =========

CHUNK_METHOD = "semantic"

CHUNK_SIZE = 500

OVERLAP = 50

SEMANTIC_BREAK_THRESHOLD = 0.2

# ========= Retrieval =========

RETRIEVE_TOP_K = 20

FINAL_TOP_K = 5

USE_RERANKER = True

HYBRID_ALPHA = 0.7

RETRIEVAL_METHOD = "rrf"

RRF_K = 5

RETRIEVAL_THRESHOLD = 0.5

# ========= Generation =========

ENABLE_GUARD = True

MAX_CONTEXT_CHARS = 3000

# ========= Experiment =========

DEBUG = False

BUILD_INDEX = True



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
        f" {FINAL_TOP_K}"
    )
    print(
        f"Hybrid:"
        f" {HYBRID_ALPHA}"
    )
    
def export_config():
    return {
        # Models
        "llm_model": LLM_MODEL,
        "embed_model": EMBED_MODEL,

        # Chunk
        "chunk_method": CHUNK_METHOD,
        "chunk_size": CHUNK_SIZE,
        "overlap": OVERLAP,

        # Retrieval
        "retrieval_method": RETRIEVAL_METHOD,
        "top_k": FINAL_TOP_K,
        "hybrid_alpha": HYBRID_ALPHA,
        "rrf_k": RRF_K,

        # Generation
        "max_context_chars": MAX_CONTEXT_CHARS,

        # Guard
        "enable_guard": ENABLE_GUARD,
        "retrieval_threshold": RETRIEVAL_THRESHOLD,
    }