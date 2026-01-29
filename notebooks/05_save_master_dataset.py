import sqlite3
import pandas as pd
from pathlib import Path

# --- Resolve project root safely ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data" / "cleaned"
DATA_DIR.mkdir(parents=True, exist_ok=True)  # <-- critical fix

OUTPUT_FILE = DATA_DIR / "master_dataset.csv"

# --- Connect to DB ---
conn = sqlite3.connect("tourism.db")


query = """
SELECT
    t.TransactionId,
    t.UserId,
    t.VisitYear,
    t.VisitMonth,
    t.Rating,
    m.VisitMode,
    c.CityName,
    co.Country,
    r.Region,
    cont.Continent,
    i.Attraction,
    ty.AttractionType
FROM "Transaction" t
LEFT JOIN "User" u ON t.UserId = u.UserId
LEFT JOIN City c ON u.CityId = c.CityId
LEFT JOIN Country co ON c.CountryId = co.CountryId
LEFT JOIN Region r ON co.RegionId = r.RegionId
LEFT JOIN Continent cont ON r.ContinentId = cont.ContinentId
LEFT JOIN Mode m ON t.VisitMode = m.VisitModeId
LEFT JOIN Item i ON t.AttractionId = i.AttractionId
LEFT JOIN Type ty ON i.AttractionTypeId = ty.AttractionTypeId
"""

df = pd.read_sql(query, conn)

df.to_csv(OUTPUT_FILE, index=False)

print("✅ Master dataset saved successfully")
print("📍 Location:", OUTPUT_FILE)
print("📐 Shape:", df.shape)

conn.close()
