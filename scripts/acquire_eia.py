#!/usr/bin/env python3

import os
import hashlib
import requests
import pandas as pd

# Configuration

OUTPUT_DIR = "data/raw"
OUTPUT_FILE = "eia_retail_sales.csv"
CHECKSUM_FILE = "checksums.txt"

API_KEY = os.environ.get("EIA_API_KEY")   # ← 从环境变量读取 API KEY

if API_KEY is None or API_KEY.strip() == "":
    raise RuntimeError(
        "EIA_API_KEY not found. Please set it as an environment variable:\n"
        "  export EIA_API_KEY='your_api_key_here'"
    )

BASE_URL = f"https://api.eia.gov/v2/electricity/retail-sales/data/?api_key={API_KEY}"

STATES = [
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS",
    "KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY",
    "NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV",
    "WI","WY","DC"
]

PAYLOAD_BASE = {
    "frequency": "monthly",
    "data": ["sales", "customers", "revenue"],
    "facets": {
        "stateid": STATES,
        "sectorid": ["ALL"]
    },
    "sort": [{"column": "period", "direction": "asc"}],
    "length": 5000,
}

# Utility: SHA-256 Checksum

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def update_checksums(filename, sha256):
    """
    Append or replace checksum entry in checksums.txt
    """
    prefix = filename + " "

    if os.path.exists(CHECKSUM_FILE):
        with open(CHECKSUM_FILE, "r") as f:
            lines = [line for line in f if not line.startswith(prefix)]
    else:
        lines = []

    lines.append(f"{filename} {sha256}\n")

    with open(CHECKSUM_FILE, "w") as f:
        f.writelines(lines)

    print(f"[INFO] Updated checksums → {CHECKSUM_FILE}")


# Main download logic
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    all_rows = []
    offset = 0

    print("[INFO] Fetching EIA retail sales data...")

    while True:
        payload = PAYLOAD_BASE.copy()
        payload["offset"] = offset

        response = requests.post(BASE_URL, json=payload).json()

        # No more data
        if ("response" not in response) or (len(response["response"]["data"]) == 0):
            break

        rows = response["response"]["data"]
        all_rows.extend(rows)
        offset += 5000

        print(f"[INFO] Fetched {len(all_rows)} rows so far...")

    # Convert to DataFrame
    df = pd.DataFrame(all_rows)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    df.to_csv(output_path, index=False)

    print(f"[INFO] Saved → {output_path}")

    # Compute checksum
    sha = sha256sum(output_path)
    update_checksums(OUTPUT_FILE, sha)

    print("\n[INFO] EIA data acquisition completed successfully.")


if __name__ == "__main__":
    main()
