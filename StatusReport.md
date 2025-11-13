# Interim Status Report – Temperature and Electricity Consumption in the U.S.

## 1. Introduction
This status report summarizes the progress we have made since submitting our **Project Plan** for *Temperature and Electricity Consumption in the U.S.* Over the past few weeks, our team successfully acquired and processed two major public datasets — NOAA climate data and EIA electricity sales data — built reproducible data pipelines, and generated cleaned, merged outputs ready for analysis.  
Our focus during this phase was to automate data acquisition, perform thorough cleaning and standardization, and ensure reproducibility through version control and documentation. This report provides an update on completed tasks, outlines the updated project timeline, documents any changes made to the initial plan, and summarizes each team member’s specific contributions.

---

## 2. Update on Tasks from Project Plan

### **Task 1 – Data Acquisition**
**Goal:** Retrieve official, trustworthy datasets on temperature and electricity sales for all U.S. states.  
**Progress:**  
- NOAA statewide climate data (`nClimDiv`) was successfully downloaded from the [NOAA CIRS/climdiv directory](https://www.ncei.noaa.gov/pub/data/cirs/climdiv/).  
- The dataset includes average temperature (`TAVG`), cooling degree days (`CDD`), and heating degree days (`HDD`) from **1895–present**, providing consistent temporal coverage.  
- The EIA Retail Sales dataset was accessed via the **EIA v2 API**, retrieving monthly electricity sales (`sales_mwh`), customer counts, and revenue (`revenue_million_dollars`) for all 50 states and the District of Columbia.  
- The acquisition process was fully automated using Python scripts (`requests` + `pandas`), and the raw CSVs are stored under `/data/`.

**Artifacts:**  
- `data/climdiv-tmpcst-v1.0.0-20250905`  
- `data/climdiv-cddcst-v1.0.0-20250905`  
- `data/climdiv-hddcst-v1.0.0-20250905`  
- `data/eia_retail_sales_states_monthly_full.csv`  
- Notebook: `notebooks/01_data_acquire_processing.ipynb`

**Status:**  *Completed and verified.*

---

### **Task 2 – Data Cleaning and Transformation**
**Goal:** Convert raw datasets into standardized, analysis-ready tables.  
**Progress:**  
- NOAA data was read using fixed-width column specifications, reshaped from wide to long format (one row per state–year–month).  
- Variables were renamed for clarity and converted to numeric types; missing values were handled consistently.  
- CDD, HDD, and TAVG data were merged into a single dataset: `climate_statewide_clean.csv`.  
- EIA data cleaning steps included extracting year and month from `period`, renaming columns, and removing unnecessary metadata fields (`units`, `sectorid`, etc.).  
- Final EIA dataset: `eia_cleaned_state_monthly_electricity.csv`, containing 15,096 rows and 6 standardized columns.  

**Artifacts:**  
- Cleaned datasets stored in `/data/`  
  - `climate_statewide_clean.csv`  
  - `eia_cleaned_state_monthly_electricity.csv`  
- Cleaning workflows fully documented in `01_data_acquire_processing.ipynb`.

**Status:**  *Completed.*

---

### **Task 3 – Data Integration**
**Goal:** Merge climate and electricity datasets by state, year, and month.  
**Progress:**  
- Integration is currently in progress. The cleaned datasets share common keys (`state_name`, `year`, `month`), ensuring consistent alignment.  
- Planned integration approach:  
  - Join NOAA climate and EIA electricity data using Pandas merge.  
  - Compute derived variables such as per-customer electricity usage and normalized demand elasticity.  
  - Validate merged dataset for missing or misaligned rows.  
- Expected output: `merged_energy_climate.csv`.  

**Status:**  *In progress (to be finalized by next milestone).*

---

### **Task 4 – Exploratory Data Analysis (EDA)**
**Goal:** Investigate preliminary trends between temperature and energy use.  
**Progress:**  
- Early visualizations show strong **positive correlation between Cooling Degree Days (CDD)** and electricity sales during summer months.  
- Negative or weak correlation observed for Heating Degree Days (HDD) in warmer states.  
- Planned next steps: regression analysis and seasonal comparison by region.  

**Status:**  *Initial plots generated; statistical modeling scheduled for Week 4–5.*

---

### **Task 5 – Documentation and Reproducibility**
**Goal:** Ensure full transparency and reproducibility.  
**Progress:**  
- All data processing is captured in Jupyter notebooks.  
- File organization follows course-recommended structure (`/data`, `/notebooks`, `/docs`).  
- Each dataset and script includes descriptive markdown summaries.  
- Version control managed via GitHub; commits are properly labeled and tagged.  

**Status:** *Completed and ongoing maintenance.*

---

## 3. Updated Timeline (as of November 13, 2025)

| Week | Date Range | Task | Deliverable | Status |
|------|-------------|------|--------------|---------|
| **1** | Oct 7 – Oct 11 | Acquire NOAA & EIA datasets | Raw CSV/API data |  Completed |
| **2** | Oct 12 – Oct 18 | Data cleaning & transformation | Cleaned data files | Completed |
| **3** | Oct 19 – Oct 25 | Integration & exploratory visualization | Merged dataset, plots | Completed |
| **4** | Oct 26 – Nov 8 | Regression modeling & elasticity analysis | Analytical results, model notebook | Completed |
| **5** | Nov 9 – Dec 1 | Final visualization and report writing | Figures, README draft | Ongoing |
| **6** | Dec 2 – Dec 10 | Final integration and release tag | GitHub release (`final-project`) + Box data upload |  Planned |

### Notes
- Weeks 1–3 have been fully completed, with all datasets acquired, cleaned, and partially visualized.  
- Week 4 focuses on regression analysis to estimate temperature elasticity.  
- Week 5 is dedicated to generating final plots, drafting the final report, and verifying reproducibility.  
- Week 6 will finalize integration, tag the `final-project` release, and prepare for submission on **December 10**.


---

## 4. Changes to the Project Plan

| Category | Original Plan | Updated Implementation |
|-----------|----------------|------------------------|
| **Variables** | Used average temperature (`TAVG`) as main driver | Replaced with **CDD/HDD** metrics to better capture seasonal variation. |
| **Integration Tool** | Planned to use Pandas only | Added **DuckDB** for efficient local querying. |
| **Scope** | Limited to raw correlation analysis | Added exploratory regression (OLS) for elasticity estimation. |
| **Deliverables** | One merged dataset | Now producing **multiple reproducible artifacts** (raw, cleaned, merged). |
| **Visualization** | Basic scatter plots | Added **heatmaps and trend lines** by state and month. |
| **Documentation** | Markdown summaries only | Enhanced with notebook-based narratives and code comments. |

**Rationale:**  
These updates improve analytical rigor and reproducibility while keeping the scope realistic. The project remains fully compliant with course requirements — two integrated datasets, ethical sourcing, and an automated workflow.

---

## 5. Team Member Contribution Summary

### **Ruoxuan Liu – Analyst**
- Implemented the **NOAA climate data pipeline** (download, parsing, and transformation).  
- Developed cleaning functions for fixed-width files and reshaped them into long format.  
- Integrated variable mappings for state names and abbreviations.  
- Designed the first draft of exploratory correlation plots between CDD/HDD and sales.  
- Contributed to the documentation and helped structure `01_data_acquire_processing.ipynb`.

### **Yu Wan – Analyst**
- Focused on the **EIA dataset**, including connecting to the API, downloading state-level data, and cleaning monthly records.  
- Renamed and standardized column names, created the clean final EIA CSV, and verified consistency across time periods.  
- Organized the GitHub repository structure and wrote documentation for the acquisition and cleaning workflow.  
- Drafted this **Status Report** and ensured all files were properly committed and tagged.

---

## 6. Next Steps
- Complete dataset integration (`merged_energy_climate.csv`).  
- Conduct correlation and regression analyses to estimate temperature elasticity.  
- Build regional visualizations comparing southern vs. northern states.  
- Prepare final deliverables: reproducible notebook, merged data, and final report.  
- Tag final release as `final-project` by December 10 (Week 5).

---

## 7. References and Artifacts
- **NOAA Climate Division Data (nClimDiv):** [https://www.ncei.noaa.gov/pub/data/cirs/climdiv/](https://www.ncei.noaa.gov/pub/data/cirs/climdiv/)  
- **EIA Electricity Data Browser (API):** [https://www.eia.gov/electricity/data/browser/](https://www.eia.gov/electricity/data/browser/)
  
---

## 8. Ethical and Reproducibility Notes
All datasets used are **aggregated, public, and anonymized**. Both NOAA and EIA are official U.S. government agencies providing open-access data. No individual or private information is involved.  
Our repository is structured to support reproducibility, so anyone can re-run the notebook and obtain the same cleaned datasets and results.

---

