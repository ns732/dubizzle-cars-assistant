
import re

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.inventory import InventoryLoader


class CarRetriever:

    SUV_MODELS = {
        "urban cruiser", "territory", "explorer", "cr-v",
        "x-trail", "patrol", "prado", "land cruiser",
        "rav4", "fortuner", "highlander", "tucson",
        "santa fe", "sportage", "sorento", "captiva",
        "cx-5", "xc60", "xc90", "q3", "q5", "q7", "q8",
        "gle-class", "glc-class", "gla-class", "gls-class",
        "range rover", "range rover sport", "range rover evoque",
        "discovery", "bentayga", "cullinan", "model x",
        "h9", "t-roc", "js4", "kicks", "edge", "yu7"
    }

    SEDAN_MODELS = {
        "corolla", "camry", "yaris", "altima", "maxima",
        "sunny", "c-class", "e-class", "a-class",
        "s-class", "3-series", "5-series", "7-series",
        "a3", "a4", "a6", "es-series", "cla-class",
        "cls-class", "model s", "han", "accent", "arrizo 5"
    }

    HATCHBACK_MODELS = {
        "golf", "mini cooper", "swift", "polo"
    }

    def __init__(self):
        self.inventory = InventoryLoader().load_inventory().copy()

        for column in ["year", "price_aed", "mileage_km"]:
            if column in self.inventory.columns:
                self.inventory[column] = pd.to_numeric(
                    self.inventory[column], errors="coerce"
                )

        text_columns = [
            "make_normalized",
            "model_normalized",
            "trim",
            "title",
            "clean_description"
        ]

        for column in text_columns:
            if column not in self.inventory.columns:
                self.inventory[column] = ""

            self.inventory[column] = (
                self.inventory[column].fillna("").astype(str)
            )

        self.inventory["search_text"] = (
            self.inventory["make_normalized"] + " " +
            self.inventory["model_normalized"] + " " +
            self.inventory["trim"].str.casefold() + " " +
            self.inventory["title"].str.casefold() + " " +
            self.inventory["clean_description"].str.casefold()
        )

        self.inventory["body_type"] = (
            self.inventory["model_normalized"]
            .apply(self.classify_body_type)
        )

        self.inventory = self.inventory.reset_index(drop=True)

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        self.car_vectors = self.vectorizer.fit_transform(
            self.inventory["search_text"]
        )

    @classmethod
    def classify_body_type(cls, model):
        model = str(model).casefold().strip()

        if model in cls.SUV_MODELS:
            return "SUV"

        if model in cls.SEDAN_MODELS:
            return "Sedan"

        if model in cls.HATCHBACK_MODELS:
            return "Hatchback"

        return None

    def search(
        self,
        query,
        make=None,
        model=None,
        min_year=None,
        max_year=None,
        min_price=None,
        max_price=None,
        min_mileage=None,
        max_mileage=None,
        body_type=None,
        fuel_type=None,
        transmission=None,
        limit=100
    ):

        results = self.inventory.copy()

        # Make filter
        if make:
            results = results[
                results["make_normalized"].str.contains(
                    re.escape(str(make).strip()),
                    case=False,
                    regex=True,
                    na=False
                )
            ]

        # Flexible model matching across model, trim and listing text
        if model:
            model_pattern = re.escape(str(model).strip())

            searchable_model = (
                results["model_normalized"].fillna("").astype(str) + " " +
                results["trim"].fillna("").astype(str) + " " +
                results["title"].fillna("").astype(str) + " " +
                results["clean_description"].fillna("").astype(str)
            )

            results = results[
                searchable_model.str.contains(
                    rf"(?<![a-zA-Z0-9]){model_pattern}(?![a-zA-Z0-9])",
                    case=False,
                    regex=True,
                    na=False
                )
            ]

        # Year filters
        if min_year is not None:
            results = results[
                results["year"] >= float(min_year)
            ]

        if max_year is not None:
            results = results[
                results["year"] <= float(max_year)
            ]

        # Price filters
        if min_price is not None:
            results = results[
                results["price_aed"].notna() &
                (results["price_aed"] >= float(min_price))
            ]

        if max_price is not None:
            results = results[
                results["price_aed"].notna() &
                (results["price_aed"] <= float(max_price))
            ]

        # Mileage filters
        if min_mileage is not None:
            results = results[
                results["mileage_km"].notna() &
                (results["mileage_km"] >= float(min_mileage))
            ]

        if max_mileage is not None:
            results = results[
                results["mileage_km"].notna() &
                (results["mileage_km"] <= float(max_mileage))
            ]

        # Body type
        if body_type:
            results = results[
                results["body_type"].str.casefold()
                == str(body_type).casefold()
            ]

        # Fuel type
        if fuel_type:
            results = results[
                results["clean_description"].str.contains(
                    re.escape(str(fuel_type)),
                    case=False,
                    regex=True,
                    na=False
                )
            ]

        # Transmission
        if transmission:
            results = results[
                results["clean_description"].str.contains(
                    re.escape(str(transmission)),
                    case=False,
                    regex=True,
                    na=False
                )
            ]

        if results.empty:
            return []

        # Rank only listings that passed the structured filters
        query_vector = self.vectorizer.transform([str(query)])

        scores = cosine_similarity(
            query_vector,
            self.car_vectors[results.index]
        ).flatten()

        results = results.copy()
        results["score"] = scores

        results = results.sort_values(
            "score",
            ascending=False,
            kind="stable"
        )

        output_columns = [
            "make", "model", "trim", "year", "title",
            "description", "photo_url", "price_aed",
            "mileage_km", "score"
        ]

        available_columns = [
            column for column in output_columns
            if column in results.columns
        ]

        limit = max(1, int(limit))

        return results.head(limit)[available_columns].to_dict(
            orient="records"
        )


if __name__ == "__main__":

    retriever = CarRetriever()

    cars = retriever.search(
        query="BMW M2 under AED 250000",
        make="BMW",
        model="M2",
        max_price=250000,
        limit=100
    )

    print(f"\nMatching cars: {len(cars)}")

    for car in cars:
        print(
            f"{car.get('make')} {car.get('model')} "
            f"({car.get('year')}) | "
            f"Price: {car.get('price_aed')} | "
            f"Mileage: {car.get('mileage_km')}"
        )
