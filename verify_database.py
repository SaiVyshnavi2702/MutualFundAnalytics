import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DB_PATH = PROJECT_ROOT / "bluestock_mf.db"

TABLES = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum",
]


def main():
    print("=" * 70)
    print("BLUESTOCK MUTUAL FUND ANALYTICS")
    print("STAR SCHEMA DATABASE VERIFICATION")
    print("=" * 70)

    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}"
        )

    conn = sqlite3.connect(DB_PATH)

    try:
        for table in TABLES:
            result = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()

            print(f"{table:<25} : {result[0]:>8} rows")

        print("\n" + "=" * 70)
        print("DATABASE VERIFICATION SUCCESSFUL")
        print("=" * 70)

    except sqlite3.Error as error:
        print("\nSQLite error:")
        print(error)
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()