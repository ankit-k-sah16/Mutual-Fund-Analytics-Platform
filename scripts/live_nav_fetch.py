import requests
import pandas as pd


# 1. HDFC Top 100 Direct NAV History

scheme_code = 125497
url = f"https://api.mfapi.in/mf/{scheme_code}"

response = requests.get(url)
response.raise_for_status()

data = response.json()

nav_df = pd.DataFrame(data["data"])
nav_df["scheme_code"] = scheme_code
nav_df["scheme_name"] = data["meta"]["scheme_name"]

nav_df.to_csv(
    "HDFC_Top_100_Direct_NAV_History.csv",
    index=False
)

print("Saved: HDFC_Top_100_Direct_NAV_History.csv")


# 2. Latest NAV for Key Schemes

schemes = {
    "SBI Bluechip Fund Direct Growth": 119551,
    "ICICI Prudential Bluechip Fund Direct Growth": 120503,
    "Nippon India Large Cap Fund Direct Growth": 118632,
    "Axis Bluechip Fund Direct Growth": 119092,
    "Kotak Bluechip Fund Direct Growth": 120841
}

latest_navs = []

for name, code in schemes.items():
    url = f"https://api.mfapi.in/mf/{code}/latest"

    try:
        r = requests.get(url)
        r.raise_for_status()

        j = r.json()

        latest_navs.append({
            "scheme_name": name,
            "scheme_code": code,
            "nav_date": j["data"][0]["date"],
            "latest_nav": j["data"][0]["nav"]
        })

    except Exception as e:
        print(f"Error fetching {name}: {e}")

latest_df = pd.DataFrame(latest_navs)
latest_df.to_csv("LargeCap_Funds_Latest_NAV.csv", index=False)

print("\nLatest NAVs")
print(latest_df)

print("\nSaved: LargeCap_Funds_Latest_NAV.csv")