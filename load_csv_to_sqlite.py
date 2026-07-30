import pandas as pd
import sqlite3
import os

# Create SQLite database connection
conn = sqlite3.connect("mutualfund.db")

print("Database created successfully")


# Folder containing CSV files
data_folder = "data/raw"

# Get all CSV files
csv_files = [file for file in os.listdir(data_folder) if file.endswith(".csv")]


# Load each CSV into SQLite
for file in csv_files:

    file_path = os.path.join(data_folder, file)

    try:
        df = pd.read_csv(file_path)

    except pd.errors.EmptyDataError:
        print(f"{file} is empty. Skipping...")
        continue

    table_name = file.replace(".csv", "")

    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"{table_name} loaded successfully")


print("All CSV files loaded into database")
# Check tables in database

cursor = conn.cursor()

cursor.execute("""
SELECT name FROM sqlite_master
WHERE type='table';
""")

tables = cursor.fetchall()

print("\nTables available in database:")

for table in tables:
    print(table[0])

conn.close()