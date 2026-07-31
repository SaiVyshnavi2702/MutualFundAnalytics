import pandas as pd
import os

print("=" * 60)
print("DATA CLEANING STARTED")
print("=" * 60)

RAW_FOLDER = "data/raw"
PROCESSED_FOLDER = "data/processed"

os.makedirs(PROCESSED_FOLDER, exist_ok=True)

datasets = [
    "01_fund_master.csv",
    "02_nav_history.csv",
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

for file in datasets:

    print("\n" + "=" * 60)
    print(f"Cleaning {file}")

    path = os.path.join(RAW_FOLDER, file)

    df = pd.read_csv(path)

    print("Original Shape:", df.shape)

    # -----------------------------------
    # Remove duplicate rows
    # -----------------------------------
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    print("Duplicates Removed:", duplicates)

    # -----------------------------------
    # Missing Values
    # -----------------------------------
    print("Missing Values")
    print(df.isnull().sum())

    # -----------------------------------
    # DATASET SPECIFIC CLEANING
    # -----------------------------------

    # Dataset 1
    if file == "01_fund_master.csv":

        df["launch_date"] = pd.to_datetime(
            df["launch_date"],
            errors="coerce"
        )

    # Dataset 2
    elif file == "02_nav_history.csv":

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        df = df.sort_values(
            ["amfi_code", "date"]
        )

        df["nav"] = df.groupby("amfi_code")["nav"].ffill()

        df = df[df["nav"] > 0]

    # Dataset 3
    elif file == "03_aum_by_fund_house.csv":

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        df = df[df["aum_crore"] > 0]

    # Dataset 4
    elif file == "04_monthly_sip_inflows.csv":

        df["month"] = pd.to_datetime(
            df["month"],
            format="%Y-%m",
            errors="coerce"
        )

        df = df[df["sip_inflow_crore"] > 0]

    # Dataset 5
    elif file == "05_category_inflows.csv":

        df["month"] = pd.to_datetime(
            df["month"],
            format="%Y-%m",
            errors="coerce"
        )

    # Dataset 6
    elif file == "06_industry_folio_count.csv":

        df["month"] = pd.to_datetime(
            df["month"],
            format="%Y-%m",
            errors="coerce"
        )

    # Dataset 7
    elif file == "07_scheme_performance.csv":

        return_columns = [
            "return_1yr_pct",
            "return_3yr_pct",
            "return_5yr_pct"
        ]

        for col in return_columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

        anomalies = df[
            (df["expense_ratio_pct"] < 0.1) |
            (df["expense_ratio_pct"] > 2.5)
        ]

        print("\nExpense Ratio Anomalies")

        print(anomalies)

    # Dataset 8
    elif file == "08_investor_transactions.csv":

        df["transaction_date"] = pd.to_datetime(
            df["transaction_date"],
            errors="coerce"
        )

        df["transaction_type"] = (
            df["transaction_type"]
            .str.strip()
            .str.title()
        )

        df = df[
            df["amount_inr"] > 0
        ]

        valid_kyc = [
            "Verified",
            "Pending"
        ]

        invalid = df[
            ~df["kyc_status"].isin(valid_kyc)
        ]

        print("\nInvalid KYC Values")

        print(invalid)

    # Dataset 9
    elif file == "09_portfolio_holdings.csv":

        df["portfolio_date"] = pd.to_datetime(
            df["portfolio_date"],
            errors="coerce"
        )

        df = df[
            (df["weight_pct"] >= 0) &
            (df["weight_pct"] <= 100)
        ]

    # Dataset 10
    elif file == "10_benchmark_indices.csv":

        df["date"] = pd.to_datetime(
            df["date"],
            errors="coerce"
        )

        df = df[
            df["close_value"] > 0
        ]

    # -----------------------------------
    # Save cleaned dataset
    # -----------------------------------

    output = file.replace(
        ".csv",
        "_clean.csv"
    )

    save_path = os.path.join(
        PROCESSED_FOLDER,
        output
    )

    df.to_csv(
        save_path,
        index=False
    )

    print("Cleaned Shape:", df.shape)

    print("Saved:", output)

print("\n" + "=" * 60)
print("ALL DATASETS CLEANED SUCCESSFULLY")
print("=" * 60)