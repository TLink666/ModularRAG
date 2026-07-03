def build_prompt(context, question):
    return f"""
You are a retrieval-based question answering assistant.
Use ONLY the information provided in the context.
Do not use prior knowledge.

If the context does not contain enough information to answer the question,
reply exactly:
"I cannot find the answer in the provided documents."

Do not speculate.
Do not make up facts.

Context:
{context}

Question:
{question}
"""