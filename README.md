# Climate, Heat, and Power: Linking NOAA Climate Divisions with EIA State Electricity Sales

Course project for IS477 · Fall 2025  

## Contributors
- Ruohan Liu (ruohanl3)
- Yu Wan (wan27)

---

## Summary (500–1000 words)

This project examines how climate conditions relate to state-level electricity demand in the United States by integrating two large public data sources: NOAA’s Climate Divisional Database (nClimDiv) and the U.S. Energy Information Administration’s (EIA) state-level retail electricity sales data. Our goal is to build a fully reproducible workflow—from acquisition to analysis—that demonstrates good data curation practices while answering substantive questions about how temperature and degree days shape electricity consumption.

We focus on the following research questions:

1. **How strongly are climate indicators (average temperature, cooling degree days, heating degree days) correlated with electricity sales and revenue across U.S. states?**  
2. **What seasonal patterns emerge when comparing temperature, degree days, and electricity sales over the course of a year?**  
3. **How does electricity demand vary geographically across states when averaged over time?**

To answer these questions, we acquire monthly climate indicators from **NOAA nClimDiv** for the 48 contiguous U.S. states and monthly retail electricity sales from **EIA** for all U.S. states and sectors. We then clean each dataset separately, harmonize identifiers and time fields, and integrate them into a single panel dataset at the granularity of **state × year × month**. The integrated dataset covers **January 2001 through August 2025** for the 48 contiguous states.

Data cleaning is implemented in both **scripts** (`scripts/clean_noaa.py`, `scripts/clean_eia.py`) and **notebooks** (`notebook/clean_noaa.ipynb`, `notebook/clean_eia.ipynb`). For NOAA, we parse fixed-width ClimDiv text files using official column specifications, convert monthly columns to a tidy long format, and handle special missing-value codes (–99.9, –9999). For EIA, we drop non-essential metadata fields, remove a heavily missing `customers` column, and verify that sales and revenue are non-negative and within reasonable ranges. We then normalize dates, map NOAA state names to EIA state abbreviations, and perform an inner join on `(stateid, year, month)` in `integrate_noaa_eia.py`.

Our analysis notebook (`notebook/analysis_noaa_eia.ipynb`) addresses the research questions using three main views of the integrated data:

- A **correlation matrix** between climate variables (TAVG, CDD, HDD) and electricity metrics (sales, revenue), visualized as a heatmap.
- **Seasonal line plots** that overlay monthly average temperature, cooling degree days, and heating degree days against average monthly sales, using dual y-axes.
- A **choropleth map** of average state-level electricity sales across the contiguous U.S.

The correlation analysis shows that climate variables are clearly related to electricity consumption, but the linear relationships are modest (correlations around 0.22–0.31). Seasonal plots reveal a strong U-shaped pattern: electricity sales peak in hot summer months (high CDD) and also rise in cold winter months (high HDD), with summer cooling being the stronger driver. The choropleth visualization highlights large differences in average consumption across states, with Texas and California among the highest, reflecting both population and climate.

From a curation standpoint, the project demonstrates end-to-end reproducibility. All acquisition, cleaning, and integration steps are automated through Python scripts and orchestrated using a **Snakemake** workflow and `run_all.sh`. We include OpenRefine history, checksums, and environment metadata so that others can inspect our decisions, verify data integrity, and re-run the entire workflow from raw downloads to final figures.

Overall, the project shows that climate is an important but not exclusive determinant of electricity demand: climate variables explain part of the variation, but population size, economic activity, infrastructure, and energy prices also matter. The workflow and integrated dataset provide a foundation for future modeling work, such as forecasting or regional policy analysis, while satisfying the IS477 requirements for transparency and reproducibility.

---

## Data Profile (500–1000 words)

### 1. NOAA Climate Division Data (nClimDiv)

**Source and access.**  
We use the **NOAA Climate Divisional Database (nClimDiv)** provided by the National Centers for Environmental Information (NCEI). The raw data files are downloaded as fixed-width text files and stored under:

- `data/raw/climdiv-tmpcst-v1.0.0-20250905` – statewide **average temperature** (TAVG)
- `data/raw/climdiv-cddcst-v1.0.0-20250905` – **cooling degree days** (CDD)
- `data/raw/climdiv-hddcst-v1.0.0-20250905` – **heating degree days** (HDD)

These are official products distributed by a U.S. federal agency, so they are generally usable for research and educational purposes as long as NOAA is cited as the data provider. No personally identifiable information (PII) is contained in the data.

