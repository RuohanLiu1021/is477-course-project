#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

RAW_DIR = "data/raw"
OUT_DIR = "data/clean"

NOAA_FILES = {
    "tavg": f"{RAW_DIR}/climdiv-tmpcst-v1.0.0-20250905",
    "cdd":  f"{RAW_DIR}/climdiv-cddcst-v1.0.0-20250905",
    "hdd":  f"{RAW_DIR}/climdiv-hddcst-v1.0.0-20250905",
}

# Fixed-width layout from NOAA documentation
colspecs = [
    (0, 3), (3, 4), (4, 6), (6, 10),
    (10, 17), (17, 24), (24, 31), (31, 38),
    (38, 45), (45, 52), (52, 59), (59, 66),
    (66, 73), (73, 80), (80, 87), (87, 94)
]

names = [
    "state", "division", "element", "year",
    "jan","feb","mar","apr","may","jun",
    "jul","aug","sep","oct","nov","dec"
]

state_name_map = {
    1: "Alabama", 2: "Arizona", 3: "Arkansas", 4: "California",
    5: "Colorado", 6: "Connecticut", 7: "Delaware", 8: "Florida",
    9: "Georgia", 10: "Idaho", 11: "Illinois", 12: "Indiana",
    13: "Iowa", 14: "Kansas", 15: "Kentucky", 16: "Louisiana",
    17: "Maine", 18: "Maryland", 19: "Massachusetts", 20: "Michigan",
    21: "Minnesota", 22: "Mississippi", 23: "Missouri", 24: "Montana",
    25: "Nebraska", 26: "Nevada", 27: "New Hampshire", 28: "New Jersey",
    29: "New Mexico", 30: "New York", 31: "North Carolina", 32: "North Dakota",
    33: "Ohio", 34: "Oklahoma", 35: "Oregon", 36: "Pennsylvania",
    37: "Rhode Island", 38: "South Carolina", 39: "South Dakota",
    40: "Tennessee", 41: "Texas", 42: "Utah", 43: "Vermont", 44: "Virginia",
    45: "Washington", 46: "West Virginia", 47: "Wisconsin", 48: "Wyoming"
}

def load_climdiv(path):
    """Load a NOAA ClimDiv fixed-width file and reshape it to long format."""
    df = pd.read_fwf(path, colspecs=colspecs, names=names)

    # Only keep contiguous U.S. states (1–48) as defined in NOAA documentation
    df = df[(df["state"] >= 1) & (df["state"] <= 48)].copy()

    # Wide → long (month is still string)
    df = df.melt(
        id_vars=["state", "year"],
        value_vars=["jan","feb","mar","apr","may","jun",
                    "jul","aug","sep","oct","nov","dec"],
        var_name="month",
        value_name="value"
    )

    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    return df


def main():
    # Load and reshape each variable
    tavg = load_climdiv(NOAA_FILES["tavg"]).rename(columns={"value": "tavg"})
    cdd  = load_climdiv(NOAA_FILES["cdd"]).rename(columns={"value": "cdd"})
    hdd  = load_climdiv(NOAA_FILES["hdd"]).rename(columns={"value": "hdd"})

    # Merge tavg / cdd / hdd
    climate = (
        tavg.merge(cdd, on=["state", "year", "month"])
            .merge(hdd, on=["state", "year", "month"])
    )

    # Add state_name
    climate["state_name"] = climate["state"].map(state_name_map)

    # Keep only selected columns for quality checking
    df = climate[["state_name", "year", "month", "tavg", "cdd", "hdd"]].copy()

    # Replace NOAA missing value codes
    df["tavg"] = df["tavg"].replace(-99.9, np.nan)
    df["cdd"]  = df["cdd"].replace(-9999, np.nan)
    df["hdd"]  = df["hdd"].replace(-9999, np.nan)

    # Remove months where NOAA has not yet released values (2025 Sep–Dec)
    df_clean = df.dropna(subset=["tavg", "cdd", "hdd"]).copy()

    # Ensure output directory exists
    os.makedirs(OUT_DIR, exist_ok=True)

    # Save final cleaned dataset
    out_path = f"{OUT_DIR}/noaa_climate_clean.csv"
    df_clean.to_csv(out_path, index=False)

    print(f"[INFO] NOAA cleaned dataset saved to: {out_path}")
    print(f"[INFO] Final shape: {df_clean.shape}")


if __name__ == "__main__":
    main()
