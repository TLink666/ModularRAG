from datetime import datetime
from src.pipeline.prepare_pipeline import prepare_pipeline
from src.pipeline.batch_query import batch_query
from src.evaluation.chunk_stats import *
from src.evaluation.retrieval_stats import *
from src.evaluation.rag_metrics import *
from src.evaluation.gold_loader import *
from src.evaluation.experiment import *
from src.config import *

def run_rag(queries):

    model, docs, index, bm25 = prepare_pipeline()

    results = batch_query(
            queries,
            model,
            index,
            bm25,
            docs
        )

    chunk_stats = analyze_chunks(docs)

    retrieval_stats = analyze_retrieval(results)

    gold = load_gold(
        f"{EVA_DATA_DIR}/retrieval_gold.json"
    )

    hit_score = retrieval_hit(
        results,
        gold
    )

    metrics = {
        "retrieval_hit":hit_score,

        "avg_retrieval_score":
            retrieval_stats["avg_score"],
        "num_chunks":
            chunk_stats["num_chunks"]
    }

    time = datetime.now()

    save_dir = (
        f"{RESULT_DIR}/"
        f"{time:%Y%m%d_%H%M%S}"
    )

    save_experiment(
        config=export_config(),
        results=results,
        metrics=metrics,
        save_dir=save_dir
    )

    return docs, results, metrics, chunk_stats, retrieval_stats