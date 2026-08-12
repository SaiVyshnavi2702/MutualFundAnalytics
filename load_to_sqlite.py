import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

print("=" * 60)
print("LOADING CLEANED DATASETS INTO SQLITE")
print("=" * 60)

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent
PROCESSED_FOLDER = PROJECT_ROOT / "data" / "processed"
DB_PATH = PROJECT_ROOT / "bluestock_mf.db"

# SQLite database
engine = create_engine(f"sqlite:///{DB_PATH}")

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

for file_name in datasets:

    path = PROCESSED_FOLDER / file_name

    if not path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {path}"
        )

    df = pd.read_csv(path)

    table_name = file_name.replace("_clean.csv", "")

    print(f"\nLoading {file_name}")
    print(f"Table Name : {table_name}")
    print(f"Rows       : {len(df)}")
    print(f"Columns    : {len(df.columns)}")

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Table Created : {table_name}")

print("\n" + "=" * 60)
print("ALL 10 CLEANED DATASETS LOADED SUCCESSFULLY")
print("=" * 60)