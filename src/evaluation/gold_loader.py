import json

def load_gold(path):
    with open(path, encoding="utf8") as f:
        rows = json.load(f)

    return {
        r["query"]: r
        for r in rows
    }