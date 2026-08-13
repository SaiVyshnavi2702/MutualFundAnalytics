from pathlib import Path
import os
import smtplib
from email.message import EmailMessage
import subprocess
import sys


# ============================================================
# B5 - AUTOMATED WEEKLY EMAIL SENDER
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = Path(__file__).resolve().parent

REPORT_SCRIPT = OUTPUT_DIR / "email_report.py"
HTML_REPORT = OUTPUT_DIR / "weekly_mutual_fund_report.html"


def run_report_generator():
    print("=" * 60)
    print("STEP 1 - GENERATING WEEKLY HTML REPORT")
    print("=" * 60)

    if not REPORT_SCRIPT.exists():
        raise FileNotFoundError(
            f"Report generator not found: {REPORT_SCRIPT}"
        )

    result = subprocess.run(
        [sys.executable, str(REPORT_SCRIPT)],
        cwd=BASE_DIR,
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout)

    if result.stderr:
        print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(
            f"email_report.py failed with exit code "
            f"{result.returncode}"
        )

    if not HTML_REPORT.exists():
        raise FileNotFoundError(
            f"HTML report was not created: {HTML_REPORT}"
        )

    print("HTML report generated successfully.")


def send_email():
    print("=" * 60)
    print("STEP 2 - SENDING WEEKLY EMAIL REPORT")
    print("=" * 60)

    sender_email = os.environ.get("BLUESTOCK_EMAIL")
    sender_password = os.environ.get("BLUESTOCK_EMAIL_PASSWORD")
    recipient_email = os.environ.get("BLUESTOCK_REPORT_RECIPIENT")

    if not sender_email:
        raise EnvironmentError(
            "BLUESTOCK_EMAIL environment variable is not set."
        )

    if not sender_password:
        raise EnvironmentError(
            "BLUESTOCK_EMAIL_PASSWORD environment variable is not set."
        )

    if not recipient_email:
        raise EnvironmentError(
            "BLUESTOCK_REPORT_RECIPIENT environment variable is not set."
        )

    html_content = HTML_REPORT.read_text(
        encoding="utf-8"
    )

    message = EmailMessage()

    message["Subject"] = (
        "Bluestock Mutual Fund - Weekly Performance Report"
    )

    message["From"] = sender_email
    message["To"] = recipient_email

    message.set_content(
        "Please open this email in an HTML-compatible email client "
        "to view the weekly mutual fund performance report."
    )

    message.add_alternative(
        html_content,
        subtype="html"
    )

    print(f"From      : {sender_email}")
    print(f"To        : {recipient_email}")
    print("SMTP      : smtp.gmail.com:465")
    print()

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            sender_email,
            sender_password
        )

        smtp.send_message(message)

    print("Email sent successfully.")


def main():

    print()
    print("=" * 60)
    print("B5 - AUTOMATED WEEKLY HTML EMAIL REPORT")
    print("=" * 60)
    print()

    run_report_generator()

    print()

    send_email()

    print()
    print("=" * 60)
    print("B5 EMAIL AUTOMATION COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":

    try:
        main()

    except Exception as error:

        print()
        print("=" * 60)
        print("B5 EMAIL AUTOMATION FAILED")
        print("=" * 60)
        print(f"ERROR: {error}")
        print("=" * 60)

        sys.exit(1)
