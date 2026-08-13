from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_script(script_name):
    script_path = PROJECT_ROOT / script_name

    if not script_path.exists():
        raise FileNotFoundError(
            f"Required script not found: {script_path}"
        )

    print("\n" + "=" * 60)
    print(f"RUNNING: {script_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=PROJECT_ROOT
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{script_name} failed with exit code "
            f"{result.returncode}"
        )

    print(f"COMPLETED: {script_name}")


def main():
    print("=" * 60)
    print("BLUESTOCK MUTUAL FUND ETL PIPELINE")
    print("=" * 60)

    run_script("data_ingestion.py")
    run_script("data_cleaning.py")
    run_script("load_to_sqlite.py")

    print("\n" + "=" * 60)
    print("ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("\nETL PIPELINE FAILED")
        print("Error:", error)
        sys.exit(1)