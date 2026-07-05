def print_errors(errors):

    print("\n=== Retrieval Errors ===")

    if not errors:
        print("No errors 🎉")
        return

    for i, e in enumerate(errors, 1):

        print("\n----------------------")
        print(f"[{i}] Query:")
        print(e["query"])

        print("\nGold Source:")
        print(e["gold"]["source"])
        if "anchor" in e["gold"]:
            print(f"Anchor: {e['gold']['anchor']}")

        print("\nFailure Type:")
        print(e["type"])

        print("\nGold Rank:")
        print(e["gold_rank"])

        print("\nTop Retrieved:")

        for r in e["retrieved"][:5]:

            print(
                f"  Rank {r['rank']} | "
                f"{r['source']} | "
                f"Score {r['score']:.3f}"
            )