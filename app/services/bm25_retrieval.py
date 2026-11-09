
import re
import pandas as pd
from rank_bm25 import BM25Okapi
from app.services.inventory import InventoryLoader


class BM25Retriever:
    def __init__(self):
        self.inventory = InventoryLoader().load_inventory()

        self.inventory["search_text"] = (
            self.inventory["make_normalized"] + " " +
            self.inventory["model_normalized"] + " " +
            self.inventory["trim"].str.casefold() + " " +
            self.inventory["year"].astype(str) + " " +
            self.inventory["title"].str.casefold() + " " +
            self.inventory["clean_description"].str.casefold()
        )

        self.tokenized_corpus = [
            self.tokenize(text)
            for text in self.inventory["search_text"]
        ]

        self.bm25 = BM25Okapi(self.tokenized_corpus)

    @staticmethod
    def tokenize(text):
        return re.findall(r"\b[\w-]+\b", text.casefold())

    def search(self, query, make=None, model=None, min_year=None, max_year=None, limit=5):
        query_tokens = self.tokenize(query)
        scores = self.bm25.get_scores(query_tokens)

        results = self.inventory.copy()
        results["score"] = scores

        if make:
            results = results[
                results["make_normalized"].str.contains(
                    re.escape(make.strip().casefold()), regex=True
                )
            ]

        if model:
            results = results[
                results["model_normalized"].str.contains(
                    re.escape(model.strip().casefold()), regex=True
                )
            ]

        if min_year is not None:
            results = results[results["year"] >= min_year]

        if max_year is not None:
            results = results[results["year"] <= max_year]

        results = results.sort_values("score", ascending=False)

        columns = [
            "make", "model", "trim", "year",
            "title", "description", "photo_url", "score"
        ]

        return results.head(limit)[columns].to_dict(orient="records")


if __name__ == "__main__":
    retriever = BM25Retriever()
    cars = retriever.search("Toyota SUV", limit=5)

    for car in cars:
        print(
            f"{car['year']} {car['make']} {car['model']} "
            f"- Score: {car['score']:.3f}"
        )
