
from app.services.bm25_retrieval import BM25Retriever
from tests.test_queries import test_queries


def evaluate_retrieval():
    retriever = BM25Retriever()
    correct = 0
    total = 0

    for test in test_queries:
        query = test["query"]

        if test.get("manual_review"):
            print(f"REVIEW: {query}")
            continue

        total += 1

        results = retriever.search(
            query,
            make=test.get("expected_make"),
            model=test.get("expected_model"),
            min_year=test.get("expected_year"),
            max_year=test.get("expected_year"),
            limit=5
        )

        match_found = False

        for car in results:
            matches = True

            if "expected_make" in test:
                matches &= car["make"].casefold() == test["expected_make"]

            if "expected_model" in test:
                matches &= car["model"].casefold() == test["expected_model"]

            if "expected_year" in test:
                matches &= car["year"] == test["expected_year"]

            if matches:
                match_found = True
                break

        expected_match = test.get("expected_match", True)
        passed = match_found == expected_match

        if passed:
            correct += 1

        status = "PASS" if passed else "FAIL"
        print(f"{status}: {query}")

        if not passed:
            print("Top 5 results:")
            for car in results:
                print(
                    f"  {car['make']} {car['model']} "
                    f"({car['year']}) - {car['score']:.3f}"
                )

    if total:
        accuracy = correct / total * 100
        print(f"\nQuery success@5: {accuracy:.1f}% ({correct}/{total})")

    manual_count = sum(test.get("manual_review", False) for test in test_queries)
    print(f"Manual reviews required: {manual_count}")


if __name__ == "__main__":
    evaluate_retrieval()
