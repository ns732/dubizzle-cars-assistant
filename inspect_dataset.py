
import pandas as pd
from pathlib import Path

# Dataset location
DATASET_PATH = Path("data/Copy_of_sample_cars_dataset.xlsx")

def inspect_dataset():
    print("\n--- DUBIZZLE ASSISTANT: DATASET INSPECTION ---")

    # Check whether the file exists
    if not DATASET_PATH.exists():
        print("Dataset not found. Check the file location.")
        return

    # Load Excel dataset
    df = pd.read_excel(DATASET_PATH)

    # Basic information
    print("\n1. Dataset shape:")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\n2. Column names:")
    print(df.columns.tolist())

    print("\n3. First five records:")
    print(df.head().to_string())

    print("\n4. Missing values:")
    print(df.isnull().sum())

    print("\n5. Duplicate records:")
    print(df.duplicated().sum())

    print("\n6. Data types:")
    print(df.dtypes)


if __name__ == "__main__":
    inspect_dataset()
