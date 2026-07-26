import pandas as pd
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor

from reportlab.graphics.shapes import Drawing, PolyLine
from reportlab.graphics.shapes import Line, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from reportlab.graphics.charts.axes import XCategoryAxis, YValueAxis
from reportlab.lib.colors import HexColor

from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
    KeepTogether
)

BASE_DIR = Path(__file__).resolve().parents[2]

companies = pd.read_excel(
    BASE_DIR / "data/raw/companies.xlsx",
    header=1
)

ratios = pd.read_excel(
    BASE_DIR / "data/supporting/financial_ratios.xlsx"
)

balancesheet = pd.read_excel(
    BASE_DIR / "data/raw/balancesheet.xlsx",header=1
)

cashflow = pd.read_excel(
    BASE_DIR / "data/raw/cashflow.xlsx",header=1
)

pros_cons = pd.read_csv(
    BASE_DIR / "output/pros_cons_generated.csv"
)

capital = pd.read_csv(
    BASE_DIR / "output/capital_allocation.csv"
)


styles = getSampleStyleSheet()

title_style = styles["Heading1"]

title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

normal_style = styles["BodyText"]


def company_history(company_id):

    ratio_hist = (
        ratios[
            ratios["company_id"] == company_id
        ]
        .sort_values("year")
        .reset_index(drop=True)
    )

    bs_hist = (
        balancesheet[
            balancesheet["company_id"] == company_id
        ]
        .sort_values("year")
        .reset_index(drop=True)
    )

    cf_hist = (
        cashflow[
            cashflow["company_id"] == company_id
        ]
        .sort_values("year")
        .reset_index(drop=True)
    )

    return ratio_hist, bs_hist, cf_hist


def company_info(company_id):

    row = companies[
        companies["id"] == company_id
    ]

    if row.empty:
        raise ValueError(
            f"{company_id} not found in companies.xlsx"
        )

    return row.iloc[0]


#------------------------------------
#   ----Revenue Bar Chart----
#------------------------------------

def revenue_chart(ratio_hist):

    drawing = Drawing(250, 180)

    chart = VerticalBarChart()

    chart.x = 35
    chart.y = 25
    chart.width = 200
    chart.height = 130

    chart.barWidth = 16
    chart.groupSpacing = 8
    chart.barSpacing = 2

    chart.categoryAxis.labels.angle = 24
    chart.categoryAxis.labels.fontSize = 7

    chart.data = [
        ratio_hist["sales"].tolist()
    ]

    years = (
        ratio_hist["year"]
        .astype(str)
        .str.replace("Mar ", "", regex=False)
        .str.replace("TTM", "TTM", regex=False)
        .tolist()
    )

    chart.categoryAxis.categoryNames = years

    chart.valueAxis.valueMin = 0

    chart.bars[0].fillColor = HexColor("#2E86DE")

    drawing.add(chart)

    return drawing


#------------------------------------
#        Net Profit Chart
#------------------------------------

def profit_chart(ratio_hist):

    drawing = Drawing(250,180)

    chart = VerticalBarChart()

    chart.x = 35
    chart.y = 25
    chart.width = 200
    chart.height = 130

    chart.barWidth = 16
    chart.groupSpacing = 8
    chart.barSpacing = 2

    chart.categoryAxis.labels.angle = 24
    chart.categoryAxis.labels.fontSize = 7

    chart.data = [
        ratio_hist["net_profit"].tolist()
    ]

    years = (
        ratio_hist["year"]
        .astype(str)
        .str.replace("Mar ", "", regex=False)
        .str.replace("TTM", "TTM", regex=False)
        .tolist()
    )

    chart.categoryAxis.categoryNames = years

    chart.valueAxis.valueMin = 0

    chart.bars[0].fillColor = HexColor("#27AE60")

    drawing.add(chart)

    return drawing


#------------------------------------
#       ROE-ROCE Line Chart
#------------------------------------

