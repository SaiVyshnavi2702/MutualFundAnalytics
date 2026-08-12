from pathlib import Path

import numpy as np
import pandas as pd


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_PATH = PROJECT_ROOT / "data" / "processed"
OUTPUT_PATH = PROJECT_ROOT / "fund_recommendations.csv"


# Load datasets
fund_master = pd.read_csv(
    DATA_PATH / "01_fund_master_clean.csv"
)

nav = pd.read_csv(
    DATA_PATH / "02_nav_history_clean.csv"
)


# Prepare NAV data
nav["date"] = pd.to_datetime(nav["date"])

nav = nav.sort_values(
    ["amfi_code", "date"]
)


# Calculate daily returns
nav["daily_return"] = (
    nav.groupby("amfi_code")["nav"]
    .pct_change()
)


# Calculate Sharpe ratio for every fund
scheme_sharpe = (
    nav.groupby("amfi_code")["daily_return"]
    .agg(
        mean_return="mean",
        std_return="std"
    )
    .reset_index()
)

# Annualize using 252 trading days
scheme_sharpe["sharpe_ratio"] = (
    scheme_sharpe["mean_return"]
    / scheme_sharpe["std_return"]
) * np.sqrt(252)


# Add fund information
recommender_data = scheme_sharpe.merge(
    fund_master[
        [
            "amfi_code",
            "scheme_name",
            "fund_house",
            "category",
            "risk_category"
        ]
    ],
    on="amfi_code",
    how="left"
)


def recommend_funds(risk_appetite):
    """
    Recommend the top three funds for a given risk appetite.

    Parameters
    ----------
    risk_appetite : str
        Investor risk preference: Low, Moderate, or High.

    Returns
    -------
    pandas.DataFrame
        Top three funds ranked by annualized Sharpe ratio.
    """

    risk_appetite = (
        risk_appetite
        .strip()
        .title()
    )

    if risk_appetite == "Low":
        matching_risk = ["Low"]

    elif risk_appetite == "Moderate":
        matching_risk = ["Moderate"]

    elif risk_appetite == "High":
        matching_risk = ["High", "Very High"]

    else:
        print("Invalid risk appetite.")
        print("Please enter Low, Moderate, or High.")
        return pd.DataFrame()

    recommendations = (
        recommender_data[
            recommender_data["risk_category"]
            .isin(matching_risk)
        ]
        .sort_values(
            "sharpe_ratio",
            ascending=False
        )
        .head(3)
    )

    return recommendations[
        [
            "amfi_code",
            "scheme_name",
            "fund_house",
            "category",
            "risk_category",
            "sharpe_ratio"
        ]
    ]


# User input
if __name__ == "__main__":

    risk = input(
        "Enter risk appetite (Low / Moderate / High): "
    )

    recommendations = recommend_funds(risk)

    if not recommendations.empty:

        print("\nTop 3 Recommended Funds:")

        print(
            recommendations.to_string(
                index=False
            )
        )

        recommendations.to_csv(
            OUTPUT_PATH,
            index=False
        )

        print(
            f"\nRecommendation saved to "
            f"{OUTPUT_PATH}"
        )