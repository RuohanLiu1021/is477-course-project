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

This section provides all steps needed for another user to reproduce your entire project workflow, from acquiring data to generating final results.

### Storage and organization
#### Project Directory Structure
Our project follows a standard reproducible research layout:

    is477-final-project/
    │── data/
    │   ├── raw/                        # Programmatically acquired raw datasets (NOAA, EIA)
    │   └── clean/                      # Cleaned datasets derived from raw data + integrated datasets
    │
    │── scripts/
    │   ├── acquire_noaa.py             # NOAA Climate Division data acquisition
    │   ├── acquire_eia.py              # EIA retail electricity sales acquisition
    │   ├── clean_noaa.py               # Cleaning and reshaping NOAA datasets
    │   ├── clean_eia.py                # Cleaning and formatting EIA data
    │   ├── integrate_noaa_eia.py       # Integration across datasets
    │   └── analysis_noaa_eia.py        # Automated analysis and figure generation
    │
    │── notebook/
    │   ├── clean_noaa.ipynb            # NOAA data cleaning workflow （with data quality analysis）
    │   ├── clean_eia.ipynb             # EIA data cleaning workflow （with data quality analysis）
    │   ├── integrate_noaa_eia.ipynb    # dataset integration
    │   └── analysis_noaa_eia.ipynb     # Climate–electricity analysis & figures
    │
    │── results/
    │   ├── corr_heatmap.png                # Correlation matrix visualization
    │   └── seasonal_temp_cdd_hdd_sales.png # Seasonal climate vs. sales trends
    │
    │── checksums.txt                   # SHA-256 checksums for data/raw files
    │── requirements.txt                # Python dependencies
    │── pip-freeze.txt                  # full dependency list
    │── run_all.sh                      # One-click reproducibility script (Snakemake wrapper)
    │── Snakefile                       # Full workflow automation
    │── README.md                       # Project documentation
    

This structure ensures clarity, reproducibility, and modularity throughout the workflow.

---
## Reproducibility and Transparency 

This section describes all components required to fully reproduce the project’s results, including environment setup, data acquisition, cleaning, integration, workflow automation, and final analysis outputs.

### 1. Environment and Dependencies
All required Python packages are listed in:
requirements.txt

Install them with:
pip install -r requirements.txt

It is recommended to create a virtual environment:
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
.\.venv\Scripts\activate         # Windows

### 2. Data Acquisition
All original data sources are public and can be automatically downloaded using the provided scripts.

Run:
python scripts/acquire_eia.py
python scripts/acquire_noaa.py

These scripts download:
- EIA state-level monthly electricity sales data
- NOAA temperature, CDD, and HDD climate data

Downloaded files will be stored in:
data/raw/

If automatic download is not possible, the README provides links and SHA-256 checksums so files can be manually placed into the same directory.

### 3. Data Cleaning
All data cleaning steps can be reproduced by running:

python scripts/clean_eia.py
python scripts/clean_noaa.py

These scripts perform:
- Missing value handling
- Column standardization
- Date formatting
- Output of cleaned CSV files into:

data/clean/

Corresponding explanatory notebooks:
notebook/clean_eia.ipynb
notebook/clean_noaa.ipynb

### 4. Data Integration
Run:
python scripts/integrate_noaa_eia.py

This script merges the cleaned EIA and NOAA datasets using state ID, year, and month.  
The resulting integrated dataset is saved to:
data/clean/noaa_eia_integrated.csv

Notebook version:
notebook/integrate_noaa_eia.ipynb

### 5. Analysis and Visualization
Run the analysis script:
python scripts/analysis_noaa_eia.py

This produces all project figures, including:
- Climate–electricity correlation matrix
- Seasonal temperature, CDD, HDD vs. electricity sales plots

All output files are saved in:
results/

Notebook version:
notebook/analysis_noaa_eia.ipynb

### 6. Workflow Automation (Snakemake)
To run the entire workflow end-to-end:

snakemake --cores 1

Or use the one-click script:
bash run_all.sh

These workflows reproduce:
data download -> cleaning -> integration -> analysis -> final results

All rules are defined in:
Snakefile

### 7. Reproducible Outputs
All generated outputs are stored in:
results/

Files include:
corr_heatmap.png
seasonal_temp_cdd_hdd_sales.png

### 8. Quick Reproduction Checklist
To reproduce the full project from scratch:

git clone https://github.com/RuohanLiu1021/is477-course-project
cd is477-course-project
pip install -r requirements.txt
bash run_all.sh

This will regenerate:
- All cleaned and integrated datasets
- All figures

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


