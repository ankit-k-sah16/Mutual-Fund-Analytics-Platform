## Calculating Daily Returns
import pandas as pd
import numpy as np
nav=pd.read_csv(r"D:\bluestock_mf_capstone\data\processed\02_nav_history_cleaned.csv")
nav['date']=pd.to_datetime(nav['date'])
nav=nav.sort_values(['amfi_code','date'])

nav['daily_return']=(nav.groupby('amfi_code')['nav'].pct_change())

returns=nav.dropna(subset=['daily_return'])
## VaR and CVaR

risk_metrics=[]
for fund in returns ['amfi_code'].unique():
    rt=returns.loc[
        returns['amfi_code']==fund,'daily_return'
    ]

    var95=np.percentile(rt,5)
    cvar95=rt[rt<=var95].mean()

    risk_metrics.append([fund,var95,cvar95])

    risk_df = pd.DataFrame(
    risk_metrics,
    columns=["amfi_code","VaR95","CVaR95"]
)

risk_df.sort_values("VaR95").head()


## Merging Fund Names
funds = pd.read_csv(r"D:\bluestock_mf_capstone\data\processed\01_fund_master_cleaned.csv")

risk_df = risk_df.merge(
    funds[["amfi_code","scheme_name"]],
    on="amfi_code",
    how="left"
)

# Sharpe Ratio Per Fund
sharpe = (
    returns.groupby("amfi_code")
    ["daily_return"]
    .agg(
        mean_return="mean",
        std_return="std"
    )
    .reset_index()
)

sharpe["sharpe"] = (
    sharpe["mean_return"]
    /
    sharpe["std_return"]
) * np.sqrt(252)


# Merging Risk Grade
reco_df = sharpe.merge(
    funds[
        ["amfi_code",
         "scheme_name",
         "risk_category"]
    ],
    on="amfi_code"
)

## Recommendation Function
def recommend_funds(risk_appetite):

    result = (
        reco_df[
            reco_df["risk_category"] == risk_appetite
        ]
        .sort_values(
            "sharpe",
            ascending=False
        )
        .head(5)
    )

    return result[
        ["scheme_name",
         "risk_category",
         "sharpe"]
    ]

print(recommend_funds("High"))