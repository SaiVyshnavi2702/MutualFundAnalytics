# Data Dictionary

## Overview

This document contains details of the datasets used in the Mutual Fund Analytics project. It describes the columns, data types, and purpose of each field.

# Dataset 1: Fund Master

Source: `01_fund_master.csv`

| Column | Data Type | Description |
|---|---|---|
| amfi_code | Integer | Unique AMFI scheme code |
| fund_house | Text | Name of the mutual fund company |
| scheme_name | Text | Name of the mutual fund scheme |
| category | Text | Fund category |
| sub_category | Text | Fund sub-category |
| plan | Text | Direct or Regular plan type |
| launch_date | Date | Date when the scheme was launched |
| benchmark | Text | Benchmark index used for comparison |
| expense_ratio_pct | Float | Expense ratio percentage |
| exit_load_pct | Float | Exit load percentage |
| min_sip_amount | Integer | Minimum SIP investment amount |
| min_lumpsum_amount | Integer | Minimum lump sum investment amount |
| fund_manager | Text | Name of the fund manager |
| risk_category | Text | Risk level of the scheme |
| sebi_category_code | Text | SEBI category classification code |

# Dataset 2: NAV History

Source: `02_nav_history.csv`

| Column | Data Type | Description |
|---|---|---|
| amfi_code | Integer | Scheme identification code |
| date | Date | Date of NAV record |
| nav | Float | Net Asset Value of the scheme |

# Dataset 3: AUM by Fund House

Source: `03_aum_by_fund_house.csv`

| Column | Data Type | Description |
|---|---|---|
| date | Date | Reporting date |
| fund_house | Text | Name of the fund house |
| aum_lakh_crore | Float | Assets under management in lakh crore |
| aum_crore | Integer | Assets under management in crore |
| num_schemes | Integer | Total number of schemes |

# Dataset 4: Monthly SIP Inflows

Source: `04_monthly_sip_inflows.csv`

| Column | Data Type | Description |
|---|---|---|
| month | Date | Month of reporting |
| sip_inflow_crore | Integer | Monthly SIP inflow amount |
| active_sip_accounts_crore | Float | Active SIP accounts |
| new_sip_accounts_lakh | Float | New SIP accounts registered |
| sip_aum_lakh_crore | Float | SIP assets under management |
| yoy_growth_pct | Float | Year-over-Year growth percentage |

# Dataset 5: Category Inflows

Source: `05_category_inflows.csv`

| Column | Data Type | Description |
|---|---|---|
| month | Date | Month of reporting |
| category | Text | Mutual fund category |
| net_inflow_crore | Float | Net inflow for the category |

# Dataset 6: Industry Folio Count

Source: `06_industry_folio_count.csv`

| Column | Data Type | Description |
|---|---|---|
| month | Date | Month of reporting |
| total_folios_crore | Float | Total number of folios |
| equity_folios_crore | Float | Equity category folios |
| debt_folios_crore | Float | Debt category folios |
| hybrid_folios_crore | Float | Hybrid category folios |
| others_folios_crore | Float | Other category folios |

# Dataset 7: Scheme Performance

Source: `07_scheme_performance.csv`

| Column | Data Type | Description |
|---|---|---|
| amfi_code | Integer | Scheme identification code |
| scheme_name | Text | Name of the scheme |
| fund_house | Text | Name of the fund house |
| category | Text | Fund category |
| return_1yr_pct | Float | One-year return percentage |
| return_3yr_pct | Float | Three-year return percentage |
| return_5yr_pct | Float | Five-year return percentage |
| benchmark_3yr_pct | Float | Three-year benchmark return |
| alpha | Float | Fund alpha value |
| beta | Float | Fund beta value |
| sharpe_ratio | Float | Sharpe ratio |
| sortino_ratio | Float | Sortino ratio |
| std_dev_ann_pct | Float | Annual standard deviation |
| max_drawdown_pct | Float | Maximum drawdown percentage |
| aum_crore | Integer | Assets under management |
| expense_ratio_pct | Float | Expense ratio percentage |
| morningstar_rating | Integer | Morningstar rating |
| risk_grade | Text | Risk classification grade |

# Dataset 8: Investor Transactions

Source: `08_investor_transactions.csv`

| Column | Data Type | Description |
|---|---|---|
| investor_id | Text | Unique investor identifier |
| transaction_date | Date | Date of transaction |
| amfi_code | Integer | Scheme identification code |
| transaction_type | Text | Type of transaction (SIP, Lumpsum, Redemption) |
| amount_inr | Integer | Transaction amount in INR |
| state | Text | Investor state |
| city | Text | Investor city |
| city_tier | Text | City classification tier |
| age_group | Text | Investor age group |
| gender | Text | Investor gender |
| annual_income_lakh | Float | Annual income |
| payment_mode | Text | Mode of payment |
| kyc_status | Text | KYC verification status |

# Dataset 9: Portfolio Holdings

Source: `09_portfolio_holdings.csv`

| Column | Data Type | Description |
|---|---|---|
| amfi_code | Integer | Scheme identification code |
| stock_symbol | Text | Stock symbol |
| stock_name | Text | Name of the company |
| sector | Text | Industry sector |
| weight_pct | Float | Portfolio allocation percentage |
| market_value_cr | Float | Market value in crore |
| current_price_inr | Float | Current stock price |
| portfolio_date | Date | Portfolio reporting date |

# Dataset 10: Benchmark Indices

Source: `10_benchmark_indices.csv`

| Column | Data Type | Description |
|---|---|---|
| date | Date | Trading date |
| index_name | Text | Name of the benchmark index |
| close_value | Float | Closing index value |

# Data Source

The datasets were provided as part of the Bluestock Fintech Mutual Fund Analytics Capstone Project. The data was cleaned, validated, and loaded into a SQLite database for analysis and reporting.

# Data Processing Note

The raw datasets were cleaned and prepared before loading them into the database. Duplicate records, missing values, and data quality issues were checked during the cleaning process.