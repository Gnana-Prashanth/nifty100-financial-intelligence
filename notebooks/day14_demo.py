import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

demo = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    LIMIT 5
    """,
    conn
)

conn.close()

print(demo)