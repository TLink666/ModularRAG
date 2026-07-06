import streamlit as st

import src.env  # 必须最先执行
import src.config as config
from src.pipeline.run_rag import build_pipeline, run_query, run_rag
from src.output.citation import resolve_citations
from src.evaluation.queries import queries


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
        
        with st.status("Running Evaluation...", expanded=True) as status:
            results, metrics, docs, chunk_stats, debug_stats, errors = run_rag(
                queries=queries
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