import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "bluestock_mf.db"


queries = {
    "Top 5 Funds by AUM": """
        SELECT
            f.scheme_name,
            p.aum_crore
        FROM dim_fund f
        JOIN fact_performance p
            ON f.amfi_code = p.amfi_code
        ORDER BY p.aum_crore DESC
        LIMIT 5;
    """,

    "Average NAV by Month": """
        SELECT
            strftime('%Y-%m', n.full_date) AS month,
            ROUND(AVG(n.nav), 2) AS average_nav
        FROM fact_nav n
        GROUP BY month
        ORDER BY month
        LIMIT 5;
    """,

    "Average Return by Category": """
        SELECT
            f.category,
            ROUND(AVG(p.return_3yr_pct), 2) AS avg_return_3yr_pct
        FROM dim_fund f
        JOIN fact_performance p
            ON f.amfi_code = p.amfi_code
        GROUP BY f.category
        ORDER BY avg_return_3yr_pct DESC;
    """,

    "Transaction Type Distribution": """
        SELECT
            transaction_type,
            COUNT(*) AS total_transactions,
            ROUND(SUM(amount_inr), 2) AS total_amount_inr
        FROM fact_transactions
        GROUP BY transaction_type
        ORDER BY total_transactions DESC;
    """,

    "Highest Rated Funds": """
        SELECT
            f.scheme_name,
            p.morningstar_rating,
            p.sharpe_ratio
        FROM dim_fund f
        JOIN fact_performance p
            ON f.amfi_code = p.amfi_code
        WHERE p.morningstar_rating = 5
        ORDER BY p.sharpe_ratio DESC
        LIMIT 5;
    """
}


def main():
    print("=" * 70)
    print("BLUESTOCK MUTUAL FUND ANALYTICS")
    print("D2 SQLITE QUERY VALIDATION")
    print("=" * 70)

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    conn = sqlite3.connect(DB_PATH)

    try:
        for query_name, query in queries.items():

            print("\n" + "=" * 70)
            print(query_name)
            print("=" * 70)

            rows = conn.execute(query).fetchall()

            for row in rows:
                print(row)

            print("Rows returned:", len(rows))

        print("\n" + "=" * 70)
        print("ALL D2 VALIDATION QUERIES EXECUTED SUCCESSFULLY")
        print("=" * 70)

    except sqlite3.Error as error:
        print("\nSQLite error:")
        print(error)
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()