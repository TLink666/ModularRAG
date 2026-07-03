from src.pipeline.run_rag import run_rag
from src.output.cli import print_result

queries = [
    "What do users prefer in AI systems?",
    "What transformed computers into household devices?",
    "Which brewing method uses pressure to produce concentrated flavor?",
    "Who invented quantum mechanics?"
]

if __name__ == "__main__":
    results, metrics, *_ = (
        run_rag(queries)
    )

    print()

    print("Finished")
    
    print()
    
    for result in results:
        print_result(result)

    print()

    print(metrics)
    
    