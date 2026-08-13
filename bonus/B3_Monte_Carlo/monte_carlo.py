from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# BLUESTOCK MUTUAL FUND ANALYTICS
# B3 - MONTE CARLO NAV PROJECTION
# ============================================================

print("=" * 70)
print("BLUESTOCK MUTUAL FUND ANALYTICS")
print("B3 - MONTE CARLO NAV PROJECTION")
print("=" * 70)


# ------------------------------------------------------------
# PROJECT PATHS
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

NAV_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "02_nav_history_clean.csv"
)

SCORECARD_FILE = (
    PROJECT_ROOT
    / "reports"
    / "fund_scorecard.csv"
)

OUTPUT_FOLDER = Path(__file__).resolve().parent

RESULT_FILE = OUTPUT_FOLDER / "monte_carlo_results.csv"

SUMMARY_FILE = OUTPUT_FOLDER / "monte_carlo_summary.csv"

CHART_FILE = (
    OUTPUT_FOLDER
    / "Monte_Carlo_5Y_Projection.png"
)


# ------------------------------------------------------------
# SIMULATION PARAMETERS
# ------------------------------------------------------------

SIMULATIONS = 1000

TRADING_DAYS_PER_YEAR = 252

YEARS = 5

FORECAST_DAYS = (
    TRADING_DAYS_PER_YEAR * YEARS
)

RANDOM_SEED = 42


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

print("\nLoading NAV data...")

nav = pd.read_csv(NAV_FILE)

nav["date"] = pd.to_datetime(
    nav["date"],
    errors="coerce"
)

nav["nav"] = pd.to_numeric(
    nav["nav"],
    errors="coerce"
)

nav = nav.dropna(
    subset=["amfi_code", "date", "nav"]
)

nav = nav[
    nav["nav"] > 0
]

nav = nav.sort_values(
    ["amfi_code", "date"]
)

print(
    "NAV rows loaded:",
    len(nav)
)


# ------------------------------------------------------------
# LOAD EXISTING FUND SCORECARD
# ------------------------------------------------------------

print("\nLoading fund scorecard...")

scorecard = pd.read_csv(
    SCORECARD_FILE
)

scorecard = scorecard.sort_values(
    "fund_score",
    ascending=False
)

top5 = scorecard.head(5).copy()

print("\nTop 5 funds selected for Monte Carlo:")

