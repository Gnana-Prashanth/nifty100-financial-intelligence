import sqlite3
import pandas as pd

from ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    return_on_capital_employed,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover
)

from cashflow import (
    free_cash_flow,
    capex_intensity,
    fcf_conversion_rate
)

from cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr
)

conn = sqlite3.connect("nifty100.db")

profit = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

balance = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

cash = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

conn.close()

print(profit.shape)
print(balance.shape)
print(cash.shape)


df = profit.merge(
    balance,
    on=["company_id","year"],
    how="left"
)

df = df.merge(
    cash,
    on=["company_id","year"],
    how="left"
)

print(df.shape)
print(df.columns)


df["net_profit_margin_pct"] = df.apply(
    lambda row: net_profit_margin(
        row["net_profit"],
        row["sales"]
    ),
    axis=1
)

print(
    df[
        [
            "company_id",
            "year",
            "net_profit_margin_pct"
        ]
    ].head()
)

df["operating_profit_margin_pct"] = df.apply(
    lambda row: operating_profit_margin(
        row["operating_profit"],
        row["sales"]
    ),
    axis=1
)

df["return_on_equity_pct"] = df.apply(
    lambda row: return_on_equity(
        row["net_profit"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)

#------------------ROCE13-----------------------
df["return_on_capital_employed_pct"] = df.apply(
    lambda row: return_on_capital_employed(
        row["operating_profit"],
        row["equity_capital"],
        row["reserves"],
        row["borrowings"]
    ),
    axis=1
)

print(
    df[
        [
            "company_id",
            "year",
            "return_on_capital_employed_pct"
        ]
    ].head(10)
)

conn = sqlite3.connect("nifty100.db")

df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("financial_ratios updated successfully!")

conn = sqlite3.connect("nifty100.db")

financial_ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

print(financial_ratios.columns.tolist())
#---------------ROCE13--------------------------

df["debt_to_equity"] = df.apply(
    lambda row: debt_to_equity(
        row["borrowings"],
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)

df["interest_coverage"] = df.apply(
    lambda row: interest_coverage_ratio(
        row["operating_profit"],
        row["other_income"],
        row["interest"]
    ),
    axis=1
)

df["asset_turnover"] = df.apply(
    lambda row: asset_turnover(
        row["sales"],
        row["total_assets"]
    ),
    axis=1
)

df["free_cash_flow_cr"] = df.apply(
    lambda row: free_cash_flow(
        row["operating_activity"],
        row["investing_activity"]
    ),
    axis=1
)

print(df[
    [
        "company_id",
        "year",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr"
    ]
].head(10))

df["total_debt_cr"] = df["borrowings"]

df["cash_from_operations_cr"] = df["operating_activity"]

df["earnings_per_share"] = df["eps"]

df["dividend_payout_ratio_pct"] = df["dividend_payout"]


def book_value_per_share(equity_capital, reserves):
    if equity_capital == 0:
        return None
    return (equity_capital + reserves) / equity_capital

df["book_value_per_share"] = df.apply(
    lambda row: book_value_per_share(
        row["equity_capital"],
        row["reserves"]
    ),
    axis=1
)

print(df[[
    "company_id",
    "year",
    "book_value_per_share"
]].head())

# abb = df[df["company_id"] == "ABB"][
#     ["company_id", "year", "sales", "net_profit", "eps"]]
# print(abb.head(10))

df = df.sort_values(
    by=["company_id", "year"]
)


df["revenue_cagr_5yr"] = None
df["revenue_cagr_5yr_flag"] = None

for company, group in df.groupby("company_id"):
    group = group.reset_index()
    for i in range(len(group)):        
        if i < 5:
            continue

        start_sales = group.loc[i - 5, "sales"]
        end_sales = group.loc[i, "sales"]

        cagr, flag = revenue_cagr(
            start_sales,
            end_sales,
            5,
            5
        )

        original_index = group.loc[i, "index"]

        df.loc[
            original_index,
            "revenue_cagr_5yr"
        ] = cagr

        df.loc[
            original_index,
            "revenue_cagr_5yr_flag"
        ] = flag

print(
    df[
        [
            "company_id",
            "year",
            "sales",
            "revenue_cagr_5yr",
            "revenue_cagr_5yr_flag"
        ]
    ].tail(20)
)



df["pat_cagr_5yr"] = None
df["pat_cagr_5yr_flag"] = None

for company, group in df.groupby("company_id"):
    group = group.reset_index()
    for i in range(len(group)):
        if i < 5:
            continue

        start_pat = group.loc[i - 5, "net_profit"]
        end_pat = group.loc[i, "net_profit"]

        cagr, flag = pat_cagr(
            start_pat,
            end_pat,
            5,
            5
        )

        original_index = group.loc[i, "index"]

        df.loc[original_index, "pat_cagr_5yr"] = cagr
        df.loc[original_index, "pat_cagr_5yr_flag"] = flag



df["eps_cagr_5yr"] = None
df["eps_cagr_5yr_flag"] = None

for company, group in df.groupby("company_id"):
    group = group.reset_index()
    for i in range(len(group)):
        if i < 5:
            continue

        start_eps = group.loc[i - 5, "eps"]
        end_eps = group.loc[i, "eps"]

        cagr, flag = eps_cagr(
            start_eps,
            end_eps,
            5,
            5
        )

        original_index = group.loc[i, "index"]

        df.loc[original_index, "eps_cagr_5yr"] = cagr
        df.loc[original_index, "eps_cagr_5yr_flag"] = flag



def composite_quality_score(row):
    score = 0

    # ROE
    if row["return_on_equity_pct"] is not None and row["return_on_equity_pct"] > 15:
        score += 1

    # Net Profit Margin
    if row["net_profit_margin_pct"] is not None and row["net_profit_margin_pct"] > 10:
        score += 1

    # Debt to Equity
    if row["debt_to_equity"] is not None and row["debt_to_equity"] < 1:
        score += 1

    # Interest Coverage
    if row["interest_coverage"] is not None and row["interest_coverage"] > 3:
        score += 1

    # Revenue CAGR
    if row["revenue_cagr_5yr"] is not None and row["revenue_cagr_5yr"] > 10:
        score += 1

    return score

df["composite_quality_score"] = df.apply(
    composite_quality_score,
    axis=1
)

print(df[
    [
        "company_id",
        "year",
        "composite_quality_score"
    ]
].head(10))


conn = sqlite3.connect("nifty100.db")

df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("\nfinancial_ratios table updated successfully!")


conn = sqlite3.connect("nifty100.db")

count = pd.read_sql(
    "SELECT COUNT(*) AS total FROM financial_ratios",
    conn
)

print(count)

conn.close()


#Manual Spot Check
#Choosing any 3 companies

print(df[df["company_id"]=="ABB"][
    [
        "company_id",
        "year",
        "return_on_equity_pct",
        "revenue_cagr_5yr"
    ]
].tail())

print(df[df["company_id"]=="TCS"][
    [
        "company_id",
        "year",
        "return_on_equity_pct",
        "revenue_cagr_5yr"
    ]
].tail())

print(df[df["company_id"]=="INFY"][
    [
        "company_id",
        "year",
        "return_on_equity_pct",
        "revenue_cagr_5yr"
    ]
].tail())