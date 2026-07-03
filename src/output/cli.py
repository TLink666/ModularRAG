from src.output.citation import resolve_citations

def print_result(result):

    print("\n===================")

    print("\nQuestion:")
    print(result["query"])

    print("\n=== Answer ===")
    print(result["answer"])

    citations = resolve_citations(
        result["answer"],
        result["retrieved"]
    )

    if citations:
        print("\n=== Citations ===")
        for c in citations:
            if c["page"] is None:
                print(
                    f'[{c["citation"]}] {c["source"]}'
                )
            else:
                print(
                    f'[{c["citation"]}] '
                    f'{c["source"]} '
                    f'Page {c["page"]}'
                )