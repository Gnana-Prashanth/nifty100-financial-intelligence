from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi import Path
from ..database import get_connection

router = APIRouter(
    prefix="/companies",
    tags=["Companies"]
)

#==================================================
#                Endpoint 1
#==================================================

@router.get("")
def list_companies(

    sector: str | None = Query(
        None,
        description="Filter by broad sector",
        example="Financials"
    ),

    market_cap_category: str | None = Query(
        None,
        description="Filter by market cap category",
        example="Large Cap"
    ),

    search: str | None = Query(
        None,
        description="Search by company name or ticker",
        example="TCS"
    )
    
):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT
        c.id AS company_id,
        c.company_name,
        s.broad_sector,
        s.sub_sector,
        s.market_cap_category,
        fr.return_on_equity_pct AS roe_pct,
        fr.return_on_capital_employed_pct AS roce_pct

    FROM companies c

    LEFT JOIN sectors s
        ON c.id = s.company_id

    LEFT JOIN financial_ratios fr
        ON c.id = fr.company_id

    WHERE fr.year = (
        SELECT MAX(f2.year)
        FROM financial_ratios f2
        WHERE
            f2.company_id = c.id
            AND f2.year != 'TTM'
    )
    """

    params = []

    if sector:

        query += """
        AND s.broad_sector = ?
        """

        params.append(sector)

    if market_cap_category:

        query += """
        AND s.market_cap_category = ?
        """

        params.append(market_cap_category) 

    if search:

        query += """
        AND (
            c.id LIKE ?
            OR c.company_name LIKE ?
        )
        """

        params.extend([
            f"%{search}%",
            f"%{search}%"
        ])

    query += """
    ORDER BY c.company_name
    """

    cur.execute(query, params)

    rows = cur.fetchall()

    conn.close()

    return [dict(row) for row in rows]


#==================================================
#                Endpoint 2
#==================================================

@router.get("/{ticker}")
def company_profile(ticker: str):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT

        c.*,

        s.broad_sector,
        s.sub_sector,
        s.market_cap_category,

        fr.*

    FROM companies c

    LEFT JOIN sectors s
    ON c.id = s.company_id

    LEFT JOIN financial_ratios fr
    ON c.id = fr.company_id

    WHERE

        c.id = ?

        AND fr.year = (

    SELECT MAX(year)

    FROM financial_ratios f2

    WHERE

        f2.company_id = c.id

        AND f2.year != 'TTM'

    )"""

    cur.execute(query, (ticker,))

    row = cur.fetchone()

    conn.close()

    if row is None:

        raise HTTPException(

            status_code=404,

            detail="Ticker not found"

        )

    return dict(row)


#==================================================
#                Endpoint 3
#==================================================

@router.get("/{ticker}/pl")
def company_pl(

    ticker: str = Path(
            ...,
            description="Company ticker symbol",
            example="TCS"
        ),

    from_year: str | None = Query(None,
                                  description="Financial year in format: MAR YYYY",
                                  example="MAR 2022"
                                ),
    to_year: str | None = Query(None,
                                description="Financial year in format: MAR YYYY",
                                example="MAR 2024")
):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT *

    FROM profitandloss

    WHERE company_id = ?
    """

    params = [ticker]

    if from_year:

        query += " AND year >= ?"

        params.append(from_year)

    if to_year:

        query += " AND year <= ?"

        params.append(to_year)

    query += " ORDER BY year"

    cur.execute(query, params)

    rows = cur.fetchall()

    conn.close()

    if not rows:

        raise HTTPException(
            status_code=404,
            detail="Company or data not found"
        )

    return [dict(r) for r in rows]


#==================================================
#                Endpoint 4
#==================================================

@router.get("/{ticker}/bs")
def company_bs(

    ticker: str = Path(
            ...,
            description="Company ticker symbol",
            example="TCS"
        ),

    from_year: str | None = Query(None,
                                  description="Financial year in format: MAR YYYY",
                                  example="MAR 2022"
                                ),
    to_year: str | None = Query(None,
                                description="Financial year in format: MAR YYYY",
                                example="MAR 2024")
):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT *

    FROM balancesheet

    WHERE company_id = ?
    """

    params = [ticker]

    if from_year:

        query += " AND year >= ?"

        params.append(from_year)

    if to_year:

        query += " AND year <= ?"

        params.append(to_year)

    query += " ORDER BY year"

    cur.execute(query, params)

    rows = cur.fetchall()

    conn.close()

    if not rows:

        raise HTTPException(
            status_code=404,
            detail="Company or data not found"
        )

    return [dict(r) for r in rows]


