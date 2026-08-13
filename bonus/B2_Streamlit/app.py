import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORTS = PROJECT_ROOT / "reports"
DATA_RAW = PROJECT_ROOT / "data" / "raw"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Bluestock Mutual Fund Analytics",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

@st.cache_data
def load_csv(path):
    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


def money(value):
    return f"₹{value:,.2f}"


# ============================================================
# LOAD EXISTING PROJECT OUTPUTS
# ============================================================

scorecard = load_csv(
    REPORTS / "fund_scorecard.csv"
)

var_cvar = load_csv(
    PROJECT_ROOT / "var_cvar_report.csv"
)

recommendations = load_csv(
    PROJECT_ROOT / "fund_recommendations.csv"
)

hhi = load_csv(
    PROJECT_ROOT / "hhi_report.csv"
)

sip_continuity = load_csv(
    PROJECT_ROOT / "sip_continuity_report.csv"
)


# ============================================================
# HEADER
# ============================================================

st.title("Bluestock Mutual Fund Analytics")

st.markdown(
    """
    **Interactive Streamlit alternative dashboard**

    This application reuses the analytical outputs generated
    during the Mutual Fund Analytics project.
    """
)

st.divider()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select analysis",
    [
        "Industry Overview",
        "Fund Performance",
        "Risk Analysis",
        "Investor Analytics",
        "Fund Recommendations"
    ]
)


# ============================================================
# PAGE 1 — INDUSTRY OVERVIEW
# ============================================================

