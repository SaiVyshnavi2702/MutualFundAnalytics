from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = Path(__file__).resolve().parent

funds = {
    "Axis Bluechip": "Axis_Bluechip_live_nav.csv",
    "HDFC Top 100 Direct": "HDFC_Top100_Direct_live_nav.csv",
    "ICICI Bluechip": "ICICI_Bluechip_live_nav.csv",
    "Kotak Bluechip": "Kotak_Bluechip_live_nav.csv",
    "SBI Bluechip": "SBI_Bluechip_live_nav.csv",
}

trading_days = 252
risk_free_rate = 0.065
number_of_portfolios = 10000
random_seed = 42


# Read NAV data for the selected funds
nav_data = {}

for fund_name, file_name in funds.items():

    file_path = DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    data = pd.read_csv(file_path)

    data["date"] = pd.to_datetime(
        data["date"],
        format="%d-%m-%Y",
        errors="coerce"
    )

    data["nav"] = pd.to_numeric(
        data["nav"],
        errors="coerce"
    )

    data = (
        data.dropna(subset=["date", "nav"])
        .drop_duplicates(subset=["date"])
        .sort_values("date")
    )

    series = data.set_index("date")["nav"]

    if fund_name == "Axis Bluechip":
        scale_date = pd.Timestamp("2015-08-30")
        series.loc[series.index >= scale_date] = (
            series.loc[series.index >= scale_date] / 100.0
    )

    nav_data[fund_name] = series


# Keep dates available for all five funds
prices = pd.concat(
    nav_data,
    axis=1,
    sort=False
).dropna()


if len(prices) < 2:
    raise ValueError(
        "There are not enough common NAV observations."
    )


print("\nMarkowitz Portfolio Optimisation")
print("--------------------------------")

print("\nSelected funds:")

for fund in funds:
    print(f"- {fund}")

print(f"\nCommon observations: {len(prices)}")

print(
    f"Date range: {prices.index.min().date()} "
    f"to {prices.index.max().date()}"
)


# Calculate daily returns
daily_returns = prices.pct_change().dropna()

annual_returns = daily_returns.mean() * trading_days

annual_volatility = (
    daily_returns.std() * np.sqrt(trading_days)
)

covariance_matrix = (
    daily_returns.cov() * trading_days
)

correlation_matrix = daily_returns.corr()


def portfolio_return(weights):
    return float(
        np.dot(weights, annual_returns.values)
    )


def portfolio_volatility(weights):
    return float(
        np.sqrt(
            np.dot(
                weights.T,
                np.dot(
                    covariance_matrix.values,
                    weights
                )
            )
        )
    )


def sharpe_ratio(weights):
    volatility = portfolio_volatility(weights)

    if volatility == 0:
        return 0.0

    return (
        portfolio_return(weights) - risk_free_rate
    ) / volatility


number_of_assets = len(funds)

initial_weights = (
    np.ones(number_of_assets)
    / number_of_assets
)

bounds = tuple(
    (0.0, 1.0)
    for _ in range(number_of_assets)
)

weight_constraint = {
    "type": "eq",
    "fun": lambda weights: np.sum(weights) - 1
}


# Find the portfolio with the lowest volatility
min_volatility_result = minimize(
    portfolio_volatility,
    initial_weights,
    method="SLSQP",
    bounds=bounds,
    constraints=weight_constraint
)

if not min_volatility_result.success:
    raise RuntimeError(
        "Minimum volatility optimisation failed: "
        + min_volatility_result.message
    )

min_volatility_weights = (
    min_volatility_result.x
)

min_volatility_return = portfolio_return(
    min_volatility_weights
)

min_volatility_risk = portfolio_volatility(
    min_volatility_weights
)

min_volatility_sharpe = sharpe_ratio(
    min_volatility_weights
)


# Find the portfolio with the highest Sharpe ratio
max_sharpe_result = minimize(
    lambda weights: -sharpe_ratio(weights),
    initial_weights,
    method="SLSQP",
    bounds=bounds,
    constraints=weight_constraint
)

if not max_sharpe_result.success:
    raise RuntimeError(
        "Maximum Sharpe optimisation failed: "
        + max_sharpe_result.message
    )

max_sharpe_weights = max_sharpe_result.x

max_sharpe_return = portfolio_return(
    max_sharpe_weights
)

max_sharpe_risk = portfolio_volatility(
    max_sharpe_weights
)

max_sharpe_value = sharpe_ratio(
    max_sharpe_weights
)


# Generate random portfolios
np.random.seed(random_seed)

portfolio_results = []

for _ in range(number_of_portfolios):

    weights = np.random.dirichlet(
        np.ones(number_of_assets)
    )

    portfolio_results.append(
        [
            portfolio_return(weights),
            portfolio_volatility(weights),
            sharpe_ratio(weights),
            *weights
        ]
    )


columns = [
    "return",
    "risk",
    "sharpe"
]

columns.extend(
    [
        f"weight_{fund}"
        for fund in funds
    ]
)

simulation_data = pd.DataFrame(
    portfolio_results,
    columns=columns
)


# Calculate the efficient frontier
target_returns = np.linspace(
    simulation_data["return"].min(),
    simulation_data["return"].max(),
    100
)

frontier = []

