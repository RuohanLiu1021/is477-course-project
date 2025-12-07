# is477-course-project
Course project for IS477  Fall 2025
# Project Title
**TODO: Add the title of your project here**

---

## Contributors
- Ruohan Liu (ruohanle)
- Yu Wan (wan27)

---

## Summary (500–1000 words)
**TODO: Write project background, motivation, research questions, datasets used, and high-level findings once analysis is completed.**

---

## Data Profile (500–1000 words)

### 1. NOAA Climate Division Data )


### 2. EIA Retail Electricity Sales Data


---

## Data Quality (500–1000 words)
**TODO: Write after cleaning and profiling. Suggested topics:**  

---

## Findings (~500 words)
**TODO: Add final analysis results, visualizations, and interpretation once analysis is complete.**

---

## Future Work (500–1000 words)
**TODO: Discuss model improvements, additional datasets, limitations, and future extensions.**

---
## Reproducing

This section provides all steps needed for another user (or the TA) to reproduce your entire project workflow, from acquiring data to generating final results.
### Data collection and acquisition

### Storage and organization
#### Project Directory Structure
Our project follows a standard reproducible research layout:

    is477-final-project/
    │── data/
    │   ├── raw/                # Programmatically acquired raw datasets (NOAA, EIA)
    │   ├── clean/              # Cleaned datasets derived from raw data
    │   └── processed/          # Integrated datasets used for analysis
    │
    │── scripts/
    │   ├── acquire_noaa.py     # NOAA Climate Division data acquisition
    │   ├── acquire_eia.py      # EIA retail electricity sales acquisition
    │   ├── clean_noaa.py       # Cleaning and reshaping NOAA datasets
    │   ├── clean_eia.py        # Cleaning and formatting EIA data
    │   └── integrate_noaa_eia.py  # Integration across datasets
    │
    │── results/
    │   ├── figures/            # Generated visualizations
    │   └── tables/             # Statistical summary tables
    │
    │── checksums.txt           # SHA-256 checksums for data/raw files
    │── requirements.txt        # Python dependencies
    │── README.md               # Project documentation

This structure ensures clarity, reproducibility, and modularity throughout the workflow.

---



## References
**TODO:** : Formatted citations for any papers, datasets, or software used in your project.