**Original structure.**  
Each ClimDiv file is a fixed-width text file where each row contains one year of monthly climate observations for a specific **state climate division**. According to the official specification, the first fields encode:

- `state` – numeric NOAA state code  
- `division` – climate division code  
- `element` – climate element (e.g., temperature)  
- `year` – four-digit year  

followed by twelve fixed-width fields for **Jan–Dec** values.

In `notebook/clean_noaa.ipynb`, we read these files using `pandas.read_fwf()` with the official `colspecs` and `names`, ensuring correct parsing of all fields.

**Filtering and reshaping.**  
We restrict the dataset to the **48 contiguous U.S. states** by keeping only rows where `state` is between 1 and 48. We then reshape from wide to long format:

- Identifier variables: `state`, `year`
- Monthly value columns: `jan, …, dec`
- Long format columns: `year`, `month`, `value`

For each file, we apply the same cleaning function and then rename `value` to `tavg`, `cdd`, or `hdd`. We merge the three long tables on `(state, year, month)` to obtain a consolidated climate table with three climate indicators.

**Variables and coverage.**

The resulting tidy dataset (`noaa_climate_clean.csv`) contains:

- `state_name` – full state name (mapped from numeric codes)
- `year` – 1895–2025
- `month` – 1–12
- `tavg` – average temperature in °F
- `cdd` – cooling degree days
- `hdd` – heating degree days

After handling missing values (see Data Quality), the final climate dataset includes **75,264** complete monthly records for the 48 contiguous states, with full coverage through August 2025. Climate values for September–December 2025 are not yet available and remain missing in the original NOAA product.

**Ethical / legal considerations.**  
The NOAA data are aggregated climate indicators at state level and contain no individual-level or sensitive information. We simply respect NOAA’s citation requirements and do not attempt to redistribute proprietary derivatives.

---

### 2. EIA Retail Electricity Sales Data

**Source and access.**  
We use state-level monthly retail electricity sales from the **U.S. Energy Information Administration (EIA)**, obtained via the EIA API and stored as `data/raw/eia_retail_sales.csv`. The dataset covers **all sectors, all states**, and includes monthly kilowatt-hour sales, customer counts, and revenue. The raw data correspond to the EIA “Electricity Data Browser – Retail Sales” series.

The EIA data are also U.S. government data, usable for educational and research purposes with appropriate citation. There is no PII: all observations are aggregated at the **state × month** level.

**Original structure and fields.**  
The raw CSV, as inspected in `notebook/clean_eia.ipynb`, has 15,147 rows and 11 columns:

- `period` – year-month string (`YYYY-MM`)
- `stateid` – two-letter state abbreviation
- `stateDescription` – state name
- `sectorid` – sector code (e.g., `ALL`)
- `sectorName` – sector label (e.g., `all sectors`)
- `sales` – retail electricity sales (million kWh)
- `customers` – number of customers
- `revenue` – revenue (million dollars)
- `sales-units`, `customers-units`, `revenue-units` – unit description strings

For our analysis we only use **all sectors combined**, so `sectorid` and `sectorName` are constant.

**Cleaning and selection.**  
We perform several steps in `clean_eia.ipynb`:

1. **Missingness:** Only the `customers` column has missing values (4,284 rows, ~28%). Because our analysis focuses on sales and revenue and we do not need customer counts, we **drop `customers` and `customers-units`** instead of attempting imputation.

2. **Redundant fields:** We drop metadata and constant columns (`sectorid`, `sectorName`, `stateDescription`, `sales-units`, `revenue-units`), keeping only the analytical fields.

3. **Quality checks:**  
   - All remaining numerical columns (`sales`, `revenue`) have **no missing values**.  
   - There are **no negative or zero values**, and the distributions look reasonable (e.g., highest revenues for California and Texas).  
   - An IQR-based outlier check flags high-revenue observations, but domain knowledge suggests these reflect real high consumption in large states rather than data errors, so we retain them.

4. **Output:**  
   We keep four columns:
   - `period`, `stateid`, `sales`, `revenue`.

The cleaned EIA dataset (`eia_retail_sales_clean.csv`) retains all 15,147 records and covers **January 2001–September 2025** for all 50 states plus DC. Later, during integration, states without climate data (e.g., Alaska, Hawaii, DC) are naturally excluded by the inner join.

**Ethical / legal considerations.**  
Like NOAA, EIA data are aggregated public statistics. We comply with EIA’s terms by citing the source and using the data only for non-commercial, educational analysis.

