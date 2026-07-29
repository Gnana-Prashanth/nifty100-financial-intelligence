from fastapi import APIRouter, Query, HTTPException
from src.api.database import get_connection

router = APIRouter(
    prefix="/screener",
    tags=["Screener"]
)

@router.get("")
def screener(

    min_roe: float | None = Query(None, ge=0),
    max_de: float | None = Query(None, ge=0),
    min_fcf: float | None = Query(None),
    sector: str | None = Query(None),
    min_rev_cagr_5yr: float | None = Query(None),
    min_pat_cagr_5yr: float | None = Query(None),
    max_pe: float | None = Query(None, ge=0)

):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    SELECT
        c.id,
        c.company_name,
        s.broad_sector,

        fr.return_on_equity_pct,
        fr.debt_to_equity,
        fr.free_cash_flow_cr,
        fr.revenue_cagr_5yr,
        fr.pat_cagr_5yr,

        mc.pe_ratio

    FROM financial_ratios fr

    JOIN companies c
    ON fr.company_id = c.id

    JOIN sectors s
    ON fr.company_id = s.company_id

    JOIN market_cap mc
    ON fr.company_id = mc.company_id
    AND CAST(substr(fr.year, -4) AS INTEGER) = mc.year

    WHERE fr.year != 'TTM'
    """

    params = []

    if min_roe is not None:
        query += " AND fr.return_on_equity_pct >= ?"
        params.append(min_roe)

    if max_de is not None:
        query += " AND fr.debt_to_equity <= ?"
        params.append(max_de)

    if min_fcf is not None:
        query += " AND fr.free_cash_flow_cr >= ?"
        params.append(min_fcf)

    if sector:
        query += " AND s.broad_sector = ?"
        params.append(sector)

    if min_rev_cagr_5yr is not None:
        query += " AND fr.revenue_cagr_5yr >= ?"
        params.append(min_rev_cagr_5yr)

    if min_pat_cagr_5yr is not None:
        query += " AND fr.pat_cagr_5yr >= ?"
        params.append(min_pat_cagr_5yr)

    if max_pe is not None:
        query += " AND mc.pe_ratio <= ?"
        params.append(max_pe)

    query += """
    ORDER BY
        fr.return_on_equity_pct DESC
    """

    cur.execute(query, params)

    rows = cur.fetchall()

    conn.close()

    return [dict(r) for r in rows]

