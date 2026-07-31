import os
import pandas as pd
from sqlalchemy import create_engine

print("=" * 60)
print("LOADING CLEANED DATASETS INTO SQLITE")
print("=" * 60)

# SQLite Database
engine = create_engine("sqlite:///bluestock_mf.db")

processed_folder = "data/processed"

datasets = [
    "01_fund_master_clean.csv",
    "02_nav_history_clean.csv",
    "03_aum_by_fund_house_clean.csv",
    "04_monthly_sip_inflows_clean.csv",
    "05_category_inflows_clean.csv",
    "06_industry_folio_count_clean.csv",
    "07_scheme_performance_clean.csv",
    "08_investor_transactions_clean.csv",
    "09_portfolio_holdings_clean.csv",
    "10_benchmark_indices_clean.csv"
]

for file in datasets:

    path = os.path.join(processed_folder, file)

    df = pd.read_csv(path)

    table_name = file.replace("_clean.csv", "").replace(".csv", "")

    print(f"\nLoading {file}")

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Table Created : {table_name}")

    print(f"Rows Loaded : {len(df)}")

print("\n" + "=" * 60)
print("ALL DATASETS LOADED SUCCESSFULLY")
print("=" * 60)