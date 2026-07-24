import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

ratios = pd.read_excel(
    BASE_DIR / "data" / "supporting" / "financial_ratios.xlsx"
)

ratios["year"] = (
    ratios["year"]
    .str.extract(r'(\d{4})')[0]
    .astype(int)
)

ratios = ratios.drop_duplicates(
    subset=["company_id", "year"],
    keep="last"
)

market = pd.read_excel(
    BASE_DIR / "data" / "supporting" / "market_cap.xlsx"
)

sectors = pd.read_excel("data/supporting/sectors.xlsx")

conn = sqlite3.connect("nifty100.db")
companies = pd.read_sql("SELECT * FROM companies", conn)
conn.close()


valuation = market.merge(
    ratios,
    on=["company_id", "year"],
    how="left"
)

valuation = valuation.merge(
    sectors[
        ["company_id", "broad_sector"]
    ],
    on="company_id",
    how="left"
)

valuation = valuation.merge(
    companies[
        ["id", "company_name"]
    ],
    left_on="company_id",
    right_on="id",
    how="left"
)


#Compute FCF Yield -> FCF / Market Cap × 100
valuation["fcf_yield_pct"] = (
    valuation["free_cash_flow_cr"]
    / valuation["market_cap_crore"]
) * 100


#Compute Sector Median P/E
latest = valuation["year"].max()

latest_df = valuation[
    valuation["year"] == latest
]

sector_pe = (
    latest_df
    .groupby("broad_sector")["pe_ratio"]
    .median()
    .reset_index()
)

sector_pe.rename(
    columns={
        "pe_ratio": "sector_median_pe"
    },
    inplace=True
)


valuation = valuation.merge(
    sector_pe,
    on="broad_sector",
    how="left"
)


#Apply Valuation Flags
def valuation_flag(row):

    pe = row["pe_ratio"]
    median = row["sector_median_pe"]

    if pd.isna(pe) or pd.isna(median):
        return None

    if pe > median * 1.5:
        return "Caution"

    elif pe < median * 0.7:
        return "Discount"

    return "Fair"

valuation["flag"] = valuation.apply(
    valuation_flag,
    axis=1
)

#Calculate 5-Year Median P/E
pe_5yr = (
    valuation.groupby("company_id")["pe_ratio"]
    .median()
    .reset_index(name="5yr_median_PE")
)

valuation = valuation.merge(
    pe_5yr,
    on="company_id",
    how="left"
)

#Calculate PE_vs_sector_median_pct
valuation["PE_vs_sector_median_pct"] = (
    (valuation["pe_ratio"] - valuation["sector_median_pe"])
    / valuation["sector_median_pe"]
) * 100

#Generate valuation_summary.xlsx
summary = valuation[
    [
        "company_id",
        "company_name",
        "broad_sector",
        "pe_ratio",
        "pb_ratio",
        "ev_ebitda",
        "fcf_yield_pct",
        "5yr_median_PE",
        "PE_vs_sector_median_pct",
        "flag"
    ]
]

summary.to_excel(
    "output/valuation_summary.xlsx",
    index=False
)

#Generate valuation_flags.csv
flags = summary[
    summary["flag"].isin(["Caution", "Discount"])
]

flags.to_csv(
    "output/valuation_flags.csv",
    index=False
)