#==================================================
#                Endpoint 5
#==================================================

@router.get("/{ticker}/cashflow")
def company_cashflow(

    ticker: str = Path(
            ...,
            description="Company ticker symbol",
            example="TCS"
        ),

    from_year: str | None = Query(None,
                                  description="Financial year in format: MAR YYYY",
                                  example="MAR 2022"
                                ),
    to_year: str | None = Query(None,
                                description="Financial year in format: MAR YYYY",
                                example="MAR 2024")
):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT *

    FROM cashflow

    WHERE company_id = ?
    """

    params = [ticker]

    if from_year:

        query += " AND year >= ?"

        params.append(from_year)

    if to_year:

        query += " AND year <= ?"

        params.append(to_year)

    query += " ORDER BY year"

    cur.execute(query, params)

    rows = cur.fetchall()

    conn.close()

    if not rows:

        raise HTTPException(
            status_code=404,
            detail="Company or data not found"
        )

    return [dict(r) for r in rows]


#==================================================
#                Endpoint 6
#==================================================

@router.get("/{ticker}/ratios")
def company_ratios(
    ticker: str = Path(
            ...,
            description="Company ticker symbol",
            example="TCS"
        ),
    year: str | None = Query(None, examplees="MAR 2022")
):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT *

    FROM financial_ratios

    WHERE company_id = ?
    """

    params = [ticker]

    if year:

        query += " AND year = ?"

        params.append(year)

    query += " ORDER BY year"

    cur.execute(query, params)

    rows = cur.fetchall()

    conn.close()

    if not rows:

        raise HTTPException(
            status_code=404,
            detail="Company or KPI data not found"
        )

    return [dict(r) for r in rows]


#==================================================
#                Endpoint 7
#==================================================

@router.get("/{ticker}/tearsheet")
def company_tearsheet(ticker: str):

    BASE_DIR = Path(__file__).resolve().parents[3]

    pdf = (
        BASE_DIR /
        "reports" /
        "tearsheets" /
        f"{ticker}_tearsheet.pdf"
    )

    if not pdf.exists():

        raise HTTPException(
            status_code=404,
            detail="Tearsheet not found"
        )

    return FileResponse(
        path=str(pdf),
        media_type="application/pdf",
        filename=f"{ticker}_tearsheet.pdf"
    )


#==================================================
#          Endpoint 8 - /documents
#==================================================

@router.get("/{ticker}/documents")
def company_documents(ticker: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            Year,
            Annual_Report
        FROM documents
        WHERE company_id=?
        ORDER BY year
    """, (ticker,))

    rows = cur.fetchall()

    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Documents not found"
        )

    result = []

    for row in rows:

        result.append({

            "Year": row["Year"],

            "annual_report": row["Annual_Report"],

            "is_url_valid": bool(row["Annual_Report"])

        })

    return result


#==================================================
#          Endpoint 9 - / Peer Comparison
#==================================================

@router.get("/{ticker}/peers/compare")
def compare_with_peers(ticker: str):

    conn = get_connection()
    cur = conn.cursor()

    # Find peer group
    cur.execute("""
        SELECT peer_group_name
        FROM peer_groups
        WHERE company_id = ?
    """, (ticker,))

    group = cur.fetchone()

    if not group:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Peer group not found"
        )

    peer_group = group["peer_group_name"]


    cur.execute("""
        SELECT company_id
        FROM peer_groups
        WHERE peer_group_name = ?
        AND is_benchmark = 1
    """, (peer_group,))

    benchmark = cur.fetchone()["company_id"]


    cur.execute("""
        SELECT
            metric,
            value
        FROM peer_percentiles
        WHERE company_id = ?
    """, (ticker,))

    company = {
        r["metric"]: r["value"]
        for r in cur.fetchall()
    }


    cur.execute("""
        SELECT
            metric,
            value
        FROM peer_percentiles
        WHERE company_id = ?
    """, (benchmark,))

    benchmark_values = {
        r["metric"]: r["value"]
        for r in cur.fetchall()
    }


    cur.execute("""
        SELECT
            metric,
            ROUND(AVG(value),2) AS avg_value
        FROM peer_percentiles
        WHERE peer_group = ?
        GROUP BY metric
    """, (peer_group,))

    peer_average = {
        r["metric"]: r["avg_value"]
        for r in cur.fetchall()
    }

    conn.close()


    return {

        "peer_group": peer_group,

        "benchmark_company": benchmark,

        "company": company,

        "peer_average": peer_average,

        "benchmark": benchmark_values

    }

#uvicorn src.api.main:app --reload --port 8000
#http://127.0.0.1:8000/docs