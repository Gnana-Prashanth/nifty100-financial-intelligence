import sqlite3
import numpy as np
import pandas as pd


# -----------------------------
# Database Connection
# -----------------------------
conn = sqlite3.connect("nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)


# -----------------------------
# Helper Functions
# -----------------------------
def winsorize(series):
    """Clip values between 10th and 90th percentile."""
    lower = series.quantile(0.10)
    upper = series.quantile(0.90)
    return series.clip(lower, upper)


def normalize(series, reverse=False):
    """Normalize values to 0-100."""

    series = pd.to_numeric(series, errors="coerce")
    series = winsorize(series)

    minimum = series.min()
    maximum = series.max()

    if pd.isna(minimum) or pd.isna(maximum) or minimum == maximum:
        return pd.Series(50, index=series.index)

    score = (series - minimum) / (maximum - minimum) * 100

    if reverse:
        score = 100 - score

    return score


# -----------------------------
# Individual Metric Scores
# -----------------------------

# Profitability
df["roe_score"] = normalize(
    df["return_on_equity_pct"]
)

df["roce_score"] = normalize(
    df["return_on_capital_employed_pct"]
)

df["npm_score"] = normalize(
    df["net_profit_margin_pct"]
)


# Cash Quality
df["fcf_cagr_score"] = normalize(
    df["fcf_cagr_5yr"]
)

df["cfo_pat_score"] = normalize(
    df["cfo_pat_ratio"]
)

df["positive_fcf_score"] = np.where(
    df["free_cash_flow_cr"] > 0,
    100,
    0
)


# Growth
df["revenue_growth_score"] = normalize(
    df["revenue_cagr_5yr"]
)

df["pat_growth_score"] = normalize(
    df["pat_cagr_5yr"]
)


# Leverage
df["de_score"] = normalize(
    df["debt_to_equity"],
    reverse=True
)

df["icr_score"] = normalize(
    df["interest_coverage"]
)


# -----------------------------
# Category Scores
# -----------------------------

df["profitability_score"] = (
      df["roe_score"] * 0.15
    + df["roce_score"] * 0.10
    + df["npm_score"] * 0.10
)

df["cash_quality_score"] = (
      df["fcf_cagr_score"] * 0.15
    + df["cfo_pat_score"] * 0.10
    + df["positive_fcf_score"] * 0.05
)

df["growth_score"] = (
      df["revenue_growth_score"] * 0.10
    + df["pat_growth_score"] * 0.10
)

df["leverage_score"] = (
      df["de_score"] * 0.10
    + df["icr_score"] * 0.05
)


# -----------------------------
# Final Composite Score
# -----------------------------

df["composite_quality_score"] = (
      df["profitability_score"]
    + df["cash_quality_score"]
    + df["growth_score"]
    + df["leverage_score"]
)


# -----------------------------
# Sector Relative Score
# -----------------------------

if "broad_sector" in df.columns:
    sector_col = "broad_sector"
elif "broad_sector_x" in df.columns:
    sector_col = "broad_sector_x"
elif "broad_sector_y" in df.columns:
    sector_col = "broad_sector_y"
else:
    sector_col = None

if sector_col:
    df["sector_relative_score"] = (
        df.groupby(sector_col)["composite_quality_score"]
          .transform(normalize)
    )
else:
    df["sector_relative_score"] = normalize(
        df["composite_quality_score"]
    )


# -----------------------------
# Save
# -----------------------------

df = df.sort_values(
    "composite_quality_score",
    ascending=False
)

df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("Composite quality score generated successfully.")