"""
Master execution script for the Bluestock Mutual Fund Analytics project.

Runs the main data-processing scripts in sequence and stops if any
stage fails.
"""

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent


def run_script(script_name):
    """Run a Python script and raise an error if it fails."""

    script_path = PROJECT_ROOT / script_name

    print(f"\nRunning {script_name}...")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{script_name} failed with exit code {result.returncode}."
        )

    print(f"{script_name} completed successfully.")


def main():
    """Run the main project data-processing pipeline."""

    print("=" * 60)
    print("BLUESTOCK MUTUAL FUND ANALYTICS PIPELINE")
    print("=" * 60)

    run_script("data_ingestion.py")
    run_script("data_cleaning.py")
    run_script("live_nav_fetch.py")

    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()