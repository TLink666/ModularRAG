from src.pipeline.prepare_pipeline import prepare_pipeline
from src.pipeline.batch_query import batch_query
from src.evaluation.chunk_stats import analyze_chunks
from src.evaluation.retrieval_debug import retrieval_debug_stats
from src.evaluation.gold_loader import load_gold
from src.evaluation.compute_metrics import compute_metrics
from src.evaluation.retrieval_analysis import analyze_retrieval_errors
from src.experiment.save_experiment import save_experiment
import src.config as config

def build_pipeline():
    model, docs, index, bm25 = prepare_pipeline()

    return {
        "model": model,
        "docs": docs,
        "index": index,
        "bm25": bm25
    }
    
def run_query(query, pipeline):

    results = batch_query(
        [query],
        pipeline["model"],
        pipeline["index"],
        pipeline["bm25"],
        pipeline["docs"]
    )

    return results[0]

def run_queries(queries, pipeline):

    return batch_query(
        queries,
        pipeline["model"],
        pipeline["index"],
        pipeline["bm25"],
        pipeline["docs"]
    )
    
def evaluate(results, docs):

    gold = load_gold(f"{config.EVA_DATA_DIR}/retrieval_gold.json")

    chunk_stats = analyze_chunks(docs)

    debug_stats = retrieval_debug_stats(results)

    errors = analyze_retrieval_errors(results, gold)

    metrics = compute_metrics(results, gold, chunk_stats, errors)

    return metrics, chunk_stats, debug_stats, errors

def run_rag(queries):

    pipeline = build_pipeline()

    results = run_queries(queries, pipeline)

    metrics, chunk_stats, debug_stats, errors = evaluate(
        results,
        pipeline["docs"]
    )

    save_experiment(
        configuration=config.export_config(),
        results=results,
        metrics=metrics,
        debug_stats=debug_stats
    )

    return results, metrics, pipeline["docs"], chunk_stats, debug_stats, errors