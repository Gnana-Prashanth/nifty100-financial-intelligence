import streamlit as st
import plotly.graph_objects as go

from utils.db import *

st.title("📈 Trend Analysis")

companies = get_companies()

selected_company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

company = companies[
    companies["company_name"] == selected_company
].iloc[0]

ticker = company["id"]

ratios = get_ratios(ticker)

ratios = ratios.sort_values("year")

ratios = ratios[ratios["year"] != "TTM"]

metric_labels = {
    "sales": "Sales",
    "net_profit": "Net Profit",
    "operating_profit_margin_pct": "OPM %",
    "net_profit_margin_pct": "NPM %",
    "return_on_equity_pct": "ROE %",
    "return_on_capital_employed_pct": "ROCE %",
    "debt_to_equity": "Debt/Equity",
    "interest_coverage": "Interest Coverage",
    "free_cash_flow_cr": "Free Cash Flow",
    "revenue_cagr_5yr": "Revenue CAGR (5Y)",
    "pat_cagr_5yr": "PAT CAGR (5Y)"
}

selected_metrics = st.multiselect(
    "Select up to 3 metrics",
    options=list(metric_labels.keys()),
    default=["sales"],
    format_func=lambda x: metric_labels[x],
    max_selections=3
)

# # Uncomment if metrics need normalization for comparison
# plot_df = ratios.copy()

# for metric in selected_metrics:
#     col = plot_df[metric]

#     # Skip normalization if all values are same
#     if col.max() != col.min():
#         plot_df[metric] = (col - col.min()) / (col.max() - col.min())

for metric in selected_metrics:
    yoy = ratios[metric].pct_change() * 100


fig = go.Figure()

for metric in selected_metrics:

    fig.add_trace(
        go.Scatter(
            x=ratios["year"], # Replace ratios → plot_df if normalization is needed
            y=ratios[metric], # Replace ratios → plot_df if normalization is needed
            mode="lines+markers",
            name=metric_labels[metric]
        )
    )

    yoy = ratios[metric].pct_change() * 100

    for x, y, pct in zip(
        ratios["year"], # Replace ratios → plot_df if normalization is needed
        ratios[metric], # Replace ratios → plot_df if normalization is needed
        yoy
    ):

        if pd.notna(pct):

            fig.add_annotation(
                x=x,
                y=y,
                text=f"{pct:+.1f}%",
                showarrow=False,
                yshift=12,
                font=dict(size=9)
            )

fig.update_layout(
    title="10-Year Trend Analysis",
    xaxis_title="Year",
    yaxis_title="Value",
    hovermode="x unified",
    legend_title="Metrics"
)

st.plotly_chart(
    fig,
    use_container_width=True
)