import pandas as pd 
import plotly.express as px
import os 
from pathlib import Path

# Loading the cleaned NAV history
df=Path("D:/bluestock_mf_capstone/data/processed/02_nav_history_cleaned.csv")
nav=pd.read_csv(df)

# Converting the date column
nav["date"] = pd.to_datetime(nav["date"])

# Filtering for 2022–2026
nav = nav[
    (nav["date"] >= "2022-01-01") &
    (nav["date"] <= "2026-12-31")
]

# CAGR calculating function

def calculate_cagr(df, years):
    
    latest_date = df["date"].max()

    start_cutoff = latest_date - pd.DateOffset(years=years)

    # Data within lookback window
    period_df = df[df["date"] >= start_cutoff]

    if len(period_df) < 2:
        return np.nan

    nav_start = period_df.iloc[0]["nav"]
    nav_end = period_df.iloc[-1]["nav"]

    if nav_start <= 0:
        return np.nan

    cagr = (nav_end / nav_start) ** (1 / years) - 1

    return cagr

#Computing CAGR for all 40 schemes/funds
results=[]
 
for amfi_code,group in nav.groupby("amfi_code"):
    results.append(
        {
            "amfi_code":amfi_code,
            "cagr_1y": calculate_cagr(group, 1),
            "cagr_3y": calculate_cagr(group, 3),
            "cagr_5y": calculate_cagr(group, 5)
        }
    )
cagr_df=pd.DataFrame(results)