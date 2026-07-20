#Import the Engine
import sqlite3
import pandas as pd

from engine import apply_filters

#Load Database
conn = sqlite3.connect("nifty100.db")

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

market_cap = pd.read_sql(
    "SELECT * FROM market_cap",
    conn
)

# sectors = pd.read_sql(
#     "SELECT company_id,broad_sector FROM sectors",
#     conn
# )

conn.close()

#Merge
df = financial_ratios.merge(
    market_cap,
    on="company_id",
    how="left"
)

# df = df.merge(
#     sectors,
#     on="company_id",
#     how="left"
# )
print(sorted(df.columns.tolist()))

#Quality Screener
quality = apply_filters(
    df,

    roe_min=18,
    de_max=1,

    opm_min=15,

    revenue_cagr_min=10,

    icr_min=3
)

print(quality.head())

quality.to_csv(
    "output/quality_screener.csv",
    index=False
)

#Growth Screener
growth = apply_filters(
    df,

    revenue_cagr_min=15,

    pat_cagr_min=15,

    roe_min=15
)

growth.to_csv(
    "output/growth_screener.csv",
    index=False
)

#Test
print("Quality :", len(quality))
print("Growth :", len(growth))


#Value Screener
value = apply_filters(
    df,

    roe_min=15,
    de_max=1,

    pe_max=20,
    pb_max=3
)

value.to_csv(
    "output/value_screener.csv",
    index=False
)

print("Value :", len(value))

#Dividend Screener
dividend = apply_filters(
    df,

    dividend_yield_min=2,

    fcf_min=0,

    de_max=1,

    icr_min=3
)

dividend.to_csv(
    "output/dividend_screener.csv",
    index=False
)

print("Dividend :", len(dividend))

#Turnaround Screener
turnaround = apply_filters(
    df,

    revenue_cagr_min=5,

    pat_cagr_min=5,

    fcf_min=0,

    icr_min=2
)

turnaround.to_csv(
    "output/turnaround_screener.csv",
    index=False
)

print("Turnaround :", len(turnaround))

#Compound Screener
compounder = apply_filters(
    df,

    roe_min=20,

    revenue_cagr_min=15,

    pat_cagr_min=15,

    de_max=0.5,

    opm_min=20,

    icr_min=5
)

compounder.to_csv(
    "output/compounder_screener.csv",
    index=False
)

print("Compounder :", len(compounder))


print("\n========== PRESET SCREENER SUMMARY ==========")

print(f"Quality      : {len(quality)} companies")
print(f"Growth       : {len(growth)} companies")
print(f"Value        : {len(value)} companies")
print(f"Dividend     : {len(dividend)} companies")
print(f"Turnaround   : {len(turnaround)} companies")
print(f"Compounder   : {len(compounder)} companies")