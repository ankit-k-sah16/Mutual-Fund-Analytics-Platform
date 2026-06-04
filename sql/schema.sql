-- DIMENSION TABLES

CREATE TABLE dim_fund (
    fund_key INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER UNIQUE NOT NULL,
    scheme_name TEXT NOT NULL,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    benchmark TEXT,
    expense_ratio REAL,
    launch_date DATE
);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day INTEGER,
    month INTEGER,
    month_name TEXT,
    quarter INTEGER,
    year INTEGER,
    week_of_year INTEGER,
    day_of_week INTEGER,
    is_weekend INTEGER
);


-- FACT TABLES


CREATE TABLE fact_nav (
    nav_fact_key INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,
    nav_value REAL NOT NULL,

    FOREIGN KEY (fund_key)
        REFERENCES dim_fund(fund_key),

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);

CREATE TABLE fact_transactions (
    transaction_fact_key INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,

    transaction_type TEXT NOT NULL,
    amount REAL NOT NULL,
    investor_count INTEGER DEFAULT 1,

    FOREIGN KEY (fund_key)
        REFERENCES dim_fund(fund_key),

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);

CREATE TABLE fact_performance (
    performance_fact_key INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_key INTEGER NOT NULL,
    date_key INTEGER NOT NULL,

    return_1m REAL,
    return_3m REAL,
    return_6m REAL,
    return_1y REAL,
    return_3y REAL,
    return_5y REAL,
    return_since_inception REAL,

    FOREIGN KEY (fund_key)
        REFERENCES dim_fund(fund_key),

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);

CREATE TABLE fact_aum_house (
    aum_fact_key INTEGER PRIMARY KEY AUTOINCREMENT,
    date_key INTEGER NOT NULL,
    fund_house TEXT NOT NULL,
    aum_value REAL NOT NULL,
    num_schemes INTEGER,

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);

CREATE INDEX idx_fund_amfi
ON dim_fund(amfi_code);

CREATE INDEX idx_nav_fund_date
ON fact_nav(fund_key, date_key);

CREATE INDEX idx_txn_fund_date
ON fact_transactions(fund_key, date_key);

CREATE INDEX idx_perf_fund_date
ON fact_performance(fund_key, date_key);

CREATE INDEX idx_aum_fund_date
ON fact_aum(fund_key, date_key);

CREATE TABLE fact_aum_house (
    aum_fact_key INTEGER PRIMARY KEY AUTOINCREMENT,
    date_key INTEGER,
    fund_house TEXT,
    aum_value REAL,

    FOREIGN KEY (date_key)
        REFERENCES dim_date(date_key)
);