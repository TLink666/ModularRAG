from src.rag.generate import ask_llm
from src.rag.prompt import build_context
from src.retrieval.hybrid import hybrid_retrieve

def batch_query(queries, model, index, bm25, docs):
    results=[]
    for query in queries:
        retrieved = hybrid_retrieve(query, model, index, bm25, docs)
        context = build_context(retrieved)
        answer = ask_llm(context, query)
        results.append({
            "query": query,

            "retrieved": retrieved,

            "answer": answer
        })
    return results