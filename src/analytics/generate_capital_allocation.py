import sqlite3
import pandas as pd

from cashflow import capital_allocation_pattern

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql(
    """
    SELECT 
        company_id,
        year,
        operating_activity,
        investing_activity,
        financing_activity
    FROM cashflow
    """,
    conn
)

conn.close()

print(df.head())
print(df.shape)


def get_sign(value):
    if value >= 0:
        return "+"
    else:
        return "-"
    

df["cfo_sign"] = df["operating_activity"].apply(get_sign)
df["cfi_sign"] = df["investing_activity"].apply(get_sign)
df["cff_sign"] = df["financing_activity"].apply(get_sign)

print(df[[
    "company_id",
    "cfo_sign",
    "cfi_sign",
    "cff_sign"
]].head())

df["pattern_label"] = df.apply(
    lambda row: capital_allocation_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"]
    ),
    axis=1
)

print(df[[
    "company_id",
    "year",
    "pattern_label"
]].head(10))


output = df[
    [
        "company_id",
        "year",
        "cfo_sign",
        "cfi_sign",
        "cff_sign",
        "pattern_label"
    ]
]

output.to_csv(
    "output/capital_allocation.csv",
    index=False
)

print("\ncapital_allocation.csv generated successfully!")

print(output.head())
print(output.shape)