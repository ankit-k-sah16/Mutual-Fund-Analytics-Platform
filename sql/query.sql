-- Top 5 Fund Houses by AUM

SELECT
    fund_house,
    MAX(aum_value) AS latest_aum_crore
FROM fact_aum_house
GROUP BY fund_house
ORDER BY latest_aum_crore DESC
LIMIT 5;

-- Average NAV Per Month

SELECT
    d.year,
    d.month,
    ROUND(AVG(n.nav_value), 2) AS avg_nav
FROM fact_nav n
JOIN dim_date d
    ON n.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- SIP Year-over-Year Growth

SELECT
    d.year,
    SUM(t.amount) AS sip_amount
FROM fact_transactions t
JOIN dim_date d
    ON t.date_key = d.date_key
WHERE t.transaction_type = 'SIP'
GROUP BY d.year
ORDER BY d.year;

SELECT
    year,
    sip_amount,
    ROUND(
        100.0 *
        (sip_amount - LAG(sip_amount) OVER (ORDER BY year))
        / LAG(sip_amount) OVER (ORDER BY year),
        2
    ) AS yoy_growth_pct
FROM (
    SELECT
        d.year,
        SUM(t.amount) AS sip_amount
    FROM fact_transactions t
    JOIN dim_date d
        ON t.date_key = d.date_key
    WHERE t.transaction_type = 'SIP'
    GROUP BY d.year
);

-- Transactions by State

SELECT
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr),2) AS total_amount
FROM stg_investor_transactions
GROUP BY state
ORDER BY total_amount DESC;

-- Funds with Expense Ratio Below 1%
SELECT
    scheme_name,
    fund_house,
    category,
    expense_ratio
FROM dim_fund
WHERE expense_ratio < 1
ORDER BY expense_ratio;

-- Top 10 Funds by 5-Year Return

SELECT
    f.scheme_name,
    p.return_5y
FROM fact_performance p
JOIN dim_fund f
    ON p.fund_key = f.fund_key
ORDER BY p.return_5y DESC
LIMIT 10;

-- Category-wise Average Return

SELECT
    f.category,
    ROUND(AVG(p.return_3y),2) AS avg_return_3y
FROM fact_performance p
JOIN dim_fund f
    ON p.fund_key = f.fund_key
GROUP BY f.category
ORDER BY avg_return_3y DESC;

-- Monthly Investment Trend

SELECT
    d.year,
    d.month,
    ROUND(SUM(t.amount),2) AS total_investment
FROM fact_transactions t
JOIN dim_date d
    ON t.date_key = d.date_key
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- Top 10 Most Invested Funds

SELECT
    f.scheme_name,
    ROUND(SUM(t.amount),2) AS total_investment
FROM fact_transactions t
JOIN dim_fund f
    ON t.fund_key = f.fund_key
GROUP BY f.scheme_name
ORDER BY total_investment DESC
LIMIT 10;

--Transaction Mix (SIP vs Lumpsum vs Redemption)
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount),2) AS total_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;

-- Highest Average NAV Funds

SELECT
    f.scheme_name,
    ROUND(AVG(n.nav_value),2) AS avg_nav
FROM fact_nav n
JOIN dim_fund f
    ON n.fund_key = f.fund_key
GROUP BY f.scheme_name
ORDER BY avg_nav DESC
LIMIT 10;