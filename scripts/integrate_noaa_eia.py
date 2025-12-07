#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

NOAA_PATH = os.path.join(ROOT_DIR, "data/clean/noaa_climate_clean.csv")
EIA_PATH = os.path.join(ROOT_DIR, "data/clean/eia_retail_sales_clean.csv")
OUTPUT_PATH = os.path.join(ROOT_DIR, "data/clean/noaa_eia_integrated.csv")

noaa = pd.read_csv(NOAA_PATH)
eia = pd.read_csv(EIA_PATH)

if "period" in eia.columns:
    eia[["year", "month"]] = eia["period"].str.split("-", expand=True)
    eia["year"] = eia["year"].astype(int)
    eia["month"] = eia["month"].astype(int)

month_map = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "may": 5, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12
}
if noaa["month"].dtype == object:
    noaa["month"] = noaa["month"].map(month_map)

state_abbrev_map = {
    "Alabama": "AL", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL",
    "Georgia": "GA", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN",
    "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
    "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
    "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

noaa["stateid"] = noaa["state_name"].map(state_abbrev_map)

min_eia_year = eia["year"].min()
noaa = noaa[noaa["year"] >= min_eia_year].copy()

integrated = noaa.merge(
    eia,
    on=["stateid", "year", "month"],
    how="inner"
)

if "period" in integrated.columns:
    integrated = integrated.drop(columns=["period"])

cols = [
    "year", "month", "stateid", "state_name",
    "tavg", "cdd", "hdd",
    "sales", "revenue"
]
integrated = integrated[cols]

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
integrated.to_csv(OUTPUT_PATH, index=False)

print("[INFO] Integrated saved:", OUTPUT_PATH)
print("[INFO] Final shape:", integrated.shape)
