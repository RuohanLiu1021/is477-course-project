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
    │   └── clean/          # Cleaned datasets derived from raw data and Integrated datasets used for analysis
    │
    │── scripts/
    │   ├── acquire_noaa.py     # NOAA Climate Division data acquisition
    │   ├── acquire_eia.py      # EIA retail electricity sales acquisition
    │   ├── clean_noaa.py       # Cleaning and reshaping NOAA datasets
    │   ├── clean_eia.py        # Cleaning and formatting EIA data
    │   └── integrate_noaa_eia.py  # Integration across datasets
    │   └── openrefine_history.json # OpenRefine operation history 
    │
    │── results/
    │   └── figures/             # Generated visualizations
    │
    │── checksums.txt           # SHA-256 checksums for data/raw files
    │── requirements.txt        # Python dependencies
    │── README.md               # Project documentation

This structure ensures clarity, reproducibility, and modularity throughout the workflow.

---



## References

National Centers for Environmental Information. (2023). *Climate Divisional Database (nClimDiv).*  
https://www.ncei.noaa.gov/pub/data/cirs/climdiv/

U.S. Energy Information Administration. (2023). *Electricity Data Browser – Retail Sales (API v2).*  
https://www.eia.gov/electricity/data/browser/

Python Software Foundation. (2023). *Python: Version 3.x.* https://www.python.org/

The pandas development team. (2023). *pandas: Python Data Analysis Library.* https://pandas.pydata.org/

Harris, C. et al. (2020). *Array programming with NumPy.* Nature. https://numpy.org/

Hunter, J. D. (2007). *Matplotlib: A 2D Graphics Environment.* https://matplotlib.org/

Waskom, M. (2021). *Seaborn: Statistical data visualization.* https://seaborn.pydata.org/

Reitz, K. (2023). *Requests: HTTP for Humans.* https://requests.readthedocs.io/

Köster, J., & Rahmann, S. (2012). *Snakemake—a scalable workflow engine.*  
https://snakemake.readthedocs.io/

DuckDB Authors. (2023). *DuckDB: An Embeddable Analytical Database.* https://duckdb.org/


