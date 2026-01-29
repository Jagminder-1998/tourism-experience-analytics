import pandas as pd
import sqlite3
from pathlib import Path

# Absolute path to raw CSV data
DATA_PATH = Path(r"D:\New folder\Tourism_Analytics_Project\data\raw")

# Connect to SQLite database
conn = sqlite3.connect("tourism.db")


# Find all CSV files
csv_files = list(DATA_PATH.glob("*.csv"))

print("Found CSV files:")
for f in csv_files:
    print("-", f.name)

# Function to safely read CSV with encoding handling
def safe_read_csv(path):
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin1")

# Load each CSV into SQLite
for file_path in csv_files:
    table_name = file_path.stem
    print(f"\nReading {file_path.name}...")
    df = safe_read_csv(file_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Loaded table: {table_name}")

conn.close()
