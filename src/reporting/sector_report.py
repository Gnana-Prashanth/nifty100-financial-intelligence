import pandas as pd
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

BASE_DIR = Path(__file__).resolve().parents[2]

ratios = pd.read_excel(
    BASE_DIR / "data/supporting/financial_ratios.xlsx"
)

sectors = pd.read_excel(
    BASE_DIR / "data/supporting/sectors.xlsx"
)

ratios = ratios[
    ratios["year"].astype(str).str.strip() != "TTM"
].copy()
latest = (
    ratios
    .sort_values(["company_id", "year"])
    .groupby("company_id")
    .tail(1)
    .reset_index(drop=True)
)

latest = (
    ratios
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
    .reset_index(drop=True)
)

latest = latest.merge(
    sectors[
        [
            "company_id",
            "broad_sector"
        ]
    ],
    on="company_id",
    how="left"
)

latest = latest.loc[:, ~latest.columns.duplicated()]


styles = getSampleStyleSheet()

def generate_sector_report(sector_name):

    sector_df = latest[
        latest["broad_sector"] == sector_name
    ].copy()

    output = (
        BASE_DIR
        / "reports"
        / "sector"
        / f"{sector_name}_report.pdf"
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    doc = SimpleDocTemplate(
        str(output),
        pagesize=A4
    )

    story = []

    # Title
    story.append(
        Paragraph(
            f"<b>{sector_name} Sector Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # Median KPI Summary
    summary = [
        ["Median Revenue", f"{sector_df['sales'].median():,.0f}"],
        ["Median Net Profit", f"{sector_df['net_profit'].median():,.0f}"],
        ["Median ROE", f"{sector_df['return_on_equity_pct'].median():.2f}%"],
        ["Median ROCE", f"{sector_df['return_on_capital_employed_pct'].median():.2f}%"],
        ["Median Debt/Equity", f"{sector_df['debt_to_equity'].median():.2f}"]
    ]

    summary_table = Table(summary)

    summary_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(summary_table)

    story.append(Spacer(1, 20))

    # Company Table
    table = [[
        "Company",
        "Revenue",
        "Net Profit",
        "ROE",
        "ROCE",
        "D/E",
        "Composite",
        "FCF CAGR"
    ]]

    for _, row in sector_df.iterrows():

        table.append([
            row["company_id"],
            f"{row['sales']:,.0f}",
            f"{row['net_profit']:,.0f}",
            f"{row['return_on_equity_pct']:.2f}",
            f"{row['return_on_capital_employed_pct']:.2f}",
            f"{row['debt_to_equity']:.2f}",
            f"{row['composite_quality_score']:.2f}",
            f"{row['fcf_cagr_5yr']:.2f}"
        ])

    company_table = Table(table)

    company_table.setStyle(
        TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
        ])
    )

    story.append(company_table)

    doc.build(story)

    print(f"Generated {sector_name}")


if __name__ == "__main__":

    for sector in sorted(
        latest["broad_sector"].dropna().unique()
    ):

        generate_sector_report(sector)