import src.config as config

def retrieval_guard(retrieved, threshold=config.RETRIEVAL_THRESHOLD):

    if (len(retrieved) == 0):
        return False

    best=max(
        r["confidence"]
        for r
        in retrieved
    )
    return (best>= threshold)