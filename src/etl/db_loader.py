import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

df.to_sql(
    "companies",
    conn,
    if_exists="append",
    index=False
)

print("Companies loaded!")

conn.close()