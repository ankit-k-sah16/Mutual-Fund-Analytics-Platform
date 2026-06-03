import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///database/bluestock_mf.db")

queries = {
    "top_funds": """
        SELECT  
            scheme_name,
            expense_ratio
        FROM dim_fund
        ORDER BY expense_ratio
        LIMIT 10
    """,

    "avg_nav_monthly": """
        SELECT
            d.year,
            d.month,
            ROUND(AVG(n.nav_value),2) AS avg_nav
        FROM fact_nav n
        JOIN dim_date d
            ON n.date_key=d.date_key
        GROUP BY d.year,d.month
    """
}

for name, query in queries.items():

    df = pd.read_sql(query, engine)

    print(f"\n{name}")
    print(df.head())

    df.to_csv(
        f"outputs/{name}.csv",
        index=False
    )