---

### 3. Integrated NOAA–EIA Dataset

The integrated dataset is created in `notebook/integrate_noaa_eia.ipynb` and `scripts/integrate_noaa_eia.py`:

- Convert `period` in EIA to `year` (int) and `month` (int).
- Map NOAA `state_name` to EIA `stateid` via a hard-coded dictionary.
- Filter NOAA to `year >= 2001` to align temporal coverage.
- Perform an **inner join** on `stateid`, `year`, `month`.

The resulting integrated table (`data/clean/noaa_eia_integrated.csv`) has:

- `year`, `month`
- `stateid`, `state_name`
- `tavg`, `cdd`, `hdd`
- `sales`, `revenue`

It contains **14,208** complete observations for the 48 contiguous states from **January 2001 through August 2025** (Alaska, Hawaii, and DC are excluded because NOAA statewide climate data are limited to the contiguous states).

---

## Data Quality (500–1000 words)

Our data quality assessment follows the steps demonstrated in Modules 9–10: profiling, missingness analysis, range checks, outlier detection, and final decisions on cleaning.

### 1. NOAA Climate Data Quality

**Profiling and structure.**  
In `clean_noaa.ipynb`, we first inspect `climate_subset` (state-level climate data before dropping missing values):

- 75,456 rows
- Columns: `state_name`, `year`, `month`, `tavg`, `cdd`, `hdd`
- Years 1895–2025, 48 states, 12 months.

All columns have the expected types (`int64` for year, `float64` for climate variables, `object` for state and month labels).

**Missing values.**  
NOAA encodes missing values using sentinel codes:

- `tavg = -99.9`
- `cdd = -9999`
- `hdd = -9999`

We replace these codes with `NaN`, then recompute missingness:

- `tavg`: 192 missing
- `cdd`: 192 missing
- `hdd`: 192 missing
- All other columns: 0 missing.

When we inspect `missing_rows`, we find a very clear pattern:

- All 192 missing rows occur in **2025**, months **September–December**, across all 48 states.  
- This matches NOAA’s partially released nClimDiv product, where late-2025 climate values have not yet been published.

Because the missingness is **structural and not recoverable**, and because we do not want to mix incomplete climate years with complete ones, we **drop all rows where any of `tavg`, `cdd`, or `hdd` is missing**. The resulting `climate_subset_clean` has 75,264 rows and complete coverage through August 2025.

**Range and validity checks.**

We perform simple range checks:

- `tavg < -40` or `tavg > 120`: 0 rows.
- `cdd < 0` or `hdd < 0`: 0 rows.

This suggests that, after removing sentinel codes, all remaining climate values lie in physically meaningful ranges for U.S. states.

**Decision summary.**

- **Missingness:** Drop late-2025 rows with missing climate values.  
- **Outliers & ranges:** No suspicious values remain after cleaning.  
- **Impact on analysis:** Our integrated dataset stops at August 2025 but otherwise has complete monthly coverage back to 2001 for all contiguous states.

---

### 2. EIA Retail Sales Data Quality

**Profiling.**  
From `clean_eia.ipynb`, the raw EIA table has 15,147 rows and 11 columns. `info()` shows:

- `sales`, `revenue` are `float64` with no missing values.
- `customers` has 10,863 non-null entries (~71.7%), i.e., **4,284 missing** (~28.3%).

**Missing values.**

We compute missing counts and percentages and find:

- `period`, `stateid`, `stateDescription`, `sectorid`, `sectorName`, `sales`, `revenue`, and all unit-description columns: 0% missing.
- `customers`: 28.28% missing.

The missing `customers` data are widespread across years and states, suggesting systematic gaps rather than isolated errors. Because our research questions focus on **sales and revenue**, and because the NOAA dataset has no comparable customer count field, imputation would not improve integration or analysis. We therefore **drop `customers` and `customers-units`** entirely.

After dropping non-needed columns and metadata columns, we verify:

- `sales` and `revenue` have no missing values.
- All rows still correspond to `sectorid = ALL` (all sectors), ensuring a consistent definition of demand.

**Range and outlier checks.**

We compute basic statistics for `revenue`:

- min: ~40 million USD
- median: ~412 million
- 75th percentile: ~761 million
- max: ~7,760 million

We then compute an IQR-based upper fence:

- Upper fence ≈ 1,662 million
- 1,056 rows above this fence.