for target_return in target_returns:

    return_constraint = {
        "type": "eq",
        "fun": (
            lambda weights,
            target=target_return:
            portfolio_return(weights) - target
        )
    }

    result = minimize(
        portfolio_volatility,
        initial_weights,
        method="SLSQP",
        bounds=bounds,
        constraints=[
            weight_constraint,
            return_constraint
        ]
    )

    if result.success:
        frontier.append(
            [
                target_return,
                portfolio_volatility(result.x)
            ]
        )


frontier_data = pd.DataFrame(
    frontier,
    columns=["return", "risk"]
)


# Save individual fund statistics
fund_statistics = pd.DataFrame(
    {
        "annual_return": annual_returns,
        "annual_volatility": annual_volatility
    }
)

fund_statistics["annual_return_pct"] = (
    fund_statistics["annual_return"] * 100
)

fund_statistics["annual_volatility_pct"] = (
    fund_statistics["annual_volatility"] * 100
)

fund_statistics.to_csv(
    OUTPUT_DIR / "fund_statistics.csv"
)


# Save correlation and covariance data
correlation_matrix.to_csv(
    OUTPUT_DIR / "correlation_matrix.csv"
)

covariance_matrix.to_csv(
    OUTPUT_DIR / "covariance_matrix.csv"
)


# Save the recommended portfolio weights
weights_data = pd.DataFrame(
    {
        "Fund": list(funds.keys()),
        "Minimum_Volatility_Weight": (
            min_volatility_weights * 100
        ),
        "Maximum_Sharpe_Weight": (
            max_sharpe_weights * 100
        )
    }
)

weights_data.to_csv(
    OUTPUT_DIR / "optimal_portfolio_weights.csv",
    index=False
)


# Save portfolio performance summary
portfolio_summary = pd.DataFrame(
    {
        "Portfolio": [
            "Minimum Volatility",
            "Maximum Sharpe"
        ],
        "Expected Return (%)": [
            min_volatility_return * 100,
            max_sharpe_return * 100
        ],
        "Volatility (%)": [
            min_volatility_risk * 100,
            max_sharpe_risk * 100
        ],
        "Sharpe Ratio": [
            min_volatility_sharpe,
            max_sharpe_value
        ]
    }
)

portfolio_summary.to_csv(
    OUTPUT_DIR / "portfolio_summary.csv",
    index=False
)


# Save simulated portfolios
simulation_data.to_csv(
    OUTPUT_DIR / "portfolio_simulations.csv",
    index=False
)


# Create the efficient frontier chart
plt.figure(figsize=(12, 8))

scatter = plt.scatter(
    simulation_data["risk"] * 100,
    simulation_data["return"] * 100,
    c=simulation_data["sharpe"],
    cmap="viridis",
    s=8,
    alpha=0.35
)

plt.colorbar(
    scatter,
    label="Sharpe Ratio"
)

if not frontier_data.empty:

    plt.plot(
        frontier_data["risk"] * 100,
        frontier_data["return"] * 100,
        color="red",
        linewidth=2.5,
        label="Efficient Frontier"
    )

plt.scatter(
    min_volatility_risk * 100,
    min_volatility_return * 100,
    color="blue",
    marker="*",
    s=300,
    label="Minimum Volatility"
)

plt.scatter(
    max_sharpe_risk * 100,
    max_sharpe_return * 100,
    color="gold",
    edgecolor="black",
    marker="*",
    s=300,
    label="Maximum Sharpe"
)

plt.xlabel("Annualised Volatility (%)")
plt.ylabel("Expected Annual Return (%)")

plt.title(
    "Markowitz Efficient Frontier - "
    "5 Selected Mutual Funds"
)

plt.legend()
plt.grid(alpha=0.25)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "efficient_frontier.png",
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# Display the results
print("\nFund Statistics")
print(fund_statistics[
    ["annual_return_pct", "annual_volatility_pct"]
].round(2))


print("\nCorrelation Matrix")
print(correlation_matrix.round(3))


print("\nMinimum Volatility Portfolio")

for fund, weight in zip(
    funds.keys(),
    min_volatility_weights
):
    print(
        f"{fund:25s}: "
        f"{weight * 100:7.2f}%"
    )

print(
    f"Expected return : "
    f"{min_volatility_return * 100:.2f}%"
)

print(
    f"Volatility      : "
    f"{min_volatility_risk * 100:.2f}%"
)

print(
    f"Sharpe ratio    : "
    f"{min_volatility_sharpe:.3f}"
)


print("\nMaximum Sharpe Portfolio")

for fund, weight in zip(
    funds.keys(),
    max_sharpe_weights
):
    print(
        f"{fund:25s}: "
        f"{weight * 100:7.2f}%"
    )

print(
    f"Expected return : "
    f"{max_sharpe_return * 100:.2f}%"
)

print(
    f"Volatility      : "
    f"{max_sharpe_risk * 100:.2f}%"
)

print(
    f"Sharpe ratio    : "
    f"{max_sharpe_value:.3f}"
)


print("\nB4 files created:")

for file_name in [
    "fund_statistics.csv",
    "correlation_matrix.csv",
    "covariance_matrix.csv",
    "optimal_portfolio_weights.csv",
    "portfolio_summary.csv",
    "portfolio_simulations.csv",
    "efficient_frontier.png"
]:
    print(f"- {file_name}")

print("\nB4 completed successfully.")