def roe_roce_chart(ratio_hist):

    drawing = Drawing(560, 180)

    years = list(range(len(ratio_hist)))

    roe = ratio_hist["return_on_equity_pct"].fillna(0).tolist()
    roce = ratio_hist["return_on_capital_employed_pct"].fillna(0).tolist()

    roe_points = []
    roce_points = []

    for i in range(len(years)):
        x = 40 + i * 60
        roe_y = 30 + roe[i] * 2
        roce_y = 30 + roce[i] * 2

        roe_points.extend([x, roe_y])
        roce_points.extend([x, roce_y])

    drawing.add(

        Line(
            40,
            30,
            520,
            30,
            strokeColor=colors.black
        )

    )

    drawing.add(

        Line(
            40,
            30,
            40,
            150,
            strokeColor=colors.black
        )

    )

    drawing.add(
        PolyLine(
            roe_points,
            strokeColor=colors.red,
            strokeWidth=2
        )
    )

    drawing.add(
        PolyLine(
            roce_points,
            strokeColor=colors.blue,
            strokeWidth=2
        )
    )

    drawing.add(

        String(

            430,

            170,

            "Blue : ROCE",

            fillColor=colors.blue,

            fontSize=9

        )

    )

    drawing.add(

        String(

            430,

            158,

            "Red : ROE",

            fillColor=colors.red,

            fontSize=9

        )

    )

    years = [
        str(y)[-2:] if str(y) != "TTM" else "TTM"
        for y in ratio_hist["year"]
    ]

    for i, yr in enumerate(years):

        drawing.add(
            String(
                35 + i * 60,
                12,
                yr,
                fontSize=7
            )
        )

    return drawing


#Balance sheet chart
def balance_sheet_chart(bs_hist):

    drawing = Drawing(520, 220)

    chart = VerticalBarChart()

    chart.x = 45
    chart.y = 35
    chart.width = 420
    chart.height = 140

    chart.data = [

        bs_hist["equity_capital"].tolist(),

        bs_hist["borrowings"].tolist(),

        bs_hist["other_liabilities"].tolist()

    ]

    chart.categoryAxis.categoryNames = (
        bs_hist["year"].astype(str).tolist()
    )

    chart.categoryAxis.labels.angle = 45
    chart.categoryAxis.labels.dy = -12

    chart.valueAxis.valueMin = 0

    chart.bars[0].fillColor = HexColor("#3498DB")   # Equity
    chart.bars[1].fillColor = HexColor("#E67E22")   # Borrowings
    chart.bars[2].fillColor = HexColor("#2ECC71")   # Other Liabilities

    chart.categoryAxis.style = "stacked"

    drawing.add(chart)

    return drawing


