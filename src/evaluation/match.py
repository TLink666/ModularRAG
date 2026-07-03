def match_gold(retrieved, target):
    return (
        retrieved["source"] == target["source"]
        and target["anchor"] in retrieved["text"]
    )