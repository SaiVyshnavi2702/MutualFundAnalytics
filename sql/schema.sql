DROP TABLE IF EXISTS fact_nav;
DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS fact_performance;
DROP TABLE IF EXISTS fact_aum;
DROP TABLE IF EXISTS dim_date;
DROP TABLE IF EXISTS dim_fund;

CREATE TABLE dim_fund (

    amfi_code INTEGER PRIMARY KEY,

    fund_house TEXT,

    scheme_name TEXT,

    category TEXT,

    sub_category TEXT,

    plan TEXT,

    benchmark TEXT,

    fund_manager TEXT,

    risk_category TEXT,

    expense_ratio_pct REAL
);


CREATE TABLE dim_date (

    date_id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_date DATE UNIQUE,

    day INTEGER,

    month INTEGER,

    month_name TEXT,

    quarter INTEGER,

    year INTEGER
);


CREATE TABLE fact_nav (

    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,

    amfi_code INTEGER,

    full_date DATE,

    nav REAL,

    FOREIGN KEY(amfi_code)

        REFERENCES dim_fund(amfi_code)
);


CREATE TABLE fact_transactions (

    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,

    investor_id TEXT,

    transaction_date DATE,

    amfi_code INTEGER,

    transaction_type TEXT,

    amount_inr REAL,

    state TEXT,

    city TEXT,

    gender TEXT,

    age_group TEXT,

    payment_mode TEXT,

    kyc_status TEXT,

    FOREIGN KEY(amfi_code)

        REFERENCES dim_fund(amfi_code)
);


CREATE TABLE fact_performance (

    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,

    amfi_code INTEGER,

    return_1yr_pct REAL,

    return_3yr_pct REAL,

    return_5yr_pct REAL,

    benchmark_3yr_pct REAL,

    alpha REAL,

    beta REAL,

    sharpe_ratio REAL,

    sortino_ratio REAL,

    std_dev_ann_pct REAL,

    max_drawdown_pct REAL,

    aum_crore REAL,

    morningstar_rating INTEGER,

    FOREIGN KEY(amfi_code)

        REFERENCES dim_fund(amfi_code)
);


CREATE TABLE fact_aum (

    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,

    fund_house TEXT,

    full_date DATE,

    aum_lakh_crore REAL,

    aum_crore REAL,

    num_schemes INTEGER
);