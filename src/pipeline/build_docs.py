from src.chunking.chunk import chunk_text

def build_docs(loaded_docs):

    docs = []
    chunk_id = 0

    for file in loaded_docs:
        chunks = chunk_text(text=file["text"])
        for chunk in chunks:
            text = chunk if isinstance(chunk, str) else chunk["text"]
            docs.append({
                "text": text,
                "metadata": {
                    "chunk_id": chunk_id,
                    "source": file["source"],
                    "page": file.get("page", None),
                    "num_images": file.get("num_images", 0)
                }
            })

            chunk_id += 1

    return docs