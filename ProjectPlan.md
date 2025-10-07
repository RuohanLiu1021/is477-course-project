# ProjectPlan.md – Temperature and Electricity Consumption in the U.S.

## 1. Project Overview
This project investigates how **temperature fluctuations** affect **electricity consumption** across the United States.  
The main goal is to quantify whether higher temperatures lead to increased energy usage, particularly in warmer months, and to identify regional differences in this effect.  
By integrating official climate data from NOAA with electricity sales data from the EIA, this study will measure the sensitivity of energy demand to heating and cooling needs, providing insights for sustainable resource planning and infrastructure management.

---

## 2. Research Questions
1. Does higher temperature correspond to greater electricity consumption across U.S. states?  
2. Are there seasonal differences in this relationship (summer vs. winter)?  
3. Which states show the strongest temperature sensitivity in energy use?  

---

## 3. Team Members
- **Ruoxuan Liu** – Analyst  
  - Responsible for statistical modeling, visualization design, and interpretation of results.  
- **Yu Wan** – Analyst  
  - Responsible for data acquisition, cleaning, integration, documentation, and reproducibility management.  

---

## 4. Data Sources

### NOAA – Monthly Climate Division Data (nClimDiv)
- **Source:** National Centers for Environmental Information (NCEI), NOAA  
- **Link:** [NOAA nClimDiv Data](https://www.ncei.noaa.gov/pub/data/cirs/climdiv/)  
- **Dataset:** `climdiv-tavgst-v1.0.0`  
- **Variables:** State, Year, Month, Avg Temperature (°F × 100), Cooling Degree Days (CDD), Heating Degree Days (HDD)  
- **Frequency:** Monthly (1895–present)  
- **Use:** Main explanatory variables representing temperature stress and seasonal energy needs.

### EIA – Retail Sales of Electricity by State
- **Source:** U.S. Energy Information Administration (EIA)  
- **Link:** [EIA Electricity Data Browser](https://www.eia.gov/electricity/data/browser/)  
- **Dataset:** Retail electricity sales by state and sector (EIA-861M)  
- **Variables:** State, Year, Month, Sector, Sales (MWh), Customers, Average Price (¢/kWh)  
- **Frequency:** Monthly  
- **Use:** Dependent variable representing energy demand, normalized by customer count when necessary.

---

## 5. Data Acquisition and Integration Plan

| Step | Description | Tools |
|------|--------------|-------|
| 1 | Retrieve NOAA and EIA datasets via API or CSV download | Python, requests |
| 2 | Clean and transform data (convert temperature ×100, extract Year/Month) | pandas |
| 3 | Merge by State + Year + Month | pandas / DuckDB |
| 4 | Compute monthly averages, ratios, and derived metrics | numpy, pandas |
| 5 | Validate data quality and summarize missing values | pandas-profiling |
| 6 | Visualize relationships and patterns | matplotlib, seaborn |

---

## 6. Analysis Plan

| Objective | Method | Visualization |
|------------|---------|---------------|
| Measure temperature–consumption relationship | Pearson correlation, regression | Scatterplots, regression lines |
| Detect seasonal variation | Group by month | Line plots |
| Compare regional differences | Group by state | Heatmaps, boxplots |
| Model elasticity | Linear regression: `Electricity ~ CDD + HDD + Month + State` | Coefficient plots |

---

## 7. Expected Outcomes
- Strong **positive correlation** between higher CDD and electricity use in summer months.  
- Mild or inverse correlation between HDD and consumption in warmer regions.  
- Distinct regional patterns—southern and coastal states showing greater sensitivity.  
- Clear visual and statistical evidence supporting temperature-driven energy demand changes.

---

## 8. Reproducibility and Tools
- **Language:** Python  
- **Libraries:** pandas, numpy, matplotlib, seaborn  
- **Version control:** GitHub  
- **Database:** DuckDB for lightweight integration  
- **Environment:** Jupyter Notebook with requirements.txt  
- **Deliverables:** Clean data, merged dataset, analysis notebook, and final visualizations.  

---

## 9. Timeline (America/Chicago)

| Week | Date Range | Task | Deliverable |
|------|-------------|------|-------------|
| 1 | Oct 7–11 | Acquire NOAA & EIA datasets | Raw CSVs / API pulls |
| 2 | Oct 12–18 | Data cleaning and transformation | Cleaned data files |
| 3 | Oct 19–25 | Integration and exploratory visualization | Integrated dataset & plots |
| 4 | Oct 26–Nov 1 | Regression modeling and diagnostics | Analytical results |
| 5 | Nov 2–8 | Final pipeline, report writing, release | GitHub release & documentation |

---

## 10. Constraints
- NOAA climate divisions and EIA state-level data differ in geographic granularity → requires aggregation and consistent mapping.  
- Some EIA monthly data may be missing for recent months or specific sectors.  
- Large file sizes and API rate limits may require batch downloads or caching.  
- Temperature data reported ×100 must be rescaled before analysis.

---

## 11. Gaps
- Population and GDP normalization not yet incorporated but planned if time allows.  
- Machine learning forecasting models (ARIMA/Random Forest) beyond current project scope.  
- Weather anomaly events (storms, heatwaves) not included but could strengthen future analysis.  

---

## 12. Ethical Considerations
All data used are **aggregated, public, and free from personal identifiers**.  
NOAA and EIA are official U.S. government agencies providing **public-domain datasets**.  
License statements and attribution will be documented under `docs/licenses/`.  
No privacy, confidentiality, or copyright concerns are involved.

