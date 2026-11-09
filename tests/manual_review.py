from app.services.retrieval import CarRetriever
from app.services.bm25_retrieval import BM25Retriever

queries = [
    "Find an SUV suitable for family trips",
    "Find a car for daily commuting",
    "Show me a luxury car",
    "Find cars under AED 100000",
    "Show me cars with less than 50000 km",
]


def review_searches(retriever, method):
    print(f"\n{'=' * 50}")
    print(f"{method} RESULTS")
    print("=" * 50)

    for query in queries:
        print(f"\nQuery: {query}")

        results = retriever.search(query, limit=5)

        if not results:
            print("No results found.")
            continue

        for car in results:
            print(
                f"{car['year']} {car['make']} {car['model']} "
                f"- Score: {car['score']:.3f}"
            )


if __name__ == "__main__":
    review_searches(CarRetriever(), "TF-IDF")
    review_searches(BM25Retriever(), "BM25")