import streamlit as st
import plotly.graph_objects as go
from utils.db import *

st.title("🤝 Peer Comparison")

peers = get_peer_groups()

peer_groups = sorted(
    peers["peer_group_name"].unique().tolist()
)

selected_group = st.selectbox(
    "Select Peer Group",
    peer_groups
)

group_df = peers[
    peers["peer_group_name"] == selected_group
]

# st.subheader(f"Companies in {selected_group}")

# st.dataframe(group_df)

benchmark = group_df[
    group_df["is_benchmark"] == 1
].iloc[0]["company_id"]

st.success(f"Benchmark Company : {benchmark}")

group_df = peers[
    peers["peer_group_name"] == selected_group
]

screener = get_screener()

peer_data = group_df.merge(
    screener,
    on="company_id",
    how="left"
)

benchmark = peer_data[
    peer_data["is_benchmark"] == 1
].iloc[0]

metrics = [
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "interest_coverage",
    "composite_quality_score",
    "sector_relative_score"
]

peer_avg = peer_data[metrics].mean()


fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=benchmark[metrics].values,
        theta=metrics,
        fill="toself",
        name=benchmark["company_id"]
    )
)

fig.add_trace(
    go.Scatterpolar(
        r=peer_avg.values,
        theta=metrics,
        fill="toself",
        name="Peer Average"
    )
)

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)

cols = [
    "company_id",
    "return_on_equity_pct",
    "return_on_capital_employed_pct",
    "net_profit_margin_pct",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "composite_quality_score"
]

st.dataframe(
    peer_data[cols],
    use_container_width=True
)

def highlight_benchmark(row):
    if row["company_id"] == benchmark["company_id"]:
        return ["background-color: lightgreen"] * len(row)
    return [""] * len(row)

st.dataframe(
    peer_data[cols]
        .style
        .apply(highlight_benchmark, axis=1)
)

# TODO: The radar chart is technically correct, but one metric (interest_coverage) has values in the hundreds or thousands, while most other metrics are between 0–100. That causes it to dominate the chart.
# A better version later would normalize each metric before plotting (e.g., Min-Max scaling or percentage of peer maximum).