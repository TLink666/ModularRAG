from src.chunking import chunk_text

def build_docs(loaded_docs, method, chunk_size=200, overlap=50):

    docs = []
    chunk_id = 0

    for file in loaded_docs:
        chunks = chunk_text(
            text=file["text"],
            method=method,
            chunk_size=chunk_size,
            overlap=overlap
        )

        for chunk in chunks:
            if isinstance(chunk, str):
                text = chunk
            else:
                text = chunk["text"]
            docs.append({
                "chunk_id": chunk_id,
                "source": file["source"],
                "page": file["page"],
                "text": text
            })
            chunk_id += 1
    return docs