def generate_tearsheet(company_id):

    output = (
        BASE_DIR /
        "output" /
        f"{company_id}_tearsheet.pdf"
    )

    output.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(

        str(output),

        pagesize=A4,

        rightMargin=25,
        leftMargin=25,
        topMargin=25,
        bottomMargin=25

    )

    story = []

    company = company_info(company_id)

    company_name = company["company_name"]
    ticker = company["id"]

    ratio_hist, bs_hist, cf_hist = company_history(company_id)


    header = Table(

        [[
            Paragraph(

                f"""
                <font color='white'>
                <b>{company['company_name']}</b><br/>
                <font size='18'>({company_id})</font>
                </font>
                """,

                title_style,

            )
        ]],

        colWidths=[7.2 * inch]

    )

    header.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#0B3D91")),

            ("TEXTCOLOR", (0,0), (-1,-1), colors.white),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

            ("TOPPADDING", (0,0), (-1,-1), 12),

            ("BOTTOMPADDING", (0,0), (-1,-1), 12)

        ])

    )

    story.append(header)

    story.append(Spacer(1, 20))

    latest = (
        ratio_hist.dropna(
            subset=[
                "return_on_equity_pct",
                "return_on_capital_employed_pct",
                "debt_to_equity"
            ],
            how="all"
        )
        .iloc[-1]
    )

    kpis = [

        ["Revenue", f"{latest['sales']:,.0f} Cr"],

        ["Net Profit", f"{latest['net_profit']:,.0f} Cr"],

        ["ROE", f"{latest['return_on_equity_pct']:.2f}%"],

        ["ROCE", f"{latest['return_on_capital_employed_pct']:.2f}%"],

        ["Debt/Equity", f"{latest['debt_to_equity']:.2f}"],

        ["Composite Score", f"{latest['composite_quality_score']:.2f}"]

    ]


    tiles = []

    value_style = styles["BodyText"]
    value_style.alignment = TA_CENTER
    value_style.fontSize = 18
    value_style.leading = 20
    value_style.spaceBefore = 0
    value_style.spaceAfter = 0

    for title, value in kpis:

        tile = Table(

            [
                [Paragraph(

                    f"""
                    <para align='center'>
                    <b>{title}</b>
                    </para>
                    """,

                    heading_style

                )],

                [Paragraph(
                    f"<b>{value}</b>", value_style
                )]
            ],

            colWidths=[2.2 * inch]

        )

        tile.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#E8E8E8")),

                ("BACKGROUND",(0,1),(-1,-1),colors.white),

                ("GRID",(0,0),(-1,-1),0.8,colors.grey),

                ("BOX",(0,0),(-1,-1),1.2,colors.grey),

                ("ALIGN",(0,0),(-1,-1),"CENTER"),

                ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

                ("TOPPADDING",(0,0),(-1,-1),5),

                ("BOTTOMPADDING",(0,0),(-1,-1),5)

            ])

        )

        tiles.append(tile)

    kpi_table = Table(

    [

        tiles[:3],

        tiles[3:]

    ],

    colWidths=[2.3 * inch] * 3

)

    story.append(Spacer(1,20))

    story.append(kpi_table)

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<b>10-Year Revenue & Net Profit</b>",
            heading_style
        )
    )

    story.append(Spacer(1,8))

    rev = revenue_chart(ratio_hist)
    profit = profit_chart(ratio_hist)


    chart_table = Table(

        [

            [rev, profit]

        ],

        colWidths=[3.4*inch,3.4*inch]

    )

    story.append(chart_table)

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<b>ROE vs ROCE Trend</b>",
            heading_style
        )
    )

    story.append(Spacer(1,8))

    story.append(
        roe_roce_chart(ratio_hist)
    )


#-----------------------------------------------------------------------------------------------

#                                   PAGE-BREAK

