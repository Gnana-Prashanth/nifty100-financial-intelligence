import streamlit as st
import plotly.express as px
from utils.db import *

st.title("🏢 Company Profile")

companies = get_companies()

company_list = companies["company_name"].tolist()

selected_company = st.selectbox(
    "Search Company",
    company_list
)

company = companies[
    companies["company_name"] == selected_company
].iloc[0]

ticker = company["id"]

st.subheader(company["company_name"])

col1, col2 = st.columns([1, 3])

with col1:
    if company["company_logo"]:
        st.image(company["company_logo"], width=120)
    else:
        st.info("No Logo")

with col2:
    st.write(f"**Ticker:** {company['id']}")
    st.write(f"**Sector:** {company['broad_sector']}")
    st.write(f"**Sub Sector:** {company['sub_sector']}")
    st.write(f"**Market Cap:** {company['market_cap_category']}")

#KPI Cards
ratios = get_ratios(ticker)
years = ratios["year"].dropna().unique().tolist()

if "Mar 2024" in years:
    years.remove("Mar 2024")
    years.insert(0, "Mar 2024")

selected_year = st.selectbox(
    "Select Year",
    years,
    index=0
)

def fmt(value, suffix=""):
    if value is None or str(value) == "nan":
        return "N/A"
    return f"{value:.2f}{suffix}"

selected_ratio = ratios[ratios["year"] == selected_year]

if selected_ratio.empty:
    st.warning("No data available for the selected year.")
    st.stop()

ratio = selected_ratio.iloc[0]


st.subheader("📊 Key Performance Indicators")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "ROE",
        fmt(ratio["return_on_equity_pct"], "%")
    )

with col2:
    st.metric(
        "ROCE",
        fmt(ratio["return_on_capital_employed_pct"], "%")
    )

with col3:
    st.metric(
        "Net Profit Margin",
        fmt(ratio["net_profit_margin_pct"], "%")
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Debt to Equity",
        fmt(ratio["debt_to_equity"])
    )

with col5:
    st.metric(
        "Interest Coverage",
        fmt(ratio["interest_coverage"])
    )

with col6:
    st.metric(
        "Quality Score",
        fmt(ratio["composite_quality_score"])
    )


#Revenue & Net Profit Trend
chart_df = (
    ratios[ratios["year"] != "TTM"]
    .sort_values("year")
)

fig = px.line(
    chart_df,
    x="year",
    y="sales",
    markers=True,
    title="Revenue Trend"
)

st.plotly_chart(fig, use_container_width=True)

fig = px.line(
    chart_df,
    x="year",
    y="net_profit",
    markers=True,
    title="Net Profit Trend"
)

st.plotly_chart(fig, use_container_width=True)

#ROE & ROCE Trend
fig = px.line(
    chart_df,
    x="year",
    y=[
        "return_on_equity_pct",
        "return_on_capital_employed_pct"
    ],
    markers=True,
    title="ROE vs ROCE Trend"
)

st.plotly_chart(fig, use_container_width=True)

#Pros & Cons
st.subheader("👍 Pros & 👎 Cons")

pros_cons = get_pros_cons(ticker)

if pros_cons.empty:
    st.info("No Pros & Cons available.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👍 Pros")

        for pro in pros_cons["pros"].dropna():
            if str(pro).strip():
                st.success(pro)

    with col2:
        st.markdown("### 👎 Cons")

        for con in pros_cons["cons"].dropna():
            if str(con).strip():
                st.error(con)