if page == "Industry Overview":

    st.header("Industry Overview")

    st.caption(
        "High-level view of mutual fund industry and project-level analytics."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Analysed Schemes",
        len(scorecard) if not scorecard.empty else 0
    )

    col2.metric(
        "Risk Records",
        len(var_cvar) if not var_cvar.empty else 0
    )

    col3.metric(
        "Investor Records",
        len(sip_continuity) if not sip_continuity.empty else 0
    )

    col4.metric(
        "Recommendations",
        len(recommendations) if not recommendations.empty else 0
    )

    st.subheader("Fund Score Distribution")

    if not scorecard.empty and "fund_score" in scorecard.columns:

        fig = px.histogram(
            scorecard,
            x="fund_score",
            nbins=15,
            title="Distribution of Fund Scores"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.subheader("Top 10 Funds by Fund Score")

    if not scorecard.empty:

        top10 = (
            scorecard
            .sort_values(
                "fund_score",
                ascending=False
            )
            .head(10)
        )

        fig = px.bar(
            top10,
            x="fund_score",
            y="scheme_name",
            orientation="h",
            title="Top 10 Mutual Funds by Fund Score"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# PAGE 2 — FUND PERFORMANCE
# ============================================================

elif page == "Fund Performance":

    st.header("Fund Performance")

    if scorecard.empty:

        st.warning(
            "fund_scorecard.csv was not found."
        )

    else:

        # ----------------------------------------------------
        # FILTERS
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            if "fund_house" in scorecard.columns:

                fund_houses = sorted(
                    scorecard["fund_house"]
                    .dropna()
                    .unique()
                    .tolist()
                )

                selected_house = st.multiselect(
                    "Fund House",
                    fund_houses
                )

            else:
                selected_house = []

        with col2:

            if "category" in scorecard.columns:

                categories = sorted(
                    scorecard["category"]
                    .dropna()
                    .unique()
                    .tolist()
                )

                selected_category = st.multiselect(
                    "Category",
                    categories
                )

            else:
                selected_category = []

        with col3:

            if "plan" in scorecard.columns:

                plans = sorted(
                    scorecard["plan"]
                    .dropna()
                    .unique()
                    .tolist()
                )

                selected_plan = st.multiselect(
                    "Plan",
                    plans
                )

            else:
                selected_plan = []

        filtered = scorecard.copy()

        if selected_house:

            filtered = filtered[
                filtered["fund_house"]
                .isin(selected_house)
            ]

        if selected_category:

            filtered = filtered[
                filtered["category"]
                .isin(selected_category)
            ]

        if selected_plan:

            filtered = filtered[
                filtered["plan"]
                .isin(selected_plan)
            ]

        # ----------------------------------------------------
        # KPIs
        # ----------------------------------------------------

        k1, k2, k3 = st.columns(3)

        k1.metric(
            "Funds",
            len(filtered)
        )

        if "cagr_3yr" in filtered.columns:

            k2.metric(
                "Average 3Y CAGR",
                f"{filtered['cagr_3yr'].mean():.2%}"
            )

        if "sharpe_ratio" in filtered.columns:

            k3.metric(
                "Average Sharpe",
                f"{filtered['sharpe_ratio'].mean():.2f}"
            )

        # ----------------------------------------------------
        # RETURN VS RISK
        # ----------------------------------------------------

        st.subheader("Return vs Risk")

        if (
            "cagr_3yr" in filtered.columns
            and "max_drawdown" in filtered.columns
        ):

            fig = px.scatter(
                filtered,
                x="max_drawdown",
                y="cagr_3yr",
                hover_name="scheme_name",
                title="3-Year CAGR vs Maximum Drawdown"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        # ----------------------------------------------------
        # SCORECARD
        # ----------------------------------------------------

        st.subheader("Fund Performance Scorecard")

        st.dataframe(
            filtered,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PAGE 3 — RISK ANALYSIS
# ============================================================

elif page == "Risk Analysis":

    st.header("Risk Analysis")

    if var_cvar.empty:

        st.warning(
            "var_cvar_report.csv was not found."
        )

    else:

        st.subheader("VaR and CVaR")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Average VaR 95%",
                f"{var_cvar['VaR_95'].mean():.2%}"
            )

        with col2:

            st.metric(
                "Average CVaR 95%",
                f"{var_cvar['CVaR_95'].mean():.2%}"
            )

        st.caption(
            "Negative values represent downside return risk."
        )

        risk_chart = var_cvar.copy()

        risk_chart["scheme_short"] = (
            risk_chart["scheme_name"]
            .astype(str)
            .str[:45]
        )

        fig = px.scatter(
            risk_chart,
            x="VaR_95",
            y="CVaR_95",
            hover_name="scheme_name",
            title="VaR 95% vs CVaR 95%"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Highest Downside Risk")

        highest_var = (
            var_cvar
            .sort_values(
                "VaR_95",
                ascending=True
            )
            .head(10)
        )

        fig = px.bar(
            highest_var,
            x="VaR_95",
            y="scheme_name",
            orientation="h",
            title="10 Funds with Highest Downside Risk by VaR"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("VaR / CVaR Data")

        st.dataframe(
            var_cvar,
            use_container_width=True,
            hide_index=True
        )


# ============================================================
# PAGE 4 — INVESTOR ANALYTICS
# ============================================================

elif page == "Investor Analytics":

    st.header("Investor Analytics")

    if sip_continuity.empty:

        st.warning(
            "sip_continuity_report.csv was not found."
        )

    else:

        st.subheader("SIP Continuity Analysis")

        st.dataframe(
            sip_continuity,
            use_container_width=True,
            hide_index=True
        )

        numeric_columns = (
            sip_continuity
            .select_dtypes(
                include="number"
            )
            .columns
            .tolist()
        )

        if numeric_columns:

            selected_metric = st.selectbox(
                "Select investor metric",
                numeric_columns
            )

            fig = px.histogram(
                sip_continuity,
                x=selected_metric,
                title=f"Distribution of {selected_metric}"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )


# ============================================================
# PAGE 5 — FUND RECOMMENDATIONS
# ============================================================

elif page == "Fund Recommendations":

    st.header("Fund Recommendations")

    st.info(
        """
        This is a transparent analytical recommender based on
        risk-category suitability and historical Sharpe ratio.
        It is not personalized financial advice.
        """
    )

    if scorecard.empty:

        st.warning(
            "Fund scorecard is not available."
        )

    else:

        if "risk_category" in scorecard.columns:

            risk_options = sorted(
                scorecard["risk_category"]
                .dropna()
                .unique()
                .tolist()
            )

            selected_risk = st.selectbox(
                "Select Risk Appetite",
                risk_options
            )

            matching = scorecard[
                scorecard["risk_category"]
                == selected_risk
            ].copy()

            if "sharpe_ratio" in matching.columns:

                matching = (
                    matching
                    .sort_values(
                        "sharpe_ratio",
                        ascending=False
                    )
                    .head(5)
                )

            st.subheader(
                f"Top Funds for {selected_risk} Risk"
            )

            st.dataframe(
                matching,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "risk_category column is not available in fund_scorecard.csv."
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Bluestock Mutual Fund Analytics | Streamlit Bonus Challenge B2"
)
