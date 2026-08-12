from pathlib import Path
import sqlite3
import pandas as pd



PROJECT_ROOT = Path(__file__).resolve().parent

DB_PATH = PROJECT_ROOT / "bluestock_mf.db"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed"


print("=" * 70)
print("BLUESTOCK MUTUAL FUND ANALYTICS")
print("CREATING COMPLETE STAR SCHEMA DATABASE")
print("=" * 70)




conn = sqlite3.connect(DB_PATH)

try:

    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON")



    print("\nLoading schema.sql...")

    with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
        schema = file.read()

    conn.executescript(schema)

    print("Star schema tables created successfully.")


    print("\nLoading processed datasets...")

    fund = pd.read_csv(
        PROCESSED_PATH / "01_fund_master_clean.csv"
    )

    nav = pd.read_csv(
        PROCESSED_PATH / "02_nav_history_clean.csv"
    )

    aum = pd.read_csv(
        PROCESSED_PATH / "03_aum_by_fund_house_clean.csv"
    )

    sip = pd.read_csv(
        PROCESSED_PATH / "04_monthly_sip_inflows_clean.csv"
    )

    category_inflows = pd.read_csv(
        PROCESSED_PATH / "05_category_inflows_clean.csv"
    )

    folio = pd.read_csv(
        PROCESSED_PATH / "06_industry_folio_count_clean.csv"
    )

    performance = pd.read_csv(
        PROCESSED_PATH / "07_scheme_performance_clean.csv"
    )

    transactions = pd.read_csv(
        PROCESSED_PATH / "08_investor_transactions_clean.csv"
    )

    holdings = pd.read_csv(
        PROCESSED_PATH / "09_portfolio_holdings_clean.csv"
    )

    benchmark = pd.read_csv(
        PROCESSED_PATH / "10_benchmark_indices_clean.csv"
    )

    print("All 10 cleaned datasets loaded.")




    print("\nConverting date columns...")

    nav["date"] = pd.to_datetime(nav["date"])

    aum["date"] = pd.to_datetime(aum["date"])

    sip["month"] = pd.to_datetime(sip["month"])

    category_inflows["month"] = pd.to_datetime(
        category_inflows["month"]
    )

    folio["month"] = pd.to_datetime(folio["month"])

    transactions["transaction_date"] = pd.to_datetime(
        transactions["transaction_date"]
    )

    holdings["portfolio_date"] = pd.to_datetime(
        holdings["portfolio_date"]
    )

    benchmark["date"] = pd.to_datetime(
        benchmark["date"]
    )

    print("Date conversion completed.")




    print("\nLoading dim_fund...")

    dim_fund = fund[
        [
            "amfi_code",
            "fund_house",
            "scheme_name",
            "category",
            "sub_category",
            "plan",
            "benchmark",
            "fund_manager",
            "risk_category",
            "expense_ratio_pct"
        ]
    ].drop_duplicates()

    dim_fund.to_sql(
        "dim_fund",
        conn,
        if_exists="append",
        index=False
    )

    print(f"dim_fund : {len(dim_fund)} rows")



    print("\nCreating dim_date...")

    all_dates = pd.concat(
        [
            nav["date"],
            aum["date"],
            sip["month"],
            category_inflows["month"],
            folio["month"],
            transactions["transaction_date"],
            holdings["portfolio_date"],
            benchmark["date"]
        ],
        ignore_index=True
    )

    all_dates = pd.to_datetime(
        all_dates
    ).dropna().drop_duplicates().sort_values()

    dim_date = pd.DataFrame(
        {
            "full_date": all_dates
        }
    )

    dim_date["day"] = dim_date["full_date"].dt.day

    dim_date["month"] = dim_date["full_date"].dt.month

    dim_date["month_name"] = (
        dim_date["full_date"].dt.month_name()
    )

    dim_date["quarter"] = (
        dim_date["full_date"].dt.quarter
    )

    dim_date["year"] = (
        dim_date["full_date"].dt.year
    )

    dim_date.to_sql(
        "dim_date",
        conn,
        if_exists="append",
        index=False
    )

    print(f"dim_date : {len(dim_date)} rows")




    print("\nLoading fact_nav...")

    fact_nav = nav[
        [
            "amfi_code",
            "date",
            "nav"
        ]
    ].copy()

    fact_nav.rename(
        columns={
            "date": "full_date"
        },
        inplace=True
    )

    fact_nav.to_sql(
        "fact_nav",
        conn,
        if_exists="append",
        index=False
    )

    print(f"fact_nav : {len(fact_nav)} rows")



    print("\nLoading fact_transactions...")

    fact_transactions = transactions[
        [
            "investor_id",
            "transaction_date",
            "amfi_code",
            "transaction_type",
            "amount_inr",
            "state",
            "city",
            "gender",
            "age_group",
            "payment_mode",
            "kyc_status"
        ]
    ].copy()

    fact_transactions.to_sql(
        "fact_transactions",
        conn,
        if_exists="append",
        index=False
    )

    print(
        f"fact_transactions : "
        f"{len(fact_transactions)} rows"
    )




    print("\nLoading fact_performance...")

    fact_performance = performance[
        [
            "amfi_code",
            "return_1yr_pct",
            "return_3yr_pct",
            "return_5yr_pct",
            "benchmark_3yr_pct",
            "alpha",
            "beta",
            "sharpe_ratio",
            "sortino_ratio",
            "std_dev_ann_pct",
            "max_drawdown_pct",
            "aum_crore",
            "morningstar_rating"
        ]
    ].copy()

    fact_performance.to_sql(
        "fact_performance",
        conn,
        if_exists="append",
        index=False
    )

    print(
        f"fact_performance : "
        f"{len(fact_performance)} rows"
    )




    print("\nLoading fact_aum...")

    fact_aum = aum[
        [
            "fund_house",
            "date",
            "aum_lakh_crore",
            "aum_crore",
            "num_schemes"
        ]
    ].copy()

    fact_aum.rename(
        columns={
            "date": "full_date"
        },
        inplace=True
    )

    fact_aum.to_sql(
        "fact_aum",
        conn,
        if_exists="append",
        index=False
    )

    print(
        f"fact_aum : "
        f"{len(fact_aum)} rows"
    )




    print("\nLoading fact_sip_inflows...")

    fact_sip = sip[
        [
            "month",
            "sip_inflow_crore",
            "active_sip_accounts_crore",
            "new_sip_accounts_lakh",
            "sip_aum_lakh_crore",
            "yoy_growth_pct"
        ]
    ].copy()

    fact_sip.to_sql(
        "fact_sip_inflows",
        conn,
        if_exists="append",
        index=False
    )

    print(
        f"fact_sip_inflows : "
        f"{len(fact_sip)} rows"
    )



    print("\nLoading fact_category_inflows...")

    fact_category = category_inflows[
        [
            "month",
            "category",
            "net_inflow_crore"
        ]
    ].copy()

    fact_category.to_sql(
        "fact_category_inflows",
        conn,
        if_exists="append",
        index=False
    )

    print(
        f"fact_category_inflows : "
        f"{len(fact_category)} rows"
    )




    print("\nLoading fact_folio_count...")

    fact_folio = folio[
        [
            "month",
            "total_folios_crore",
            "equity_folios_crore",
            "debt_folios_crore",
            "hybrid_folios_crore",
            "others_folios_crore"
        ]
    ].copy()

    fact_folio.to_sql(
        "fact_folio_count",
        conn,
        if_exists="append",
        index=False
    )

    print(
        f"fact_folio_count : "
        f"{len(fact_folio)} rows"
    )



    print("\nLoading fact_portfolio_holdings...")

    fact_holdings = holdings[
        [
            "amfi_code",
            "stock_symbol",
            "stock_name",
            "sector",
            "weight_pct",
            "market_value_cr",
            "current_price_inr",
            "portfolio_date"
        ]
    ].copy()

    fact_holdings.to_sql(
        "fact_portfolio_holdings",
        conn,
        if_exists="append",
        index=False
    )

    print(
        f"fact_portfolio_holdings : "
        f"{len(fact_holdings)} rows"
    )




    print("\nLoading fact_benchmark_indices...")

    fact_benchmark = benchmark[
        [
            "date",
            "index_name",
            "close_value"
        ]
    ].copy()

    fact_benchmark.rename(
        columns={
            "date": "full_date"
        },
        inplace=True
    )

    fact_benchmark.to_sql(
        "fact_benchmark_indices",
        conn,
        if_exists="append",
        index=False
    )

    print(
        f"fact_benchmark_indices : "
        f"{len(fact_benchmark)} rows"
    )



    conn.commit()

    print("\nDatabase saved successfully.")


    print("\n" + "=" * 70)
    print("FINAL STAR SCHEMA VERIFICATION")
    print("=" * 70)

    tables = [
        "dim_fund",
        "dim_date",
        "fact_nav",
        "fact_transactions",
        "fact_performance",
        "fact_aum",
        "fact_sip_inflows",
        "fact_category_inflows",
        "fact_folio_count",
        "fact_portfolio_holdings",
        "fact_benchmark_indices"
    ]

    for table in tables:

        result = pd.read_sql(
            f"SELECT COUNT(*) AS total FROM {table}",
            conn
        )

        count = result.iloc[0, 0]

        print(
            f"{table:<30} : {count:>8} rows"
        )

    print("\n" + "=" * 70)
    print("COMPLETE STAR SCHEMA CREATED SUCCESSFULLY")
    print("=" * 70)


except Exception as error:

    conn.rollback()

    print("\nERROR:")
    print(error)

    raise

finally:

    conn.close()

    print("\nDatabase connection closed.")