These “outliers” are concentrated in large states (especially California and Texas) in recent years. We manually inspect the top 10 rows by revenue and confirm that they match plausible high-consumption months (e.g., CA summer months). Since these values reflect real economic scale rather than data errors, we **retain all rows** and simply document the heavy-tailed distribution.

**Decision summary.**

- **Missingness:** Drop `customers` rather than impute; all remaining variables are complete.  
- **Outliers:** Large revenues are treated as legitimate extreme values.  
- **Units and consistency:** We retain the `period` string (later split into `year` and `month`) and keep sales and revenue in their original units (million kWh / million USD) for comparability.

---

### 3. Integrated Dataset Quality

In `integrate_noaa_eia.ipynb`, we merge cleaned NOAA and EIA tables by:

1. Splitting EIA `period` into `year` and `month` (integers).
2. Mapping NOAA `state_name` to EIA `stateid`.
3. Filtering NOAA to `year >= 2001`.
4. Performing an **inner join** on `(stateid, year, month)`.

We then check missingness in `integrated_preview`:

- All variables (`state_name`, `year`, `month`, `tavg`, `cdd`, `hdd`, `stateid`, `period`, `sales`, `revenue`) have **0 missing values**.

Finally, we drop the redundant `period` column and reorder columns for clarity, producing `integrated_clean` with:

- 14,208 rows
- 9 columns: `year`, `month`, `stateid`, `state_name`, `tavg`, `cdd`, `hdd`, `sales`, `revenue`.

Because NOAA only covers the contiguous 48 states, **Alaska, Hawaii, and DC are excluded** from the integrated panel. For the remaining states, the panel is complete for January 2001–August 2025.

---

## Findings (~500 words)

We address our research questions using the integrated NOAA–EIA dataset and the analysis notebook `analysis_noaa_eia.ipynb`.

### 1. Linear relationships between climate and electricity demand

We compute Pearson correlations among five variables: `tavg`, `cdd`, `hdd`, `sales`, and `revenue`. The correlation matrix (visualized in `results/corr_heatmap.png`) shows:

- **Strong internal climate relationships:**  
  - `tavg` and `hdd`: –0.97 (as temperature rises, heating degree days fall).  
  - `tavg` and `cdd`: 0.76 (warmer months have more cooling degree days).  
  - `cdd` and `hdd`: –0.62.

- **Demand–climate correlations:**  
  - `sales` vs. `tavg`: ~0.27  
  - `sales` vs. `cdd`: ~0.31  
  - `sales` vs. `hdd`: –0.23  
  - `revenue` follows a very similar pattern.

These coefficients indicate that **climate variables are related to electricity demand but only moderately in a linear sense**. Higher temperatures and more cooling degree days are associated with higher sales, while more heating degree days are associated with slightly lower sales on average (reflecting differences between electric vs. non-electric heating). However, much of the variation in sales and revenue is clearly driven by non-climate factors such as population, industry, and electricity prices.

### 2. Seasonal patterns of temperature, degree days, and sales

We compute monthly averages across all states and years, and create three dual-axis plots saved as `results/seasonal_temp_cdd_hdd_sales.png`:

- **Average temperature vs. sales:** Temperature rises from winter to a July–August peak, then declines. Electricity sales follow a similar curve, with a pronounced summer peak. This suggests that **summer cooling demand is a major driver** of electricity consumption.

- **Cooling degree days vs. sales:** CDD values spike sharply in June–August. The sales curve closely tracks this spike, reinforcing the role of air-conditioning loads.

- **Heating degree days vs. sales:** HDD is highest in December–February. Sales increase in winter relative to spring and fall but not as dramatically as in summer. This implies that **electric heating contributes to demand but is generally less dominant than cooling**, likely because many households and businesses use gas or other fuels for space heating.

Together, these plots reveal a **U-shaped seasonal pattern** in electricity demand: low in mild spring/fall months, high in very hot and very cold months, with the summer peak being strongest.

### 3. Spatial variation in average sales

Using Plotly choropleth maps, we visualize **average electricity sales by state**:

- **Highest sales:** Texas stands out with the highest average monthly sales, reflecting its large population, energy-intensive industry, and hot summers. California, Florida, and New York also show high values consistent with their population and economic size.

- **Moderate sales:** Many Midwestern and Northeastern states exhibit moderate sales levels, balancing substantial heating needs with moderate populations.

- **Lower sales:** Mountain West and some Great Plains states have comparatively lower sales, aligning with smaller populations and less energy-intensive industrial bases.

