rule all:
    input:
        "data/clean/noaa_climate_clean.csv",
        "data/clean/eia_retail_sales_clean.csv",
        "data/clean/noaa_eia_integrated.csv",
        "results/corr_heatmap.png",
        "results/seasonal_temp_cdd_hdd_sales.png"


rule clean_noaa:
    input:
        tavg="data/raw/climdiv-tmpcst-v1.0.0-20250905",
        cdd="data/raw/climdiv-cddcst-v1.0.0-20250905",
        hdd="data/raw/climdiv-hddcst-v1.0.0-20250905"
    output:
        "data/clean/noaa_climate_clean.csv"
    shell:
        "python scripts/clean_noaa.py"


rule clean_eia:
    input:
        "data/raw/eia_retail_sales.csv"
    output:
        "data/clean/eia_retail_sales_clean.csv"
    shell:
        "python scripts/clean_eia.py"


rule integrate:
    input:
        noaa="data/clean/noaa_climate_clean.csv",
        eia="data/clean/eia_retail_sales_clean.csv"
    output:
        "data/clean/noaa_eia_integrated.csv"
    shell:
        "python scripts/integrate_noaa_eia.py"


rule analyze:
    input:
        "data/clean/noaa_eia_integrated.csv"
    output:
        "results/corr_heatmap.png",
        "results/seasonal_temp_cdd_hdd_sales.png"
    shell:
        "python scripts/analyze_visualize.py"
