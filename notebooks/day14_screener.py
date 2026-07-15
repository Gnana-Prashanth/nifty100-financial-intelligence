import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql(
    """
    SELECT
        company_id,
        year,
        return_on_equity_pct,
        debt_to_equity
    FROM financial_ratios
    """,
    conn
)

conn.close()

result = df[
    (df["return_on_equity_pct"] > 15)
    &
    (df["debt_to_equity"] < 1)
]

companies = result["company_id"].unique()

print("Total Companies:", len(companies))

print(companies)

result = result.drop_duplicates(subset=["company_id"])
print(result)
print("Total Companies:", len(result))