print(
    top5[
        [
            "amfi_code",
            "scheme_name",
            "fund_score"
        ]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# RANDOM NUMBER GENERATOR
# ------------------------------------------------------------

rng = np.random.default_rng(
    RANDOM_SEED
)


# ------------------------------------------------------------
# STORE RESULTS
# ------------------------------------------------------------

all_results = []

summary_results = []


# ------------------------------------------------------------
# RUN MONTE CARLO FOR EACH FUND
# ------------------------------------------------------------

for _, fund_row in top5.iterrows():

    code = fund_row["amfi_code"]

    scheme_name = fund_row["scheme_name"]

    print("\n" + "-" * 70)

    print(
        "Simulating:",
        scheme_name
    )

    fund_nav = nav[
        nav["amfi_code"] == code
    ].copy()

    fund_nav = fund_nav.sort_values(
        "date"
    )

    # --------------------------------------------------------
    # DAILY LOG RETURNS
    # --------------------------------------------------------

    fund_nav["log_return"] = np.log(
        fund_nav["nav"]
        / fund_nav["nav"].shift(1)
    )

    returns = (
        fund_nav["log_return"]
        .dropna()
        .values
    )

    if len(returns) < 100:

        print(
            "Skipped - insufficient historical observations:",
            len(returns)
        )

        continue


    # --------------------------------------------------------
    # HISTORICAL PARAMETERS
    # --------------------------------------------------------

    mean_daily_return = np.mean(
        returns
    )

    daily_volatility = np.std(
        returns,
        ddof=1
    )

    latest_nav = fund_nav.iloc[-1]["nav"]

    latest_date = fund_nav.iloc[-1]["date"]


    # --------------------------------------------------------
    # MONTE CARLO SIMULATION
    #
    # Geometric Brownian Motion style model:
    #
    # log(S_t/S_(t-1))
    # = mu - 0.5*sigma^2 + sigma*Z
    #
    # --------------------------------------------------------

    random_shocks = rng.normal(
        0,
        1,
        size=(
            FORECAST_DAYS,
            SIMULATIONS
        )
    )

    daily_growth = (
        mean_daily_return
        - 0.5 * daily_volatility ** 2
        + daily_volatility * random_shocks
    )

    cumulative_growth = np.exp(
        np.cumsum(
            daily_growth,
            axis=0
        )
    )

    simulated_paths = (
        latest_nav
        * cumulative_growth
    )


    # --------------------------------------------------------
    # PERCENTILE BANDS
    # --------------------------------------------------------

    lower_band = np.percentile(
        simulated_paths,
        5,
        axis=1
    )

    median_path = np.percentile(
        simulated_paths,
        50,
        axis=1
    )

    upper_band = np.percentile(
        simulated_paths,
        95,
        axis=1
    )


    # --------------------------------------------------------
    # FINAL PROJECTION VALUES
    # --------------------------------------------------------

    final_5th = lower_band[-1]

    final_median = median_path[-1]

    final_95th = upper_band[-1]


    # --------------------------------------------------------
    # EXPECTED RETURN
    # --------------------------------------------------------

    projected_median_return = (
        final_median / latest_nav
    ) - 1


    # --------------------------------------------------------
    # SAVE SUMMARY
    # --------------------------------------------------------

    summary_results.append(
        [
            code,
            scheme_name,
            latest_date.strftime("%Y-%m-%d"),
            latest_nav,
            mean_daily_return,
            daily_volatility,
            final_5th,
            final_median,
            final_95th,
            projected_median_return
        ]
    )


    # --------------------------------------------------------
    # SAVE YEARLY PROJECTION POINTS
    # --------------------------------------------------------

    for year in range(1, YEARS + 1):

        day_index = (
            year
            * TRADING_DAYS_PER_YEAR
        ) - 1

        all_results.append(
            [
                code,
                scheme_name,
                year,
                lower_band[day_index],
                median_path[day_index],
                upper_band[day_index]
            ]
        )


    # --------------------------------------------------------
    # PLOT
    # --------------------------------------------------------

    plt.figure(
        figsize=(12, 7)
    )

    days = np.arange(
        1,
        FORECAST_DAYS + 1
    )

    plt.plot(
        days,
        median_path,
        label="Median projection"
    )

    plt.fill_between(
        days,
        lower_band,
        upper_band,
        alpha=0.2,
        label="5th–95th percentile range"
    )

    plt.axhline(
        latest_nav,
        linestyle="--",
        label="Current NAV"
    )

    plt.title(
        "5-Year Monte Carlo NAV Projection\n"
        + scheme_name
    )

    plt.xlabel(
        "Trading Days"
    )

    plt.ylabel(
        "Projected NAV"
    )

    plt.legend()

    plt.tight_layout()

    # Save each fund chart temporarily only for the
    # final top-5 combined chart below.
    plt.close()


    print(
        "Latest NAV:",
        round(latest_nav, 4)
    )

    print(
        "Daily volatility:",
        round(daily_volatility, 6)
    )

    print(
        "5-Year median projected NAV:",
        round(final_median, 4)
    )

    print(
        "5-Year 5th percentile:",
        round(final_5th, 4)
    )

    print(
        "5-Year 95th percentile:",
        round(final_95th, 4)
    )


# ------------------------------------------------------------
# SAVE RESULT CSV
# ------------------------------------------------------------

results_df = pd.DataFrame(
    all_results,
    columns=[
        "amfi_code",
        "scheme_name",
        "year",
        "lower_5pct_nav",
        "median_nav",
        "upper_95pct_nav"
    ]
)

results_df.to_csv(
    RESULT_FILE,
    index=False
)


# ------------------------------------------------------------
# SAVE SUMMARY CSV
# ------------------------------------------------------------

summary_df = pd.DataFrame(
    summary_results,
    columns=[
        "amfi_code",
        "scheme_name",
        "latest_date",
        "latest_nav",
        "mean_daily_log_return",
        "daily_volatility",
        "projection_5pct_nav",
        "projection_median_nav",
        "projection_95pct_nav",
        "projected_median_return"
    ]
)

summary_df.to_csv(
    SUMMARY_FILE,
    index=False
)


# ------------------------------------------------------------
# COMBINED 5-YEAR PROJECTION CHART
# ------------------------------------------------------------

plt.figure(
    figsize=(14, 8)
)

for _, row in summary_df.iterrows():

    code = row["amfi_code"]

    scheme_name = row["scheme_name"]

    fund_nav = nav[
        nav["amfi_code"] == code
    ].copy()

    fund_nav["log_return"] = np.log(
        fund_nav["nav"]
        / fund_nav["nav"].shift(1)
    )

    returns = (
        fund_nav["log_return"]
        .dropna()
        .values
    )

    mean_daily_return = np.mean(
        returns
    )

    daily_volatility = np.std(
        returns,
        ddof=1
    )

    latest_nav = fund_nav.iloc[-1]["nav"]

    local_rng = np.random.default_rng(
        RANDOM_SEED + int(code)
        if str(code).isdigit()
        else RANDOM_SEED
    )

    shocks = local_rng.normal(
        0,
        1,
        size=(
            FORECAST_DAYS,
            SIMULATIONS
        )
    )

    growth = (
        mean_daily_return
        - 0.5 * daily_volatility ** 2
        + daily_volatility * shocks
    )

    paths = latest_nav * np.exp(
        np.cumsum(
            growth,
            axis=0
        )
    )

    median_path = np.percentile(
        paths,
        50,
        axis=1
    )

    days = np.arange(
        1,
        FORECAST_DAYS + 1
    )

    plt.plot(
        days,
        median_path,
        label=scheme_name[:35]
    )


plt.title(
    "5-Year Monte Carlo Median NAV Projection - Top 5 Funds"
)

plt.xlabel(
    "Trading Days"
)

plt.ylabel(
    "Projected NAV"
)

plt.legend(
    fontsize=8
)

plt.tight_layout()

plt.savefig(
    CHART_FILE,
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ------------------------------------------------------------
# FINAL OUTPUT
# ------------------------------------------------------------

print("\n" + "=" * 70)

print(
    "MONTE CARLO SIMULATION COMPLETED SUCCESSFULLY"
)

print("=" * 70)

print(
    "Results:",
    RESULT_FILE
)

print(
    "Summary:",
    SUMMARY_FILE
)

print(
    "Chart:",
    CHART_FILE
)

print(
    "Funds simulated:",
    len(summary_df)
)

print(
    "Simulations per fund:",
    SIMULATIONS
)

print(
    "Projection period:",
    YEARS,
    "years"
)

print("=" * 70)