import pandas as pd
import os

# Folder containing all CSV files
data_path = "data/raw"

# List all CSV files
csv_files = [file for file in os.listdir(data_path) if file.endswith(".csv")]

print("=" * 60)
print("DATA INGESTION STARTED")
print("=" * 60)

# Load every dataset
for file in csv_files:
    print(f"\nLoading Dataset: {file}")

    file_path = os.path.join(data_path, file)

    df = pd.read_csv(file_path)

    print("\nShape:")
    print(df.shape)

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst Five Rows:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("-" * 60)

print("\nAll datasets loaded successfully.")