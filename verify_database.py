import sqlite3

conn = sqlite3.connect("bluestock_mf.db")

cursor = conn.cursor()

tables = [

    "01_fund_master",

    "02_nav_history",

    "03_aum_by_fund_house",

    "04_monthly_sip_inflows",

    "05_category_inflows",

    "06_industry_folio_count",

    "07_scheme_performance",

    "08_investor_transactions",

    "09_portfolio_holdings",

    "10_benchmark_indices"

]

print("=" * 60)
print("DATABASE VERIFICATION")
print("=" * 60)

for table in tables:

    cursor.execute(f"SELECT COUNT(*) FROM '{table}'")

    rows = cursor.fetchone()[0]

    print(f"{table} : {rows} rows")

conn.close()

print("\nDatabase verification completed.")