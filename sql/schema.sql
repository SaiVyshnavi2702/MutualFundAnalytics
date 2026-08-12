PRAGMA foreign_keys = ON;
DROP TABLE IF EXISTS fact_benchmark_indices;
DROP TABLE IF EXISTS fact_portfolio_holdings;
DROP TABLE IF EXISTS fact_folio_count;
DROP TABLE IF EXISTS fact_category_inflows;
DROP TABLE IF EXISTS fact_sip_inflows;
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

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (full_date)
        REFERENCES dim_date(full_date)
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

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (transaction_date)
        REFERENCES dim_date(full_date)
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

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
);



CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_house TEXT,
    full_date DATE,
    aum_lakh_crore REAL,
    aum_crore REAL,
    num_schemes INTEGER,

    FOREIGN KEY (full_date)
        REFERENCES dim_date(full_date)
);

CREATE TABLE fact_sip_inflows (
    sip_id INTEGER PRIMARY KEY AUTOINCREMENT,
    month DATE,
    sip_inflow_crore REAL,
    active_sip_accounts_crore REAL,
    new_sip_accounts_lakh REAL,
    sip_aum_lakh_crore REAL,
    yoy_growth_pct REAL,

    FOREIGN KEY (month)
        REFERENCES dim_date(full_date)
);


CREATE TABLE fact_category_inflows (
    category_inflow_id INTEGER PRIMARY KEY AUTOINCREMENT,
    month DATE,
    category TEXT,
    net_inflow_crore REAL,

    FOREIGN KEY (month)
        REFERENCES dim_date(full_date)
);


CREATE TABLE fact_folio_count (
    folio_id INTEGER PRIMARY KEY AUTOINCREMENT,
    month DATE,
    total_folios_crore REAL,
    equity_folios_crore REAL,
    debt_folios_crore REAL,
    hybrid_folios_crore REAL,
    others_folios_crore REAL,

    FOREIGN KEY (month)
        REFERENCES dim_date(full_date)
);

CREATE TABLE fact_portfolio_holdings (
    holding_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER,
    stock_symbol TEXT,
    stock_name TEXT,
    sector TEXT,
    weight_pct REAL,
    market_value_cr REAL,
    current_price_inr REAL,
    portfolio_date DATE,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (portfolio_date)
        REFERENCES dim_date(full_date)
);


CREATE TABLE fact_benchmark_indices (
    benchmark_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date DATE,
    index_name TEXT,
    close_value REAL,

    FOREIGN KEY (full_date)
        REFERENCES dim_date(full_date)
);
