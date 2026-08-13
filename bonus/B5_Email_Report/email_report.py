from pathlib import Path
from datetime import datetime
import os
import smtplib
from email.message import EmailMessage

import pandas as pd


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "raw"

OUTPUT_DIR = Path(__file__).resolve().parent


# ============================================================
# FUNDS
# ============================================================

FUNDS = {
    "Axis Bluechip": "Axis_Bluechip_live_nav.csv",
    "HDFC Top 100 Direct": "HDFC_Top100_Direct_live_nav.csv",
    "ICICI Bluechip": "ICICI_Bluechip_live_nav.csv",
    "Kotak Bluechip"
    : "Kotak_Bluechip_live_nav.csv",
    "Nippon Large Cap": "Nippon_Large_Cap_live_nav.csv",
    "SBI Bluechip": "SBI_Bluechip_live_nav.csv",
}


# ============================================================
# GMAIL CONFIGURATION
# ============================================================

SENDER_EMAIL = os.getenv("BLUESTOCK_EMAIL")

SENDER_PASSWORD = os.getenv("BLUESTOCK_EMAIL_PASSWORD")

RECIPIENT_EMAIL = os.getenv("BLUESTOCK_REPORT_RECIPIENT")


SMTP_SERVER = "smtp.gmail.com"

SMTP_PORT = 465


# ============================================================
# VALIDATE EMAIL CONFIGURATION
# ============================================================

def validate_email_configuration():

    missing = []

    if not SENDER_EMAIL:
        missing.append("BLUESTOCK_EMAIL")

    if not SENDER_PASSWORD:
        missing.append("BLUESTOCK_EMAIL_PASSWORD")

    if not RECIPIENT_EMAIL:
        missing.append("BLUESTOCK_REPORT_RECIPIENT")

    if missing:

        raise ValueError(
            "Missing email configuration: "
            + ", ".join(missing)
        )


# ============================================================
# LOAD NAV DATA
# ============================================================

def load_nav_data(file_name):

    file_path = DATA_DIR / file_name

    if not file_path.exists():

        raise FileNotFoundError(
            f"NAV file not found: {file_path}"
        )

    data = pd.read_csv(file_path)

    required_columns = {
        "date",
        "nav"
    }

    if not required_columns.issubset(data.columns):

        raise ValueError(
            f"{file_name} must contain "
            f"date and nav columns."
        )

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
        data
        .dropna(subset=["date", "nav"])
        .drop_duplicates(subset=["date"])
        .sort_values("date")
    )

    return data


# ============================================================
# CALCULATE WEEKLY PERFORMANCE
# ============================================================

def calculate_weekly_performance():

    results = []

    for fund_name, file_name in FUNDS.items():

        data = load_nav_data(file_name)

        if len(data) < 2:
            continue

        latest_date = data["date"].max()

        previous_week_date = (
            latest_date
            - pd.Timedelta(days=7)
        )

        previous_data = data[
            data["date"] <= previous_week_date
        ]

        if previous_data.empty:
            continue

        latest_nav = data.loc[
            data["date"].idxmax(),
            "nav"
        ]

        previous_nav = previous_data.iloc[-1]["nav"]

        weekly_return = (
            (latest_nav / previous_nav) - 1
        ) * 100

        results.append(
            {
                "Fund": fund_name,

                "Latest Date":
                    latest_date.strftime(
                        "%d-%m-%Y"
                    ),

                "Latest NAV":
                    latest_nav,

                "Previous NAV":
                    previous_nav,

                "Weekly Return (%)":
                    weekly_return
            }
        )

    report_data = pd.DataFrame(results)

    if report_data.empty:

        raise ValueError(
            "No fund data was available "
            "to create the report."
        )

    report_data = report_data.sort_values(
        "Weekly Return (%)",
        ascending=False
    )

    return report_data


# ============================================================
# CREATE HTML REPORT
# ============================================================

