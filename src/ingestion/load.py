import json
from pathlib import Path

import pandas as pd
import os
from pathlib import Path

PROJECT_DIR = Path(
    os.getenv("PROJECT_DIR", "/opt/airflow")
)

RAW_DIR = PROJECT_DIR / "data/raw/products"
BRONZE_DIR = PROJECT_DIR / "data/bronze/products"


def json_to_parquet(input_file):
    
    try:
        with input_file.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON formatting detected: {e}")
    except FileNotFoundError:
        print("The target file could not be found.")


    products = data["products"]

    df = pd.DataFrame(products)

    output_dir = BRONZE_DIR / input_file.parent.name
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / input_file.with_suffix(".parquet").name

    df.to_parquet(output_file, index=False)

    print(f"Bronze data saved to: {output_file}")


def get_unprocessed_files():
    raw_files = sorted(RAW_DIR.glob("*/*.json"))

    unprocessed_files = []

    for raw_file in raw_files:
        bronze_file = (
            BRONZE_DIR
            / raw_file.parent.name
            / raw_file.with_suffix(".parquet").name
        )

        if not bronze_file.exists():
            unprocessed_files.append(raw_file)

    return unprocessed_files


if __name__ == "__main__":
    files_to_process = get_unprocessed_files()

    if not files_to_process:
        print("No new files to process.")
    else:
        print(f"Found {len(files_to_process)} new file(s).")

        for raw_file in files_to_process:
            print(f"Processing: {raw_file}")
            json_to_parquet(raw_file)