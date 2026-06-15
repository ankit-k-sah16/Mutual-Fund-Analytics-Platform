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
print(nav)