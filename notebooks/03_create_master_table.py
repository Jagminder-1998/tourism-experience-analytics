import sqlite3
import pandas as pd

conn = sqlite3.connect("tourism.db")


tables = [
    "Transaction",
    "User",
    "City",
    "Country",
    "Region",
    "Continent",
    "Item",
    "Type",
    "Mode",
    "Attraction_sites"
]

for table in tables:
    print(f"\nTable: {table}")
    df = pd.read_sql(f'SELECT * FROM "{table}" LIMIT 5', conn)
    print(df.columns.tolist())

conn.close()
