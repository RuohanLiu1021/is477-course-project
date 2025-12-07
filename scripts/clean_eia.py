import pandas as pd
import os

RAW_PATH = "data/raw/eia_retail_sales.csv"
OUT_PATH = "data/clean/eia_retail_sales_clean.csv"


def main():
    print("[INFO] Loading raw EIA dataset...")
    
    # Load raw CSV
    eia = pd.read_csv(RAW_PATH)

    # Step 1 — Drop customer fields (missing 28%)
    cols_drop_missing = ["customers", "customers-units"]

    # Step 2 — Drop metadata or constant columns
    cols_drop_meta = [
        "sectorid",        # always "ALL"
        "sectorName",      # always "all sectors"
        "sales-units",     # unit metadata
        "revenue-units",   # unit metadata
        "stateDescription" # duplicate information
    ]

    drop_cols = cols_drop_missing + cols_drop_meta

    print(f"[INFO] Dropping columns: {drop_cols}")

    eia_clean = eia.drop(columns=drop_cols).copy()

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    # Save cleaned file
    eia_clean.to_csv(OUT_PATH, index=False)

    print(f"[INFO] Cleaned EIA dataset saved to: {OUT_PATH}")
    print(f"[INFO] Final shape: {eia_clean.shape}")


if __name__ == "__main__":
    main()
