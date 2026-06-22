import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

companies = [
    "BANKBARODA",
    "HCLTECH",
    "NESTLEIND",
    "ADANIGREEN",
    "BOSCHLTD"
]

for company in companies:

    query = f"""
    SELECT company_id,
           MIN(year) AS first_year,
           MAX(year) AS last_year,
           COUNT(DISTINCT year) AS total_years
    FROM profitandloss
    WHERE company_id = '{company}'
    """
    df = pd.read_sql(query, conn)
    print("\n", company)
    print(df)

conn.close()