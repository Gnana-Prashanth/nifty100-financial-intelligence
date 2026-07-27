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
    TableStyle,
    PageBreak
)

BASE_DIR = Path(__file__).resolve().parents[2]

ratios = pd.read_excel(
    BASE_DIR / "data/supporting/financial_ratios.xlsx"
)

sectors = pd.read_excel(
    BASE_DIR / "data/supporting/sectors.xlsx"
)

companies = pd.read_excel(
    BASE_DIR / "data/raw/companies.xlsx",
    header=1
)


def trend_arrow(current, previous):

    if pd.isna(current) or pd.isna(previous):
        return "-"

    if previous == 0:
        return "→"

    change = (current - previous) / abs(previous)

    if abs(change) <= 0.02:
        return "→"
    elif change > 0:
        return "↑"
    else:
        return "↓"

#Reverse Arrow for Debt/Equity
def debt_trend_arrow(current, previous):

    if pd.isna(current) or pd.isna(previous):
        return "-"

    if previous == 0:
        return "→"

    change = (current - previous) / abs(previous)

    if abs(change) <= 0.02:
        return "→"

    elif change < 0:
        return "↑"      # Lower debt = Better

    else:
        return "↓"      # Higher debt = Worse

    

portfolio_dir = BASE_DIR / "reports" / "portfolio"
portfolio_dir.mkdir(parents=True, exist_ok=True)

output = portfolio_dir / "portfolio_summary.pdf"

doc = SimpleDocTemplate(
    str(output),
    pagesize=A4
)

styles = getSampleStyleSheet()
story = []

company_ids = sorted(ratios["company_id"].unique())

for company in company_ids:

    history = ratios[
        (ratios["company_id"] == company) &
        (ratios["year"] != "TTM")
    ].sort_values("year")

    if len(history) < 2:
        continue

    latest = history.iloc[-1]
    previous = history.iloc[-2]

    sector = sectors.loc[
        sectors["company_id"] == company,
        "broad_sector"
    ].values

    sector = sector[0] if len(sector) else "Unknown"


    story.append(
        Paragraph(
            f"<b>{company}</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"Sector : {sector}",
            styles["Heading2"]
        )
    )

    story.append(Spacer(1, 15))

    #KPI Table    

    data = [

        ["KPI","Latest","Trend"],

        [
            "Revenue",
            f"{latest['sales']:,.0f}",
            trend_arrow(
                latest["sales"],
                previous["sales"]
            )
        ],

        [
            "Net Profit",
            f"{latest['net_profit']:,.0f}",
            trend_arrow(
                latest["net_profit"],
                previous["net_profit"]
            )
        ],

        [
            "ROE",
            f"{latest['return_on_equity_pct']:.2f}%",
            trend_arrow(
                latest["return_on_equity_pct"],
                previous["return_on_equity_pct"]
            )
        ],

        [
            "ROCE",
            f"{latest['return_on_capital_employed_pct']:.2f}%",
            trend_arrow(
                latest["return_on_capital_employed_pct"],
                previous["return_on_capital_employed_pct"]
            )
        ],

        [
            "Debt / Equity",
            f"{latest['debt_to_equity']:.2f}",
            debt_trend_arrow(
                latest["debt_to_equity"],
                previous["debt_to_equity"]
            )
        ],

        [
            "Composite Score",
            f"{latest['composite_quality_score']:.2f} / 5",
            trend_arrow(
                latest["composite_quality_score"],
                previous["composite_quality_score"]
            )
        ]

    ]
    

    table = Table(
        data,
        colWidths=[180,120,70]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),0.5,colors.black),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("BOTTOMPADDING",(0,0),(-1,-1),6),

            ("FONTSIZE",(0,0),(-1,-1),10)

        ])

    )

    story.append(table)

    story.append(PageBreak())

doc.build(story)

print("Portfolio Summary Generated")
