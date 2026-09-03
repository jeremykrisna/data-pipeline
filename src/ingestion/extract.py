import json
from datetime import datetime
from pathlib import Path

import pendulum
from api_client import fetch_products

RAW_DIR = Path("data/raw/products")
local_tz = pendulum.timezone("Asia/Jakarta")


def save_raw_data(data):
    timestamp = datetime.now(local_tz)

    # Folder base on date
    output_dir = RAW_DIR / timestamp.strftime("%Y-%m-%d")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Filename based on time ingestion
    output_file = output_dir / (
        f"products_{timestamp.strftime('%H%M%S')}.json"
    )

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)
    print(f"Raw snapshot saved to: {output_file}")

if __name__ == "__main__":
    data = fetch_products()
    save_raw_data(data)