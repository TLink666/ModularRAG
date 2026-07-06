import streamlit as st

import src.env  # 必须最先执行
import src.config as config
from src.pipeline.run_rag import build_pipeline, run_query, run_rag
from src.output.citation import resolve_citations


# ======================
# Session State
# ======================
if "pipeline" not in st.session_state:
    st.session_state.pipeline = None


# ======================
# Sidebar (Config)
# ======================
st.sidebar.title("⚙️ Config")

config.CHUNK_METHOD = st.sidebar.selectbox(
    "Chunk Method",
    ["naive", "paragraph", "recursive", "semantic"]
)

config.CHUNK_SIZE = st.sidebar.slider(
    "Chunk Size",
    100, 2000, config.CHUNK_SIZE
)

config.RETRIEVE_TOP_K = st.sidebar.slider(
    "Retrieve Top K (Recall)",
    5, 50, config.RETRIEVE_TOP_K
)

config.FINAL_TOP_K = st.sidebar.slider(
    "Final Top K (Precision)",
    1, 10, config.FINAL_TOP_K
)

config.HYBRID_ALPHA = st.sidebar.slider(
    "Hybrid Alpha",
    0.0, 1.0, config.HYBRID_ALPHA
)

config.USE_RERANKER = st.sidebar.checkbox(
    "Use Reranker",
    value=config.USE_RERANKER
)

config.ENABLE_OCR = st.sidebar.checkbox(
    "Enable OCR",
    value=config.ENABLE_OCR
)


# ======================
# Build Pipeline
# ======================
if st.sidebar.button("🔨 Build / Rebuild Pipeline"):
    with st.spinner("Building pipeline..."):
        st.session_state.pipeline = build_pipeline()
    st.success("Pipeline built!")


# 自动初始化
if st.session_state.pipeline is None:
    st.session_state.pipeline = build_pipeline()


pipeline = st.session_state.pipeline


# ======================
# Main UI
# ======================
st.title("🔍 RAG System Demo")


query = st.text_input("Ask a question")


# ======================
# MODE 1: USER QUERY
# ======================
if query.strip():
    with st.status("🤔 Thinking...", expanded=False) as status:
        result = run_query(query, pipeline)
        status.update(
            label="✅ Finished",
            state="complete"
        )
    st.subheader("🧠 Answer")
    st.write(result["answer"])

    # citations
    citations = resolve_citations(
        result["answer"],
        result["retrieved"]
    )

    if citations:
        st.subheader("📚 Citations")
        for c in citations:
            st.write(f"[{c['citation']}] {c['source']} Page {c['page']}")

    # retrieved chunks
    st.subheader("📄 Retrieved Chunks")

    for r in result["retrieved"]:
        st.markdown(f"""
        ---
        **Score:** {r.get('score')}
        **Source:** {r.get('source')} (Page {r.get('page')})
        
        {r.get('text')}
        """)


# ======================
# MODE 2: BENCHMARK
# ======================
else:

    st.subheader("📊 Benchmark Mode")

    if st.button("Run Evaluation"):
        queries = [
            "What are the main challenges of implementing memory in AI systems, and how do retrieval mechanisms address these challenges?",
            "What enabled computers to move from room-sized machines to home and school devices?",
            "Which brewing method uses pressure to produce concentrated flavor and serves as the base for drinks such as cappuccino and latte?",
            "What has helped reduce the cost and increase the frequency of space launches in modern space exploration?",
            "What are some recent developments in urban transportation systems?",
            "What is the gameplay loop in game design?",
            "Why is this type of lorem ipsum style text used in retrieval system testing?",
            "What does cosine similarity focus on in vector embeddings?",
            "Why is data quality often more important than model complexity in machine learning systems?",
            "What do users prefer in AI systems?",
            "Who invented quantum mechanics?",
            "What is the name displayed on the entrance gate in the accompanying image?",
            "What message is written on the greeting card shown in the accompanying image?",
            "What does the sign in the photo or image say?",
            "what words does Peter like?"
        ]
        with st.status("Running Evaluation...", expanded=True) as status:
            results, metrics, docs, chunk_stats, debug_stats, errors = run_rag(
                queries=queries  # 或你原来的gold queries
            )
            status.update(
                label="Evaluation Complete!",
                state="complete"
            )

        st.subheader("📈 Metrics")
        st.json(metrics)

        st.subheader("📦 Chunk Stats")
        st.json(chunk_stats)

        st.subheader("🐛 Debug Stats")
        st.json(debug_stats)

        st.subheader("⚠️ Errors")
        st.json(errors)