These patterns highlight that **electricity demand is shaped by both climate and structural factors**. Hot, populous states with robust industrial sectors consume substantially more electricity than cooler or less populated states, even after averaging across many years.

---

## Future Work (500–1000 words)

This project establishes a clean, integrated, and reproducible dataset linking climate indicators with state-level electricity demand. Several promising extensions could deepen both the methodological and substantive insights:

1. **Incorporate demographic and economic covariates.**  
   Our current analysis uses climate variables alone. Adding population, GDP, industrial composition, or urbanization metrics would allow us to disentangle how much variation in electricity demand is due to climate vs. economic scale. This would support elasticities such as “kWh per capita per °F” or “kWh per unit of state GDP.”

2. **Model non-linear and threshold effects.**  
   Correlation coefficients only capture linear relationships, but the true climate–demand relationship is strongly non-linear (e.g., cooling demand only activates above a comfort temperature). Future work could fit:
   - Piecewise linear or spline models in temperature.
   - Non-linear regression on CDD/HDD.
   - Generalized additive models (GAMs) or tree-based models that automatically capture thresholds and interactions.

3. **Time-series and panel models.**  
   With over 20 years of monthly data for 48 states, the dataset is well suited to:
   - State-level fixed-effects panel regressions (controlling for time-invariant state differences).  
   - Seasonally adjusted ARIMA or SARIMAX models using CDD/HDD as exogenous regressors.  
   - Forecasting experiments for near-term electricity demand under different climate scenarios.

4. **Sector-specific analysis.**  
   We currently aggregate across all sectors (`sectorid = ALL`). The EIA API offers sector breakdowns (residential, commercial, industrial, transportation). Repeating the integration and analysis at the sector level would show how climate sensitivity differs across sectors—e.g., residential demand may react more strongly to CDD than industrial demand.

5. **Price and policy effects.**  
   Electricity demand is also shaped by retail prices, energy efficiency policies, and technology adoption (e.g., heat pumps, rooftop solar). Integrating state-level price data, renewable penetration, or policy indices (renewable portfolio standards, building codes) could help explain deviations from purely climate-driven patterns.

6. **Climate change trends.**  
   Because NOAA’s nClimDiv spans 1895–present, we could extend the climate series further back and compare early-2000s versus recent years. This would enable questions such as: Are summer CDDs increasing over time for specific regions? How does that translate into electricity demand growth after controlling for population?

7. **Improved spatial granularity.**  
   State-level averages hide within-state variation (e.g., coastal vs. inland California). Future work could use climate division or county-level climate data combined with utility service territories or county-level electricity statistics (where available) to analyze finer spatial patterns.

8. **Packaging and archiving.**  
   To improve FAIRness, we could:
   - Publish the cleaned and integrated dataset (or at least documentation and scripts) in an archival repository such as Zenodo.  
   - Add richer machine-readable metadata (e.g., DataCite, DCAT, or schema.org JSON-LD).  
   - Optionally build a Docker image capturing the entire runtime environment.

Each of these directions would build on the reproducible foundation we designed here: transparent acquisition, clearly documented cleaning steps, and a Snakemake-based workflow that can be extended with additional rules for new datasets and analyses.

---

## Reproducing

This section provides all steps needed for another user to reproduce our entire project workflow, from acquiring data to generating final results.

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
    │   ├── analysis_noaa_eia.ipynb     # Climate–electricity analysis & figures
    │   └── openrefine_history.json     # Openrefine operation History
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

## Box data sharing 
We also upload our cleaned / integrated datasets and key outputs to Box so TAs can access them directly.
Shareable Box folder:
https://uofi.box.com/s/hm5d4i6fq5g43vmyz6ejv48ho0czny7h
The Box folder contains: 
-noaa_climate_clean.csv
-eia_retail_sales_clean.csv
-noaa_eia_integrated.csv

## References

### Data Sources
- National Centers for Environmental Information (2023). *nClimDiv Climate Divisional Database.*
  https://www.ncei.noaa.gov/pub/data/cirs/climdiv/
- U.S. Energy Information Administration (2023). *Electricity Data Browser – Retail Sales.*
  https://www.eia.gov/electricity/data/browser/
### Software & Libraries
- Python Software Foundation (2023). Python 3.x  
- NumPy, pandas, Matplotlib, Seaborn, Requests  
- Snakemake workflow engine  

### Course Documentation
- IS477 Course Staff (2025). *Course Project Overview & Instructions.* (Internal document)


