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
    sector: str | None = Query(default=None),
    market_cap_category: str | None = Query(default=None),
    search: str | None = Query(default=None)
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
    year: str | None = Query(None, example="MAR 2022")
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

#uvicorn src.api.main:app --reload --port 8000