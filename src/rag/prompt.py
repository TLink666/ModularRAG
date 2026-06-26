def build_prompt(context, question):
    return f"""
You are a retrieval-based assistant.
Answer ONLY using the provided context.
If the answer is not contained in the context,
say:
"I cannot find the answer in the provided documents."

Context:
{context}

Question:
{question}
"""