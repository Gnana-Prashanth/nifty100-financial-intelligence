import pandas as pd
import sqlite3
import yaml

with open("config/screener_config.yaml", "r") as file:
    config = yaml.safe_load(file)

print(config)

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

sectors = pd.read_sql(
    "SELECT company_id, broad_sector FROM sectors",
    conn
)

# df = df.merge(
#     sectors,
#     on="company_id",
#     how="left"
# )

market_cap = pd.read_sql(
    """
    SELECT
        company_id,
        market_cap_crore,
        pe_ratio,
        pb_ratio,
        dividend_yield_pct
    FROM market_cap
    """,
    conn
)

df = df.merge(
    market_cap,
    on="company_id",
    how="left"
)

conn.close()

print(df.shape)

print(df[
    [
        "company_id",
        "market_cap_crore",
        "pe_ratio",
        "pb_ratio",
        "dividend_yield_pct"
    ]
].head())

print(df.columns.tolist())


def apply_filters(
    df,
    roe_min=None,
    de_max=None,
    fcf_min=None,
    revenue_cagr_min=None,
    pat_cagr_min=None,
    opm_min=None,
    icr_min=None,
    asset_turnover_min=None,
    sales_min=None,

    pe_max=None,
    pb_max=None,
    dividend_yield_min=None,
    market_cap_min=None
):

    result = df.copy()

    if roe_min is not None:
        result = result[
            result["return_on_equity_pct"] >= roe_min
        ]

    if de_max is not None:
        
        financial = result[
        result["broad_sector"]
        .str.contains("Financial", case=False, na=False)
    ]
        
        non_financial = result[
        ~result["broad_sector"]
        .str.contains("Financial", case=False, na=False)
    ]
        
        non_financial = non_financial[
        non_financial["debt_to_equity"] <= de_max
    ]
        
        result = pd.concat(
        [
            financial,
            non_financial
        ]
    )

    if fcf_min is not None:
        result = result[
            result["free_cash_flow_cr"] >= fcf_min
        ]

    if revenue_cagr_min is not None:
        result = result[
            result["revenue_cagr_5yr"] >= revenue_cagr_min
        ]

    if pat_cagr_min is not None:
        result = result[
            result["pat_cagr_5yr"] >= pat_cagr_min
        ]

    if opm_min is not None:
        result = result[
            result["operating_profit_margin_pct"] >= opm_min
        ]

    if icr_min is not None:
        result = result[
        (
            result["interest_coverage"] >= icr_min
        )
        |
        (
            result["interest_coverage"].isna()
        )
    ]

    if asset_turnover_min is not None:
        result = result[
            result["asset_turnover"] >= asset_turnover_min
        ]

    if sales_min is not None:
        result = result[
            result["sales"] >= sales_min
        ]

    if pe_max is not None:
      result = result[
            result["pe_ratio"] <= pe_max
        ]

    if pb_max is not None:
        result = result[
            result["pb_ratio"] <= pb_max
        ]

    if dividend_yield_min is not None:
        result = result[
            result["dividend_yield_pct"] >= dividend_yield_min
        ]

    if market_cap_min is not None:
        result = result[
            result["market_cap_crore"] >= market_cap_min
        ]

    result = result.sort_values(
    by="composite_quality_score",
    ascending=False
)

    return result


filtered = apply_filters(
    df,

    roe_min=config["filters"]["roe_min"],
    de_max=config["filters"]["de_max"],
    fcf_min=config["filters"]["fcf_min"],
    revenue_cagr_min=config["filters"]["revenue_cagr_min"],
    pat_cagr_min=config["filters"]["pat_cagr_min"],
    opm_min=config["filters"]["opm_min"],
    icr_min=config["filters"]["icr_min"],
    asset_turnover_min=config["filters"]["asset_turnover_min"],
    sales_min=config["filters"]["sales_min"],

    pe_max=config["filters"]["pe_max"],
    pb_max=config["filters"]["pb_max"],
    dividend_yield_min=config["filters"]["dividend_yield_min"],
    market_cap_min=config["filters"]["market_cap_min"],
)

print(filtered.head())

print("\nRows:", len(filtered))