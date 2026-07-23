import streamlit as st
import plotly.express as px

from utils.db import *

st.title("🏭 Sector Analysis")

df = get_screener()

companies = get_companies()

df = df.merge(
    companies[
        [
            "id",
            "company_name",
            "sub_sector",
            "market_cap_category"
        ]
    ],
    left_on="company_id",
    right_on="id",
    how="left"
)

df = df.drop(columns=["id"], errors="ignore")

sector = st.selectbox(
    "Select Sector",
    sorted(df["broad_sector"].dropna().unique().tolist())
)

sector_df = df[
    df["broad_sector"] == sector
]

fig = px.scatter(
    sector_df,
    x="sales",
    y="return_on_equity_pct",
    size="market_cap_crore",
    color="sub_sector",
    hover_name="company_name",
    title=f"{sector} Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


median_df = (
    sector_df[
        [
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
            "net_profit_margin_pct",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "composite_quality_score"
        ]
    ]
    .median()
    .reset_index()
)

median_df.columns = ["Metric", "Median"]

fig = px.bar(
    median_df,
    x="Metric",
    y="Median",
    title=f"{sector} Median KPIs"
)

st.plotly_chart(fig, use_container_width=True)