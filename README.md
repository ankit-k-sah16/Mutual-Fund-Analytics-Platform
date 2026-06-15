# Mutual Fund Analytics Dashboard 📈

Version: v1.0

A comprehensive Mutual Fund Analytics project built using Python, SQL, Power BI, and data analytics techniques to analyze mutual fund performance, risk metrics, portfolio composition, and industry trends.

## 🚀 Project Overview

This project provides end-to-end analysis of mutual fund data, covering:

- NAV performance analysis

- Fund return calculations

- Risk assessment using VaR and CVaR

- Rolling Sharpe Ratio analysis

- Portfolio allocation insights

- Industry-level AUM and SIP trend analysis

- Interactive Power BI dashboard for visualization

The project follows a complete data analytics pipeline from raw data processing to dashboard reporting.

## 📊 Key Features 

 Performance Analytics

    NAV growth tracking
    
    Fund-wise cumulative returns
    
    CAGR analysis
    
    Annual return comparison
    
    Top-performing fund identification
    
Risk Analytics

    Daily return computation
    
    Annualized volatility
    
    Sharpe Ratio
    
    Historical VaR (95%)
    
    Conditional VaR (CVaR)
    
    Rolling 90-Day Sharpe Ratio
    
Portfolio Analytics
    
    Sector allocation analysis
    
    Top holdings identification
    
    Portfolio diversification insights
    
    Concentration risk assessment
    
Industry Analytics
 
    AUM trend analysis
    
    SIP inflow monitoring
    
    AMC comparison
    
    Industry growth visualization
    
Dashboard Reporting

    Interactive Power BI Dashboard
    
    KPI cards
    
    Trend analysis
    
    Drill-through fund details
    
    Export-ready reports

## 🛠️ Technology Stack

Category : Tools Used

Programming :	Python

Data Processing :	Pandas, NumPy

Visualization	: Matplotlib, Seaborn

Database : SQLite

Dashboard	: Power BI
Development :	Jupyter Notebook
Version Control	: Git & GitHub

### bluestock_mf_capstone/
    ├── dashboard/
    │   └── bluestock_mf.pbix
    |
    ├── data/
    │   ├── raw/           ← original downloaded files
    │   ├── processed/     ← cleaned, merged CSVs
    │   └── db/            ← bluestock_mf.db (SQLite)
    |
    ├── docs/
    |   └── data_dictionary.md
    |
    ├── notebooks/
    │   ├── 01_Data_Ingestion.ipynb
    │   ├── 02_Data_Cleaning.ipynb
    │   ├── 03_ADA_Analysis.ipynb
    │   ├── 04_Performance_Analytics.ipynb
    │   └── 05_Advanced_Analytics.ipynb
    |
    ├── scripts/
    │   ├── etl_pipeline.py
    │   ├── live_nav_fetch.py
    │   ├── load_to_sqlite.py
    │   └── recommender.py
    |   ├── run_analytics.py 
    ├── sql/
    │   ├── schema.sql
    │   └── queries.sql
    |
    ├── reports/
    │   ├── Final_Report.pdf
    │   └── Presentation.pptx
    ├── requirements.txt
    └── README.md


## 📈 Dashboard Pages
### Page 1 – Industry Overview

    Total AUM
    
    SIP Inflows
    
    Total Folios
    
    Total Schemes
    
    AUM Trend Analysis
    
    AMC-wise AUM Distribution
    
### Page 2 – Fund Performance

    NAV Growth Comparison
    
    Fund Rankings
    
    Return Distribution
    
    Performance KPIs
    
### Page 3 – Risk Analytics

    Volatility Analysis
    
    Sharpe Ratio Comparison
    
    VaR and CVaR Metrics
    
    Rolling Sharpe Trends

    
### Page 4 - SIP & Market Trends
    
    SIP Inflow Trends

    Market Benchmark Tracking
    
    Industry Growth Indicators
    
### Page 5 – Fund Drill-through
    
    Fund-specific Overview
    
    Historical NAV
    
    Risk Metrics
    
    Portfolio Composition


## 📊 Risk Metrics Methodology

Historical VaR (95%)

The 5th percentile of the daily return distribution.

Conditional VaR (CVaR):

- Average return of all observations below the VaR threshold.

Rolling Sharpe Ratio:

- Computed using a rolling 90-day window:

Sharpe=

(Rolling Standard Deviation/
Rolling Mean Return) * 252
	​
## ▶️ Running the Project

- Clone Repository
  
      git clone https://github.com/ankit-k-sah16/Mutual-Fund-Analytics-Platform
      cd mutual_fund_analytics
  
- Install Dependencies

      pip install -r requirements.txt

- Execute Complete Pipeline

      python run_pipeline.py

## 📌 Project Outcomes

- Built a complete mutual fund analytics pipeline.

- Automated data cleaning and processing workflows.

- Implemented advanced financial risk metrics.

- Designed an interactive Power BI dashboard.

- Generated actionable insights from fund and industry data.

- Applied data engineering, analytics, and visualization techniques in a real-world finance use case.

## 🎯 Future Enhancements

- Portfolio Optimization Module

- Predictive Performance Modeling

- Automated Report Generation

## 👨‍💻 Author

Ankit Kumar Sah

Data Analytics Intern | Bluestock Fintech


## 🏷️ Release

v1.0 — Initial Release

- Complete data processing pipeline

- Risk analytics implementation

- Portfolio and industry analysis

- SQLite data warehouse integration

- Power BI dashboard development

- Documentation and project packaging







  
