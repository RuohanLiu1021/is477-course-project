# Project Plan — Temperature vs Electricity Consumption in the U.S.

## 1. Project Overview
This project explores how **temperature** influences **electricity consumption** across the United States.  
The main goal is to identify whether higher temperatures lead to increased electricity usage, especially during the summer months.  
This analysis aims to quantify the relationship between climate variability and energy demand, supporting sustainable energy planning.

---

## 2. Research Questions
- Does higher temperature correspond to greater electricity consumption?
- Are there seasonal differences in this relationship (summer vs winter)?
- Do some states show stronger temperature sensitivity than others?

---

## 3. Data Sources

### NOAA — Monthly Average Temperature (nClimDiv)
- **Source:** National Centers for Environmental Information (NCEI), NOAA  
- **Link:** [https://www.ncei.noaa.gov/pub/data/cirs/climdiv/](https://www.ncei.noaa.gov/pub/data/cirs/climdiv/)  
- **Dataset:** `climdiv-tavgst-v1.0.0`  
- **Variables:** State, Year, Month, Avg Temperature (°F × 100)  
- **Frequency:** Monthly (1895–Present)

### EIA — Retail Sales of Electricity by State
- **Source:** U.S. Energy Information Administration (EIA)  
- **Link:** [https://www.eia.gov/electricity/data/browser/](https://www.eia.gov/electricity/data/browser/)  
- **Dataset:** Retail electricity sales by state and sector  
- **Variables:** State, Year, Month, Sector, Sales (MWh)  
- **Frequency:** Monthly

---

## 4. Data Acquisition and Integration Plan

| Step | Description | Tools |
|------|--------------|--------|
| 1 | Download NOAA and EIA datasets | Browser / Python |
| 2 | Clean data (convert temp ×100, parse Year/Month) | pandas |
| 3 | Merge by State + Year + Month | pandas merge |
| 4 | Compute monthly averages and correlations | numpy, pandas |
| 5 | Visualize trends | matplotlib, seaborn |
| 6 | Version control and reproducibility | GitHub, Jupyter |

---

## 5. Analysis Plan

| Objective | Method | Visualization |
|------------|---------|----------------|
| Correlation between temperature and electricity | Pearson correlation | Scatter + regression |
| Seasonal patterns | Monthly grouping | Line charts |
| Regional comparison | State-level grouping | Boxplot / heatmap |
| Optional model | Linear regression (`Electricity ~ Temp`) | Fit plots |

---

## 6. Expected Outcomes
- A clear **positive correlation** between high temperature and electricity usage.  
- Seasonal variation: stronger correlation in summer than winter.  
- Regional differences: southern states show stronger sensitivity.  
- Visuals that demonstrate climate–energy links.

---

## 7. Reproducibility and Tools
- **Language:** Python  
- **Libraries:** pandas, numpy, matplotlib, seaborn  
- **Version control:** GitHub  
- **Reproducible environment:** Jupyter Notebook  
- **Deliverables:** Clean data, notebook, final report.

---

## 8. Timeline

| Week | Task | Deliverable |
|------|------|-------------|
| 1 | Data acquisition | Raw NOAA & EIA data |
| 2 | Data cleaning + merging | Integrated CSV |
| 3 | Exploratory analysis | Plots and stats |
| 4 | Interpret results | Draft report |
| 5 | Final reproducible pipeline | Final deliverables |

---

## 9. Course Module Alignment

| Module | Application |
|---------|--------------|
| Data Acquisition | Downloading from NOAA & EIA |
| Integration | Merging two datasets |
| Cleaning & Transformation | Temperature conversion, missing value handling |
| Data Quality | Validate time alignment |
| Visualization | Correlation and trend plots |
| Reproducibility | Git + Jupyter notebook |
| Ethics | Proper attribution, public data only |

---

## 10. Ethical Considerations
All datasets are **public, aggregated, and contain no personal data**.  
Proper citations to NOAA and EIA will be provided in the final report.

