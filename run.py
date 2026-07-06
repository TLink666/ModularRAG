import src.env
import time
from src.pipeline.run_rag import run_rag
from src.output.cli import print_result
from src.evaluation.queries import queries

if __name__ == "__main__":

    start = time.perf_counter()

    results, metrics, *_ = run_rag(queries)

    elapsed = time.perf_counter() - start

    print(f"\nFinished in {elapsed:.2f}s\n")

    for result in results:
        print_result(result)

    print(metrics)
    
    