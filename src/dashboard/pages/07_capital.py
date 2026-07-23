import streamlit as st
import pandas as pd
import plotly.express as px
from utils.db import *

st.title("🗺️Capital Allocation Map")

capital = get_capital_allocation()

companies = get_companies()

capital = capital.merge(
    companies[["id", "company_name"]],
    left_on="company_id",
    right_on="id",
    how="left"
)

capital["company_name"] = capital["company_name"].fillna(capital["company_id"])

capital["year_num"] = capital["year"].str[-2:].astype(int)

capital = capital.sort_values("year_num")

capital = capital.drop_duplicates(
    subset=["company_id"],
    keep="last"
)

capital = capital.drop(columns="year_num")


# Parent nodes (patterns)
patterns = pd.DataFrame({
    "name": capital["pattern_label"].unique(),
    "parent": ""
})

# Child nodes (companies)
companies_tree = pd.DataFrame({
    "name": capital["company_name"],
    "parent": capital["pattern_label"]
})

tree = pd.concat([patterns, companies_tree], ignore_index=True)

fig = px.treemap(
    tree,
    names="name",
    parents="parent",
    title="Capital Allocation Map"
)

st.plotly_chart(fig, use_container_width=True)

pattern = st.selectbox(
    "Select Pattern",
    sorted(capital["pattern_label"].unique())
)

filtered = capital[capital["pattern_label"] == pattern]

st.dataframe(
    filtered[
    [
        "company_name",
        "company_id",
        "pattern_label",
        "year"
    ]
]
)