import streamlit as st
import plotly.express as px
from utils.db import *

st.sidebar.header("Filters")

years = ["Mar 2024", "TTM", "Mar 2023", "Mar 2022", "Mar 2021", "Mar 2020"]

selected_year = st.sidebar.selectbox(
    "Select Year",
    years,
    index=0   # Default = Mar 2024
)

st.title("🏠 Home Dashboard")
st.write("Welcome to Nifty100 Financial Intelligence Dashboard")

companies = get_companies()

st.metric("Companies", len(companies))

#KPI Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Companies", len(companies))

with col2:
    st.metric("Sectors", companies["broad_sector"].nunique())

with col3:
    st.metric("Sub Sectors", companies["sub_sector"].nunique())

with col4:
    st.metric("Sub Industries", companies["sub_sector"].nunique())

#Sector Distribution
sector_counts = (
    companies
    .groupby("broad_sector")
    .size()
    .reset_index(name="Count")
)

fig = px.pie(
    sector_counts,
    names="broad_sector",
    values="Count",
    hole=0.5,
    title="Sector Distribution"
)

st.plotly_chart(fig, use_container_width=True)

ratios = get_all_ratios(selected_year)

top5 = (
    ratios
    .sort_values("composite_quality_score", ascending=False)
    .head(5)
)

st.subheader("🏆 Top 5 Quality Companies")

st.dataframe(
    top5[
        [
            "company_id",
            "composite_quality_score",
            "return_on_equity_pct",
            "return_on_capital_employed_pct",
        ]
    ],
    use_container_width=True,
)