def create_html_report(report_data):

    report_date = datetime.now().strftime(
        "%d %B %Y"
    )

    table_rows = ""

    for _, row in report_data.iterrows():

        weekly_return = (
            row["Weekly Return (%)"]
        )

        if weekly_return >= 0:

            color = "#198754"
            sign = "+"

        else:

            color = "#dc3545"
            sign = ""

        table_rows += f"""
        <tr>
            <td>{row["Fund"]}</td>

            <td>{row["Latest Date"]}</td>

            <td>
                {row["Latest NAV"]:.4f}
            </td>

            <td>
                {row["Previous NAV"]:.4f}
            </td>

            <td style="
                color:{color};
                font-weight:bold;
            ">
                {sign}{weekly_return:.2f}%
            </td>
        </tr>
        """

    best_fund = report_data.iloc[0]

    worst_fund = report_data.iloc[-1]

    html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>
Mutual Fund Weekly Report
</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background-color: #f4f6f8;
    color: #212529;
    margin: 0;
    padding: 30px;
}}

.container {{
    max-width: 1000px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 10px;
}}

h1 {{
    color: #17365d;
    margin-bottom: 5px;
}}

.subtitle {{
    color: #6c757d;
    margin-bottom: 25px;
}}

.cards {{
    display: flex;
    gap: 15px;
    margin-bottom: 25px;
}}

.card {{
    flex: 1;
    padding: 18px;
    border-radius: 8px;
    background: #f1f5f9;
}}

.card-title {{
    font-size: 13px;
    color: #6c757d;
}}

.card-value {{
    font-size: 20px;
    font-weight: bold;
    margin-top: 8px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}}

th {{
    background-color: #17365d;
    color: white;
    padding: 12px;
    text-align: left;
}}

td {{
    padding: 11px;
    border-bottom: 1px solid #dee2e6;
}}

tr:hover {{
    background-color: #f8f9fa;
}}

.footer {{
    margin-top: 30px;
    padding-top: 15px;
    border-top: 1px solid #dee2e6;
    color: #6c757d;
    font-size: 12px;
}}

</style>

</head>

<body>

<div class="container">

<h1>
Mutual Fund Weekly Performance Report
</h1>

<div class="subtitle">

Report generated on {report_date}

</div>


<div class="cards">


<div class="card">

<div class="card-title">
Funds Covered
</div>

<div class="card-value">
{len(report_data)}
</div>

</div>


<div class="card">

<div class="card-title">
Best Weekly Performer
</div>

<div class="card-value">
{best_fund["Fund"]}
</div>

</div>


<div class="card">

<div class="card-title">
Lowest Weekly Performer
</div>

<div class="card-value">
{worst_fund["Fund"]}
</div>

</div>


</div>


<h2>
Weekly Performance Summary
</h2>


<table>

<thead>

<tr>

<th>Fund</th>

<th>Latest Date</th>

<th>Latest NAV</th>

<th>Previous NAV</th>

<th>Weekly Return</th>

</tr>

</thead>


<tbody>

{table_rows}

</tbody>

</table>


<div class="footer">

This report was generated automatically from the
MutualFundAnalytics project NAV data.

</div>


</div>

</body>

</html>
"""

    report_path = (
        OUTPUT_DIR
        / "weekly_mutual_fund_report.html"
    )

    report_path.write_text(
        html,
        encoding="utf-8"
    )

    return report_path, report_date


# ============================================================
# SAVE CSV
# ============================================================

def save_csv(report_data):

    csv_path = (
        OUTPUT_DIR
        / "weekly_performance_summary.csv"
    )

    report_data.to_csv(
        csv_path,
        index=False
    )

    return csv_path


# ============================================================
# SEND EMAIL
# ============================================================

def send_email(
    report_data,
    html_path,
    report_date
):

    validate_email_configuration()

    best_fund = report_data.iloc[0]

    worst_fund = report_data.iloc[-1]

    message = EmailMessage()

    message["Subject"] = (
        "Bluestock Mutual Fund "
        f"Weekly Performance Report - "
        f"{report_date}"
    )

    message["From"] = SENDER_EMAIL

    message["To"] = RECIPIENT_EMAIL


    # --------------------------------------------------------
    # Plain-text version
    # --------------------------------------------------------

    text_body = f"""
