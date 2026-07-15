import sqlite3
import pandas as pd
import os

# ----------------------------
# Connect Database
# ----------------------------
conn = sqlite3.connect("nifty100.db")

companies = pd.read_sql("SELECT * FROM companies", conn)
financial_ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
sectors = pd.read_sql("SELECT * FROM sectors", conn)

conn.close()

# ----------------------------
# Merge Data
# ----------------------------
companies_small = companies[
    [
        "id",
        "roce_percentage",
        "roe_percentage"
    ]
].rename(columns={"id": "company_id"})

df = financial_ratios.merge(
    companies_small,
    on="company_id",
    how="left"
)

df = df.merge(
    sectors[
        [
            "company_id",
            "broad_sector"
        ]
    ],
    on="company_id",
    how="left"
)

# ----------------------------
# Task 1
# Financial Sector Carve-Out
# ----------------------------
financial_mask = df["broad_sector"].str.contains(
    "Financial",
    case=False,
    na=False
)

print("\nFinancial Companies:")
print(df.loc[financial_mask, ["company_id", "broad_sector"]].drop_duplicates())

# ----------------------------
# Task 2
# High Leverage Warning
# ----------------------------
df["high_leverage_flag"] = (
    df["debt_to_equity"] > 5
)

df["de_warning"] = df["high_leverage_flag"]

df.loc[
    financial_mask,
    "de_warning"
] = False

# ----------------------------
# Task 3
# ROCE Cross Check
# ----------------------------
df["roce_difference"] = (
    abs(
        df["return_on_capital_employed_pct"]
        - df["roce_percentage"]
    )
)

# ----------------------------
# Task 4
# ROE Cross Check
# ----------------------------
df["roe_difference"] = (
    abs(
        df["return_on_equity_pct"]
        - df["roe_percentage"]
    )
)

# ----------------------------
# Task 5
# Categorise
# ----------------------------
def categorise(row):

    if row["roce_difference"] > 5:
        return "Formula Discrepancy"

    if row["roe_difference"] > 5:
        return "Data Source Issue"

    return "OK"


df["category"] = df.apply(
    categorise,
    axis=1
)

# ----------------------------
# Task 6
# Edge Cases
# ----------------------------
edge_cases = df[
    (df["roce_difference"] > 5)
    |
    (df["roe_difference"] > 5)
]

# ----------------------------
# Save Log
# ----------------------------
os.makedirs("output", exist_ok=True)

edge_cases[
    [
        "company_id",
        "year",
        "return_on_capital_employed_pct",
        "roce_percentage",
        "roce_difference",
        "return_on_equity_pct",
        "roe_percentage",
        "roe_difference",
        "category"
    ]
].to_csv(
    "output/ratio_edge_cases.log",
    index=False
)

# ----------------------------
# Summary
# ----------------------------
print("\n========== SUMMARY ==========")

print(
    "Financial Companies :",
    financial_mask.sum()
)

print(
    "ROCE Differences >5 :",
    (df["roce_difference"] > 5).sum()
)

print(
    "ROE Differences >5 :",
    (df["roe_difference"] > 5).sum()
)

print(
    "Total Edge Cases :",
    len(edge_cases)
)

print(
    "\nSaved to : output/ratio_edge_cases.log"
)