import os

def load_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return [
            {
                "source":
                    os.path.basename(path),
                "text": f.read()
            }

        ]