Bluestock Mutual Fund Weekly Performance Report

Report Date: {report_date}

Funds Covered: {len(report_data)}

Best Performer:
{best_fund["Fund"]} ({best_fund["Weekly Return (%)"]:+.2f}%)

Lowest Performer:
{worst_fund["Fund"]} ({worst_fund["Weekly Return (%)"]:+.2f}%)

Weekly Performance:

"""

    for _, row in report_data.iterrows():

        text_body += (
            f"{row['Fund']}: "
            f"{row['Weekly Return (%)']:+.2f}%\n"
        )


    message.set_content(text_body)


    # --------------------------------------------------------
    # HTML version
    # --------------------------------------------------------

    html_content = html_path.read_text(
        encoding="utf-8"
    )

    message.add_alternative(
        html_content,
        subtype="html"
    )


    # --------------------------------------------------------
    # Attach HTML report
    # --------------------------------------------------------

    with open(
        html_path,
        "rb"
    ) as file:

        html_bytes = file.read()

    message.add_attachment(
        html_bytes,
        maintype="text",
        subtype="html",
        filename="weekly_mutual_fund_report.html"
    )


    # --------------------------------------------------------
    # Connect to Gmail SMTP
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("STEP 2 - SENDING WEEKLY EMAIL REPORT")
    print("=" * 60)

    print()

    print(
        f"From      : {SENDER_EMAIL}"
    )

    print(
        f"To        : {RECIPIENT_EMAIL}"
    )

    print(
        f"SMTP      : {SMTP_SERVER}:{SMTP_PORT}"
    )

    print()


    with smtplib.SMTP_SSL(
        SMTP_SERVER,
        SMTP_PORT
    ) as smtp:

        smtp.login(
            SENDER_EMAIL,
            SENDER_PASSWORD
        )

        smtp.send_message(message)


    print()
    print(
        "EMAIL SENT SUCCESSFULLY"
    )

    print(
        f"Sent to: {RECIPIENT_EMAIL}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    print()

    print("=" * 60)
    print("B5 - WEEKLY HTML EMAIL REPORT")
    print("=" * 60)

    print()


    # --------------------------------------------------------
    # STEP 1
    # Generate report
    # --------------------------------------------------------

    report_data = (
        calculate_weekly_performance()
    )

    html_path, report_date = (
        create_html_report(
            report_data
        )
    )

    csv_path = save_csv(
        report_data
    )


    print(
        f"Funds included: "
        f"{len(report_data)}"
    )

    print(
        f"Report date: "
        f"{report_date}"
    )

    print()

    print(
        "Weekly performance:"
    )

    for _, row in report_data.iterrows():

        print(
            f"{row['Fund']:25s} "
            f"{row['Weekly Return (%)']:+.2f}%"
        )


    print()

    print(
        "B5 output files:"
    )

    print(
        f"Created: {html_path}"
    )

    print(
        f"Created: {csv_path}"
    )

    print()

    print(
        "HTML report generated successfully."
    )


    # --------------------------------------------------------
    # STEP 2
    # Send email
    # --------------------------------------------------------

    send_email(
        report_data,
        html_path,
        report_date
    )


    print()

    print("=" * 60)

    print(
        "B5 EMAIL AUTOMATION COMPLETED SUCCESSFULLY"
    )

    print("=" * 60)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except Exception as error:

        print()

        print("=" * 60)

        print(
            "B5 EMAIL AUTOMATION FAILED"
        )

        print("=" * 60)

        print(
            f"ERROR: {error}"
        )

        print("=" * 60)

        raise