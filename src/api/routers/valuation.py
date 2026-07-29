from fastapi import APIRouter
from fastapi import Path
import pandas as pd
from fastapi import HTTPException, Query

from ..database import get_connection

router = APIRouter(
    prefix="/market-cap",
    tags=["Valuation"]
)

#==================================================
#        Endpoint 2 - /market-cap/{ticker}
#==================================================

@router.get("/{ticker}")
def market_cap_history(
        ticker: str = Path(
            ...,
            description="Company ticker symbol",
            example="TCS"
        )
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            year,
            market_cap_crore,
            pe_ratio,
            pb_ratio,
            ev_ebitda,
            dividend_yield_pct
        FROM market_cap
        WHERE company_id=?
        ORDER BY year
    """, (ticker,))

    rows = cur.fetchall()

    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Ticker not found"
        )

    return [dict(r) for r in rows]