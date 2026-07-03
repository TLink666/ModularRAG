from src.pipeline.prepare_pipeline import prepare_pipeline
from src.pipeline.batch_query import batch_query
from src.evaluation.chunk_stats import analyze_chunks
from src.evaluation.retrieval_debug import retrieval_debug_stats
from src.evaluation.gold_loader import load_gold
from src.evaluation.compute_metrics import compute_metrics
from src.evaluation.retrieval_analysis import analyze_retrieval_errors
from src.experiment.save_experiment import save_experiment
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

    gold = load_gold(
        f"{EVA_DATA_DIR}/retrieval_gold.json"
    )

    chunk_stats = analyze_chunks(docs)

    debug_stats = retrieval_debug_stats(results)
    
    errors = analyze_retrieval_errors(results, gold)

    metrics = compute_metrics(results, gold, chunk_stats, errors)
    
    save_experiment(
        config=export_config(),
        results=results,
        metrics=metrics,
        debug_stats=debug_stats
    )

    return results, metrics, docs, chunk_stats, debug_stats, errors