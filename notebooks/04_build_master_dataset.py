import sqlite3
import pandas as pd

conn = sqlite3.connect("tourism.db")


query = """
SELECT
    t.TransactionId,
    t.UserId,
    t.VisitYear,
    t.VisitMonth,
    t.Rating,

    m.VisitMode,

    u.CityId,
    c.CityName,
    co.Country,
    r.Region,
    cont.Continent,

    i.AttractionId,
    i.Attraction,
    i.AttractionAddress,
    ty.AttractionType

FROM "Transaction" t

LEFT JOIN "User" u
    ON t.UserId = u.UserId

LEFT JOIN City c
    ON u.CityId = c.CityId

LEFT JOIN Country co
    ON c.CountryId = co.CountryId

LEFT JOIN Region r
    ON co.RegionId = r.RegionId

LEFT JOIN Continent cont
    ON r.ContinentId = cont.ContinentId

LEFT JOIN Mode m
    ON t.VisitMode = m.VisitModeId

LEFT JOIN Item i
    ON t.AttractionId = i.AttractionId

LEFT JOIN Type ty
    ON i.AttractionTypeId = ty.AttractionTypeId
"""

master_df = pd.read_sql(query, conn)

print("Master dataset shape:", master_df.shape)
print(master_df.head())

conn.close()
