import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# compute correct path relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
integrated_path = os.path.join(SCRIPT_DIR, "..", "data", "clean", "noaa_eia_integrated.csv")

# Load integrated (clean + merged) NOAA–EIA dataset
df = pd.read_csv(integrated_path)

# 1. Correlation Heatmap

climate_cols = ["tavg", "cdd", "hdd"]
sales_cols = ["sales", "revenue"]

corr = df[climate_cols + sales_cols].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation between Climate Variables and Electricity Metrics")
plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, "..", "results", "corr_heatmap.png"), dpi=300)
plt.close()

# 2. Seasonal Plots (TAVG, CDD, HDD vs Sales)

monthly_avg = df.groupby("month")[["tavg", "cdd", "hdd", "sales"]].mean().reset_index()

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Plot 1: Avg Temp vs Sales 
ax1 = axes[0]
ax1.plot(monthly_avg["month"], monthly_avg["tavg"], color="blue")
ax1.set_title("Avg Temperature vs Sales")
ax1.set_xlabel("Month")
ax1.set_ylabel("Avg Temp (°F)", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

ax1b = ax1.twinx()
ax1b.plot(monthly_avg["month"], monthly_avg["sales"], color="orange")
ax1b.set_ylabel("Electricity Sales (MWh)", color="orange")
ax1b.tick_params(axis="y", labelcolor="orange")

# Plot 2: CDD vs Sales 
ax2 = axes[1]
ax2.plot(monthly_avg["month"], monthly_avg["cdd"], color="green")
ax2.set_title("Cooling Degree Days vs Sales")
ax2.set_xlabel("Month")
ax2.set_ylabel("CDD", color="green")
ax2.tick_params(axis="y", labelcolor="green")

ax2b = ax2.twinx()
ax2b.plot(monthly_avg["month"], monthly_avg["sales"], color="orange")
ax2b.set_ylabel("Electricity Sales (MWh)", color="orange")
ax2b.tick_params(axis="y", labelcolor="orange")

# Plot 3: HDD vs Sales
ax3 = axes[2]
ax3.plot(monthly_avg["month"], monthly_avg["hdd"], color="purple")
ax3.set_title("Heating Degree Days vs Sales")
ax3.set_xlabel("Month")
ax3.set_ylabel("HDD", color="purple")
ax3.tick_params(axis="y", labelcolor="purple")

ax3b = ax3.twinx()
ax3b.plot(monthly_avg["month"], monthly_avg["sales"], color="orange")
ax3b.set_ylabel("Electricity Sales (MWh)", color="orange")
ax3b.tick_params(axis="y", labelcolor="orange")

plt.tight_layout()
plt.savefig(os.path.join(SCRIPT_DIR, "..", "results", "seasonal_temp_cdd_hdd_sales.png"), dpi=300)
plt.close()
