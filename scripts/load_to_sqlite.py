from pathlib import Path
import pandas as pd
from sqlalchemy import text
from sqlalchemy import create_engine

BASE_DIR = Path(__file__).resolve().parent.parent

db_path = BASE_DIR / "data" / "database" / "bluestock_mf.db"

print("Using DB:", db_path)

#DATABASE CONNECTION

engine = create_engine(f"sqlite:///{db_path}")

# FILE PATHS


files = {
    "stg_fund_master": r"D:\bluestock_mf_capstone\data\processed\01_fund_master_cleaned.csv",
    "stg_nav_history": r"D:\bluestock_mf_capstone\data\processed\02_nav_history_cleaned.csv",
    "stg_investor_transactions": r"D:\bluestock_mf_capstone\data\processed\08_investor_transactions_cleaned.csv",
    "stg_scheme_performance": r"D:\bluestock_mf_capstone\data\processed\07_scheme_performance_cleaned.csv",
    "stg_aum_history": r"D:\bluestock_mf_capstone\data\processed\03_aum_by_fund_house_cleaned.csv"
}


# LOADING CSVs INTO STAGING TABLES


print("\nLoading staging tables...\n")

for table_name, file_path in files.items():

    print(f"Loading {table_name}")
    print(f"Source: {file_path}")

    df = pd.read_csv(file_path)

    print(f"Rows: {len(df)}")

    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False
    )

    print(f" {table_name}: {len(df):,} rows loaded")


# VALIDATING ROW COUNTS


print("\n" + "=" * 60)
print("ROW COUNT VALIDATION")
print("=" * 60)

with engine.connect() as conn:

    for table_name, file_path in files.items():

        csv_rows = len(pd.read_csv(file_path))

        db_rows = conn.execute(
            text(f"SELECT COUNT(*) FROM {table_name}")
        ).scalar()

        status = "PASS" if csv_rows == db_rows else "FAIL"

        print(
            f"{table_name:<30}"
            f"CSV={csv_rows:<8}"
            f"DB={db_rows:<8}"
            f"[{status}]"
        )

print("\n All staging tables loaded successfully.")

#Populating dim_fund from stg_fund_master
with engine.begin() as conn:

    conn.execute(text("""
        INSERT OR IGNORE INTO dim_fund (
            amfi_code,
            scheme_name,
            fund_house,
            category,
            sub_category,
            benchmark,
            expense_ratio,
            launch_date
        )
        SELECT DISTINCT
            amfi_code,
            scheme_name,
            fund_house,
            category,
            sub_category,
            benchmark,
            expense_ratio_pct,
            launch_date
        FROM stg_fund_master
    """))

print(" dim_fund loaded")

## Creating and Populating dim_date from stg_nav_history
nav_df = pd.read_sql(
    "SELECT DISTINCT date FROM stg_nav_history",
    engine
)

nav_df["date"] = pd.to_datetime(nav_df["date"])

dim_date = pd.DataFrame({
    "date_key": nav_df["date"].dt.strftime("%Y%m%d").astype(int),
    "full_date": nav_df["date"],
    "day": nav_df["date"].dt.day,
    "month": nav_df["date"].dt.month,
    "month_name": nav_df["date"].dt.month_name(),
    "quarter": nav_df["date"].dt.quarter,
    "year": nav_df["date"].dt.year,
    "week_of_year": nav_df["date"].dt.isocalendar().week.astype(int),
    "day_of_week": nav_df["date"].dt.dayofweek,
    "is_weekend": nav_df["date"].dt.dayofweek.isin([5, 6]).astype(int)
})

dim_date.to_sql(
    "dim_date",
    engine,
    if_exists="append",
    index=False
)

print(f" dim_date loaded ({len(dim_date)} rows)") 


## Populating fact_nav from stg_nav_history, joining with dim_fund and dim_date to get keys
with engine.begin() as conn:

    conn.execute(text("""
        INSERT  OR IGNORE INTO fact_nav (
            fund_key,
            date_key,
            nav_value
        )
        SELECT
            f.fund_key,
            d.date_key,
            n.nav
        FROM stg_nav_history n
        JOIN dim_fund f
            ON n.amfi_code = f.amfi_code
        JOIN dim_date d
            ON DATE(n.date) = DATE(d.full_date)
    """))

print(" fact_nav loaded")

# Validating row counts in final tables
with engine.connect() as conn:

    print("dim_fund:",
          conn.execute(text("SELECT COUNT(*) FROM dim_fund")).scalar())

    print("dim_date:",
          conn.execute(text("SELECT COUNT(*) FROM dim_date")).scalar())

    print("fact_nav:",
          conn.execute(text("SELECT COUNT(*) FROM fact_nav")).scalar())

    print("stg_nav_history:",
          conn.execute(text("SELECT COUNT(*) FROM stg_nav_history")).scalar())
    

#Populating fact_transactions from stg_investor_transactions, joining with dim_fund and dim_date to get keys
with engine.begin() as conn:

    conn.execute(text("""
        INSERT OR IGNORE INTO fact_transactions (
            fund_key,
            date_key,
            transaction_type,
            amount
        )
        SELECT
            f.fund_key,
            d.date_key,
            t.transaction_type,
            t.amount_inr
        FROM stg_investor_transactions t
        JOIN dim_fund f
            ON t.amfi_code = f.amfi_code
        JOIN dim_date d
            ON DATE(t.transaction_date) = DATE(d.full_date)
    """))

print(" fact_transactions loaded")

#Populating fact_performance from stg_scheme_performance, joining with dim_fund and dim_date to get keys
#Adding a snapshot date 
snapshot_date = pd.Timestamp.today().strftime("%Y-%m-%d")
date_key = int(pd.Timestamp.today().strftime("%Y%m%d"))

with engine.begin() as conn:

    conn.execute(text(f"""
        INSERT OR IGNORE INTO dim_date (
            date_key,
            full_date
        )
        VALUES (
            {date_key},
            '{snapshot_date}'
        )
    """))

with engine.begin() as conn:

    conn.execute(text(f"""
        INSERT OR IGNORE INTO fact_performance (
            fund_key,
            date_key,
            return_1y,
            return_3y,
            return_5y
        )
        SELECT
            f.fund_key,
            {date_key},
            p.return_1yr_pct,
            p.return_3yr_pct,
            p.return_5yr_pct
        FROM stg_scheme_performance p
        JOIN dim_fund f
            ON p.amfi_code = f.amfi_code
    """))

print("fact_performance loaded")

#Populating fact_aum from stg_aum_history, joining with dim_date to get date_key

with engine.begin() as conn:

    conn.execute(text("""
        INSERT OR IGNORE INTO fact_aum_house (
            date_key,
            fund_house,
            aum_value,
            num_schemes
        )
        SELECT
            d.date_key,
            a.fund_house,
            a.aum_crore,
            a.num_schemes
        FROM stg_aum_history a
        JOIN dim_date d
            ON DATE(a.date) = DATE(d.full_date)
    """))

print("fact_aum_house loaded")