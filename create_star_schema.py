import sqlite3
import pandas as pd

print("=" * 60)
print("CREATING STAR SCHEMA DATABASE")
print("=" * 60)

# CONNECT DATABASE

conn = sqlite3.connect("bluestock_mf.db")
cursor = conn.cursor()


# EXECUTE SCHEMA.SQL

with open("sql/schema.sql", "r") as file:
    schema = file.read()

cursor.executescript(schema)

print("Star Schema Created Successfully")

# LOAD CLEANED DATASETS

fund = pd.read_csv("data/processed/01_fund_master_clean.csv")

nav = pd.read_csv("data/processed/02_nav_history_clean.csv")

aum = pd.read_csv("data/processed/03_aum_by_fund_house_clean.csv")

performance = pd.read_csv("data/processed/07_scheme_performance_clean.csv")

transactions = pd.read_csv("data/processed/08_investor_transactions_clean.csv")

print("All Cleaned CSV Files Loaded")


# DATE CONVERSION

fund["launch_date"] = pd.to_datetime(fund["launch_date"])

nav["date"] = pd.to_datetime(nav["date"])

aum["date"] = pd.to_datetime(aum["date"])

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)

print("Date Conversion Completed")


# POPULATE dim_fund

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
]

dim_fund = dim_fund.drop_duplicates()

dim_fund.to_sql(
    "dim_fund",
    conn,
    if_exists="append",
    index=False
)

print(f"Rows Inserted : {len(dim_fund)}")


# CREATE dim_date

print("\nCreating dim_date...")

dates = pd.concat([
    nav["date"],
    aum["date"],
    transactions["transaction_date"]
])

dates = pd.DataFrame({
    "full_date": pd.to_datetime(dates.unique())
})

dates = dates.sort_values("full_date")

dates["day"] = dates["full_date"].dt.day

dates["month"] = dates["full_date"].dt.month

dates["month_name"] = dates["full_date"].dt.month_name()

dates["quarter"] = dates["full_date"].dt.quarter

dates["year"] = dates["full_date"].dt.year

dates.to_sql(
    "dim_date",
    conn,
    if_exists="append",
    index=False
)
print(f"Rows Inserted : {len(dates)}")

# POPULATE fact_nav

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

print(f"Rows Inserted : {len(fact_nav)}")

# POPULATE fact_transactions

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

print(f"Rows Inserted : {len(fact_transactions)}")


# POPULATE fact_performance

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

print(f"Rows Inserted : {len(fact_performance)}")


# POPULATE fact_aum

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

print(f"Rows Inserted : {len(fact_aum)}")


# COMMIT CHANGES

conn.commit()
print("\nDatabase Saved Successfully")

# VERIFY STAR SCHEMA TABLES

print("\n" + "=" * 60)
print("STAR SCHEMA VERIFICATION")
print("=" * 60)

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

for table in tables:

    count = pd.read_sql(
        f"SELECT COUNT(*) AS total FROM {table}",
        conn
    )

    print(f"{table} : {count.iloc[0,0]} rows")


# CLOSE DATABASE
conn.close()
print("\nDatabase Connection Closed")
print("\n" + "=" * 60)
print("STAR SCHEMA CREATED SUCCESSFULLY")
print("=" * 60)