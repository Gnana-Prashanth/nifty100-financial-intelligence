import streamlit as st
import pandas as pd
from utils.db import get_screener
from src.screener.engine import apply_filters

st.title("🔎 Stock Screener")

df = get_screener()

st.sidebar.header("🚀 Quick Presets")

quality = st.sidebar.button("⭐ Quality")
value = st.sidebar.button("💰 Value")
growth = st.sidebar.button("📈 Growth")
dividend = st.sidebar.button("💵 Dividend")
debt_free = st.sidebar.button("🛡️ Debt-Free")
turnaround = st.sidebar.button("🔄 Turnaround")

st.sidebar.header("🎯 Filters")

roe_min = st.sidebar.slider(
    "Minimum ROE (%)",
    float(df["return_on_equity_pct"].min()),
    float(df["return_on_equity_pct"].max()),
    0.0
)

de_max = st.sidebar.slider(
    "Maximum Debt to Equity",
    float(df["debt_to_equity"].min()),
    float(df["debt_to_equity"].max()),
    float(df["debt_to_equity"].max())
)

fcf_min = st.sidebar.slider(
    "Minimum Free Cash Flow",
    float(df["free_cash_flow_cr"].min()),
    float(df["free_cash_flow_cr"].max()),
    float(df["free_cash_flow_cr"].min())
)

revenue_cagr_min = st.sidebar.slider(
    "Minimum Revenue CAGR",
    float(df["revenue_cagr_5yr"].min()),
    float(df["revenue_cagr_5yr"].max()),
    float(df["revenue_cagr_5yr"].min())
)

pat_cagr_min = st.sidebar.slider(
    "Minimum PAT CAGR",
    float(df["pat_cagr_5yr"].min()),
    float(df["pat_cagr_5yr"].max()),
    float(df["pat_cagr_5yr"].min())
)

opm_min = st.sidebar.slider(
    "Minimum OPM",
    float(df["operating_profit_margin_pct"].min()),
    float(df["operating_profit_margin_pct"].max()),
    float(df["operating_profit_margin_pct"].min())
)

pe_max = st.sidebar.slider(
    "Maximum PE",
    float(df["pe_ratio"].min()),
    float(df["pe_ratio"].max()),
    float(df["pe_ratio"].max())
)

pb_max = st.sidebar.slider(
    "Maximum PB",
    float(df["pb_ratio"].min()),
    float(df["pb_ratio"].max()),
    float(df["pb_ratio"].max())
)

dividend_yield_min = st.sidebar.slider(
    "Minimum Dividend Yield",
    float(df["dividend_yield_pct"].min()),
    float(df["dividend_yield_pct"].max()),
    float(df["dividend_yield_pct"].min())
)

icr_min = st.sidebar.slider(
    "Minimum Interest Coverage",
    float(df["interest_coverage"].fillna(0).min()),
    float(df["interest_coverage"].fillna(0).max()),
    0.0
)

#Override slider values if a preset is clicked
if quality:
    roe_min = 20
    de_max = 0.5
    revenue_cagr_min = 10
    pat_cagr_min = 10
    opm_min = 15
    icr_min = 5

if quality:
    roe_min = 20
    de_max = 0.5
    revenue_cagr_min = 10
    pat_cagr_min = 10
    opm_min = 15
    icr_min = 5

if growth:
    revenue_cagr_min = 15
    pat_cagr_min = 15

if dividend:
    dividend_yield_min = 2

if debt_free:
    de_max = 0

if turnaround:
    revenue_cagr_min = 5
    pat_cagr_min = 5
    opm_min = 5


filtered = apply_filters(
    df,
    roe_min=roe_min,
    de_max=de_max,
    fcf_min=fcf_min,
    revenue_cagr_min=revenue_cagr_min,
    pat_cagr_min=pat_cagr_min,
    opm_min=opm_min,
    icr_min=icr_min,
    pe_max=pe_max,
    pb_max=pb_max,
    dividend_yield_min=dividend_yield_min
)

st.subheader(f"📈 {len(filtered)} companies match your filters")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Results",
    data=csv,
    file_name="screened_companies.csv",
    mime="text/csv"
)

st.dataframe(
    filtered[
        [
            "company_id",
            "broad_sector",
            "composite_quality_score",
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "pe_ratio",
            "pb_ratio",
            "dividend_yield_pct",
        ]
    ],
    use_container_width=True
)

# TODO: Replace simple preset button logic with st.session_state
# so preset buttons update both filter values and slider positions.
# Current implementation is functionally correct.
# Refactor later for a better portfolio/demo if time permits.