#!/usr/bin/env python3

import os
import hashlib
import requests

# Configuration

BASE_URL = "https://www.ncei.noaa.gov/pub/data/cirs/climdiv/"
OUTPUT_DIR = "data/raw"
CHECKSUM_FILE = "checksums.txt"

# NOAA filenames you used in your notebook
NOAA_FILES = {
    "tavg": "climdiv-tmpcst-v1.0.0-20250905",
    "cdd":  "climdiv-cddcst-v1.0.0-20250905",
    "hdd":  "climdiv-hddcst-v1.0.0-20250905",
}

# Utility: Compute SHA-256 checksum

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# Download a single file

def download_file(url, output_path):
    print(f"[INFO] Downloading {url} ...")
    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError(
            f"Failed to download {url} (status {response.status_code})"
        )

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"[INFO] Saved → {output_path}")

# Update checksums.txt

def update_checksums(filename, sha256):
    """
    Appends or replaces the SHA-256 checksum entry for a file.
    """
    entry_prefix = filename + " "

    # Load existing lines except the one for this file
    if os.path.exists(CHECKSUM_FILE):
        with open(CHECKSUM_FILE, "r") as f:
            lines = [line for line in f if not line.startswith(entry_prefix)]
    else:
        lines = []

    # Add new entry
    lines.append(f"{filename} {sha256}\n")

    with open(CHECKSUM_FILE, "w") as f:
        f.writelines(lines)

    print(f"[INFO] Updated checksums → {CHECKSUM_FILE}")

# Main workflow

def main():
    # Ensure data/raw exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for key, fname in NOAA_FILES.items():
        url = BASE_URL + fname
        output_path = os.path.join(OUTPUT_DIR, fname)

        # If file already exists, skip re-downloading
        if os.path.exists(output_path):
            print(f"[INFO] File already exists: {output_path}")
            print("[INFO] Skipping download.")
        else:
            download_file(url, output_path)

        # Compute checksum
        sha = sha256sum(output_path)
        update_checksums(fname, sha)

    print("\n[INFO] NOAA data acquisition completed successfully.")

if __name__ == "__main__":
    main()
