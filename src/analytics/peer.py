import sqlite3
import numpy as np
import pandas as pd

conn = sqlite3.connect("nifty100.db")

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

peer_groups = pd.read_sql(
    "SELECT * FROM peer_groups",
    conn
)

df = ratios.merge(
    peer_groups,
    on="company_id",
    how="left"
)

missing = df["peer_group_name"].isna().sum()

print(f"Companies without peer group : {missing}")

df["peer_group_status"] = df["peer_group_name"].fillna(
    "No peer group assigned"
)

print(
    df[
        [
            "company_id",
            "peer_group_name",
            "peer_group_status"
        ]
    ].head(10)
)


def calculate_percentile_rank(dataframe, metric, lower_is_better=False):
    """
    Calculate percentile rank within each peer group and year.

    lower_is_better=False -> Higher value gets higher percentile.
    lower_is_better=True  -> Lower value gets higher percentile (e.g. D/E).
    """

    percentile = (
        dataframe
        .groupby(["peer_group_name", "year"])[metric]
        .rank(method="average", pct=True)
        * 100
    )

    if lower_is_better:
        percentile = 100 - percentile

    return percentile

metrics = [
    ("ROE", "return_on_equity_pct", False),
    ("ROCE", "return_on_capital_employed_pct", False),
    ("Net Profit Margin", "net_profit_margin_pct", False),
    ("Debt to Equity", "debt_to_equity", True),
    ("Free Cash Flow", "free_cash_flow_cr", False),
    ("PAT CAGR 5yr", "pat_cagr_5yr", False),
    ("Revenue CAGR 5yr", "revenue_cagr_5yr", False),
    ("EPS CAGR 5yr", "eps_cagr_5yr", False),
    ("Interest Coverage", "interest_coverage", False),
    ("Asset Turnover", "asset_turnover", False),
]

peer_percentiles = []

for metric_name, column_name, lower_is_better in metrics:

    percentile = calculate_percentile_rank(
        df,
        column_name,
        lower_is_better
    )

    temp = df[
        [
            "company_id",
            "peer_group_name",
            "year",
            column_name
        ]
    ].copy()

    temp["metric"] = metric_name
    temp["value"] = temp[column_name]
    temp["percentile_rank"] = percentile

    temp = temp.drop(columns=[column_name])

    peer_percentiles.append(temp)


peer_percentiles = pd.concat(
    peer_percentiles,
    ignore_index=True
)

peer_percentiles.rename(
    columns={
        "peer_group_name": "peer_group"
    },
    inplace=True
)

#Remove companies with no peer group
peer_percentiles = peer_percentiles[
    peer_percentiles["peer_group"].notna()
]

print(peer_percentiles.head(20))
print(peer_percentiles.shape)

# de_test = peer_percentiles[
#     peer_percentiles["metric"] == "Debt to Equity"
# ]

# print(
#     de_test[
#         [
#             "company_id",
#             "peer_group",
#             "year",
#             "value",
#             "percentile_rank"
#         ]
#     ]
#     .sort_values(
#         ["peer_group", "year", "value"]
#     )
#     .head(20)
# )

peer_percentiles.to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False
)

conn.commit()
conn.close()

print("peer_percentiles table created successfully!")