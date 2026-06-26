from src.rag.generate import ask_llm
from src.retrieval.hybrid import hybrid_retrieve

def batch_query(queries, model, index, bm25, docs):
    results=[]
    for query in queries:
        retrieved = hybrid_retrieve(query, model, index, bm25, docs)
        answer = ask_llm(retrieved, query)
        results.append({
            "query": query,

            "retrieved": retrieved,

            "answer": answer
        })
    return results