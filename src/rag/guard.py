from src.config import *

def retrieval_guard(retrieved, threshold=RETRIEVAL_THRESHOLD):

    if (len(retrieved) == 0):
        return False

    best=max(
        r["confidence"]
        for r
        in retrieved
    )
    return (best>= threshold)