#-----------------------------------------------------------------------------------------------

    story.append(PageBreak())

    page2 = Paragraph(
        "<b>Financial Analysis</b>",
        title_style
    )

    story.append(page2)
    story.append(Spacer(1,20))

    latest_bs = bs_hist[
        [
            "year",
            "equity_capital",
            "borrowings",
            "other_liabilities"
        ]
    ]

    bs_data = [
        [
            "Year",
            "Equity",
            "Borrowings",
            "Other Liabilities"
        ]
    ]

    for _, row in latest_bs.iterrows():

        bs_data.append([

            str(row["year"]),

            f"{row['equity_capital']:,.0f}",

            f"{row['borrowings']:,.0f}",

            f"{row['other_liabilities']:,.0f}"

        ])

    bs_table = Table(bs_data)

    bs_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),0.5,colors.black),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ])

    )

    story.append(
        Paragraph(
            "<b>Balance Sheet Composition</b>",
            heading_style
        )
    )

    story.append(Spacer(1,10))

    story.append(
        balance_sheet_chart(bs_hist)
    )

    story.append(Spacer(1,20))

    legend_data = [
        [
            Paragraph("<font color='#3498DB'>■</font> Equity", normal_style),
            Paragraph("<font color='#E67E22'>■</font> Borrowings", normal_style),
            Paragraph("<font color='#2ECC71'>■</font> Other Liabilities", normal_style)
        ]
    ]

    legend = Table(
        legend_data,
        colWidths=[2.2*inch, 2.2*inch, 2.2*inch]
    )

    legend.setStyle(
        TableStyle([
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("BOTTOMPADDING",(0,0),(-1,-1),5)
        ])
    )

    story.append(legend)

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<b>Latest Cash Flow Summary</b>",
            heading_style
        )
    )

    story.append(Spacer(1,10))

    latest_cf = cf_hist.iloc[-1]

    cf_data = [

        ["Operating Cash Flow",
        f"{latest_cf['operating_activity']:,.0f}"],

        ["Investing Cash Flow",
        f"{latest_cf['investing_activity']:,.0f}"],

        ["Financing Cash Flow",
        f"{latest_cf['financing_activity']:,.0f}"],

        ["Net Cash Flow",
        f"{latest_cf['net_cash_flow']:,.0f}"]

    ]

    cf_table = Table(
        cf_data,
        colWidths=[3.5*inch,2.2*inch]
    )

    cf_table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,0),(-1,-1),colors.whitesmoke),

            ("ALIGN",(1,0),(1,-1),"RIGHT"),

            ("BOTTOMPADDING",(0,0),(-1,-1),8)

        ])

    )

    story.append(cf_table)

    story.append(Spacer(1,8))

    company_pc = pros_cons[pros_cons["company_id"] == company_id]
    pros = company_pc[company_pc["type"].str.lower() == "pro"]["text"].tolist()
    cons = company_pc[company_pc["type"].str.lower() == "con"]["text"].tolist()

    story.append(
        Paragraph("<b>Pros</b>", heading_style)
    )

    pros_rows = []

    for p in pros:

        pros_rows.append([

            Paragraph(

                f"""
                <font color='green' size='10'>●</font>
                <font size='12'>{p}</font>
                """,

                normal_style

            )

        ])

    pros_table = Table(
        pros_rows,
        colWidths=[6.6*inch]
    )

    pros_table.setStyle(

        TableStyle([

            ("VALIGN",(0,0),(-1,-1),"TOP"),

            ("BOTTOMPADDING",(0,0),(-1,-1),4)

        ])

    )

    story.append(Spacer(1,8))
    story.append(pros_table)


    story.append(
        Paragraph("<b>Cons</b>", heading_style)
    )

    if len(cons) == 0:

        story.append(
            Paragraph(
                "<font color='red'>No major negative signals.</font>",
                normal_style
            )
        )

    else:

        cons_rows = []

        for p in cons:

            cons_rows.append([

                Paragraph(

                    f"""
                    <font color='red' size='10'>●</font>
                    <font size='9'>{p}</font>
                    """,

                    normal_style

                )

            ])

        cons_table = Table(
            cons_rows,
            colWidths=[6.6*inch]
        )

        cons_table.setStyle(

            TableStyle([

                ("VALIGN",(0,0),(-1,-1),"TOP"),

                ("BOTTOMPADDING",(0,0),(-1,-1),3)

            ])

        )

        story.append(cons_table)

    story.append(Spacer(1,8))


    latest_pattern = (

        capital[
            capital["company_id"]==company_id
        ]

        .sort_values("year")

        .iloc[-1]["pattern_label"]

    )


    badge = Table(

        [

            ["Capital Allocation"],

            [latest_pattern]

        ],

        colWidths=[3*inch]

    )

    badge.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("BACKGROUND",(0,1),(-1,-1),colors.lightgreen),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BOTTOMPADDING",(0,0),(-1,-1),10)

        ])

    )

    story.append(KeepTogether([badge]))

    
    doc.build(story)
    print(f"Generated: {output}")

if __name__ == "__main__":  #This prevents the PDF from being generated automatically whenever the module is imported
    generate_tearsheet("TCS")