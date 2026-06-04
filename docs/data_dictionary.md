# Mutual Fund Analytics Data Dictionary

## Overview

This document describes all datasets, columns, data types, business definitions, and source references used in the Mutual Fund Analytics Data Warehouse project.

---

# 1. Fund Master Dataset

**Source File:** `01_fund_master_cleaned.csv`

**Description:** Contains master information for all mutual fund schemes.

| Column Name        | Data Type | Business Definition                             |
| ------------------ | --------- | ----------------------------------------------- |
| amfi_code          | Integer   | Unique AMFI scheme identifier                   |
| fund_house         | String    | Asset Management Company (AMC) name             |
| scheme_name        | String    | Name of the mutual fund scheme                  |
| category           | String    | Fund category (Equity, Debt, Hybrid, etc.)      |
| sub_category       | String    | Detailed category classification                |
| plan               | String    | Growth, IDCW, Direct, Regular, etc.             |
| launch_date        | Date      | Date on which the scheme was launched           |
| benchmark          | String    | Benchmark index used for performance comparison |
| expense_ratio_pct  | Float     | Annual expense ratio charged by the fund (%)    |
| exit_load_pct      | Float     | Exit load charged on redemption (%)             |
| min_sip_amount     | Float     | Minimum SIP investment amount (INR)             |
| min_lumpsum_amount | Float     | Minimum lumpsum investment amount (INR)         |
| fund_manager       | String    | Fund manager responsible for the scheme         |
| risk_category      | String    | Risk classification of the scheme               |
| sebi_category_code | String    | SEBI classification code                        |

---

# 2. NAV History Dataset

**Source File:** `02_nav_history_cleaned.csv`

**Description:** Historical Net Asset Value (NAV) data for mutual fund schemes.

| Column Name | Data Type | Business Definition      |
| ----------- | --------- | ------------------------ |
| amfi_code   | Integer   | AMFI scheme identifier   |
| date        | Date      | NAV reporting date       |
| nav         | Float     | Net Asset Value per unit |

---

# 3. Investor Transactions Dataset

**Source File:** `03_investor_transactions_cleaned.csv`

**Description:** Investor purchase and redemption transactions.

| Column Name        | Data Type | Business Definition                 |
| ------------------ | --------- | ----------------------------------- |
| investor_id        | String    | Unique investor identifier          |
| transaction_date   | Date      | Transaction date                    |
| amfi_code          | Integer   | AMFI scheme identifier              |
| transaction_type   | String    | SIP, Lumpsum, or Redemption         |
| amount_inr         | Float     | Transaction amount in Indian Rupees |
| state              | String    | Investor state                      |
| city               | String    | Investor city                       |
| city_tier          | String    | Tier classification of city         |
| age_group          | String    | Investor age bracket                |
| gender             | String    | Investor gender                     |
| annual_income_lakh | Float     | Annual income in Lakhs              |
| payment_mode       | String    | UPI, Net Banking, Debit Card, etc.  |
| kyc_status         | String    | Investor KYC verification status    |

---

# 4. Scheme Performance Dataset

**Source File:** `04_scheme_performance_cleaned.csv`

**Description:** Performance and risk metrics for mutual fund schemes.

| Column Name         | Data Type | Business Definition                 |
| ------------------- | --------- | ----------------------------------- |
| amfi_code           | Integer   | AMFI scheme identifier              |
| scheme_name         | String    | Scheme name                         |
| fund_house          | String    | AMC name                            |
| category            | String    | Scheme category                     |
| plan                | String    | Fund plan type                      |
| return_1yr_pct      | Float     | One-year annualized return (%)      |
| return_3yr_pct      | Float     | Three-year annualized return (%)    |
| return_5yr_pct      | Float     | Five-year annualized return (%)     |
| benchmark_3yr_pct   | Float     | Benchmark three-year return (%)     |
| alpha               | Float     | Risk-adjusted excess return         |
| beta                | Float     | Market sensitivity measure          |
| sharpe_ratio        | Float     | Risk-adjusted return ratio          |
| sortino_ratio       | Float     | Downside risk-adjusted return ratio |
| std_dev_ann_pct     | Float     | Annualized volatility (%)           |
| max_drawdown_pct    | Float     | Maximum observed loss (%)           |
| aum_crore           | Float     | Assets Under Management (Crore INR) |
| expense_ratio_pct   | Float     | Expense ratio (%)                   |
| morningstar_rating  | Integer   | Morningstar rating score            |
| risk_grade          | String    | Fund risk grade                     |
| return_1yr_pct_flag | String    | Return quality flag                 |
| return_3yr_pct_flag | String    | Return quality flag                 |
| return_5yr_pct_flag | String    | Return quality flag                 |

---

# 5. AUM History Dataset

**Source File:** `05_aum_history_cleaned.csv`

**Description:** Industry and AMC-level Assets Under Management statistics.

| Column Name    | Data Type | Business Definition         |
| -------------- | --------- | --------------------------- |
| date           | Date      | Reporting date              |
| fund_house     | String    | Asset Management Company    |
| aum_lakh_crore | Float     | AUM measured in Lakh Crores |
| aum_crore      | Float     | AUM measured in Crores      |
| num_schemes    | Integer   | Number of active schemes    |

---

# Data Warehouse Tables

## Dimension Tables

### dim_fund

Stores master information for all mutual fund schemes.

**Primary Key:** `fund_key`

### dim_date

Stores date attributes used for time-series analysis.

**Primary Key:** `date_key`

---

## Fact Tables

### fact_nav

Stores daily NAV observations.

**Foreign Keys**

* fund_key → dim_fund
* date_key → dim_date

### fact_transactions

Stores investment and redemption transactions.

**Foreign Keys**

* fund_key → dim_fund
* date_key → dim_date

### fact_performance

Stores return and risk metrics.

**Foreign Keys**

* fund_key → dim_fund
* date_key → dim_date

### fact_aum_house

Stores AMC-level AUM metrics.

**Foreign Keys**

* date_key → dim_date

---

# Data Quality Rules

| Rule               | Validation                          |
| ------------------ | ----------------------------------- |
| AMFI Code          | Must be present in Fund Master      |
| NAV                | Must be greater than 0              |
| Expense Ratio      | Must be between 0.1% and 2.5%       |
| Transaction Amount | Must be greater than 0              |
| Dates              | Must be valid and standardized      |
| KYC Status         | Must belong to approved enum values |
| Transaction Type   | SIP, Lumpsum, Redemption            |

---

# Data Sources

| Dataset               | Source                                 |
| --------------------- | -------------------------------------- |
| Fund Master           | Mutual Fund Scheme Metadata            |
| NAV History           | AMFI NAV Reports                       |
| Investor Transactions | Simulated Investor Transaction Dataset |
| Scheme Performance    | Fund Performance Reports               |
| AUM History           | AMC AUM Reports                        |

---

**Version:** 1.0

**Last Updated:** June 2026
