
from pathlib import Path
import pandas as pd
from bs4 import BeautifulSoup

from app.services.listing_details import ListingDetails


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = PROJECT_ROOT / "data" / "Copy_of_sample_cars_dataset.xlsx"

REQUIRED_COLUMNS = [
    "make", "model", "trim", "year", "title", "description", "photo_url",
]


class InventoryLoader:
    def __init__(self, dataset_path: Path = DATASET_PATH):
        self.dataset_path = dataset_path
        self.inventory = None

    def load_inventory(self) -> pd.DataFrame:
        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.dataset_path}"
            )

        df = pd.read_excel(self.dataset_path)

        missing_columns = [
            column for column in REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        df = df[REQUIRED_COLUMNS].copy()

        if df.empty:
            raise ValueError("The inventory dataset is empty.")

        for column in [
            "make", "model", "trim", "title", "description", "photo_url"
        ]:
            df[column] = (
                df[column].fillna("").astype(str).str.strip()
            )

        df["clean_description"] = df["description"].apply(self.clean_html)

        details = [
            ListingDetails.extract_details(
                row.title,
                row.clean_description
            )
            for row in df.itertuples()
        ]

        df["price_aed"] = [
            item["price_aed"] for item in details
        ]

        df["mileage_km"] = [
            item["mileage_km"] for item in details
        ]

        df["make_normalized"] = df["make"].str.casefold()
        df["model_normalized"] = df["model"].str.casefold()

        self.inventory = df.reset_index(drop=True)

        print(
            f"Successfully loaded {len(self.inventory)} car listings."
        )

        return self.inventory

    @staticmethod
    def clean_html(text: str) -> str:
        return BeautifulSoup(
            text, "html.parser"
        ).get_text(separator=" ", strip=True)


if __name__ == "__main__":
    loader = InventoryLoader()
    inventory = loader.load_inventory()

    print("\nFirst five listings:")

    print(
        inventory[
            ["make", "model", "year", "price_aed", "mileage_km"]
        ].head().to_string(index=False)
    )

    print("\nAvailable price values:")
    print(inventory["price_aed"].notna().sum())

    print("\nAvailable mileage values:")
    print(inventory["mileage_km"].notna().sum())
