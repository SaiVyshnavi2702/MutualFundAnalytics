from pathlib import Path
import subprocess
import sys
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_FOLDER = Path(__file__).resolve().parent / "logs"

LOG_FOLDER.mkdir(parents=True, exist_ok=True)


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"

    print(line)

    log_file = LOG_FOLDER / "scheduled_etl.log"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run_script(script_path):
    script_path = Path(script_path)

    if not script_path.exists():
        raise FileNotFoundError(
            f"Script not found: {script_path}"
        )

    log(f"Starting: {script_path.name}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    if result.stdout:
        log(result.stdout.strip())

    if result.stderr:
        log(result.stderr.strip())

    if result.returncode != 0:
        raise RuntimeError(
            f"{script_path.name} failed with exit code "
            f"{result.returncode}"
        )

    log(f"Completed successfully: {script_path.name}")


def main():

    log("=" * 70)
    log("BLUESTOCK AUTOMATED ETL STARTED")
    log("=" * 70)

    try:

        # Step 1: Fetch latest NAV
        run_script(
            PROJECT_ROOT / "live_nav_fetch.py"
        )

        # Step 2: Run existing ETL pipeline
        run_script(
            PROJECT_ROOT / "scripts" / "etl_pipeline.py"
        )

        log("=" * 70)
        log("BLUESTOCK AUTOMATED ETL COMPLETED SUCCESSFULLY")
        log("=" * 70)

    except Exception as error:

        log("=" * 70)
        log("BLUESTOCK AUTOMATED ETL FAILED")
        log(f"ERROR: {error}")
        log("=" * 70)

        sys.exit(1)


if __name__ == "__main__":
    main()
