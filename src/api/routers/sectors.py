from fastapi import APIRouter, HTTPException
from statistics import median
from src.api.database import get_connection
from fastapi import Path

router = APIRouter(
    prefix="/sectors",
    tags=["Sectors"]
)

@router.get("")
def get_sectors():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            s.company_id,
            s.broad_sector,
            fr.return_on_equity_pct,
            fr.debt_to_equity,
            mc.pe_ratio
        FROM sectors s
        JOIN financial_ratios fr
            ON s.company_id = fr.company_id
        LEFT JOIN market_cap mc
            ON s.company_id = mc.company_id

    """)

    rows = cur.fetchall()
    conn.close()

    sectors = {}

    for row in rows:
        sector = row["broad_sector"]

        if sector not in sectors:
            sectors[sector] = {
                "companies": set(),
                "roe": [],
                "pe": [],
                "de": []
            }

        sectors[sector]["companies"].add(row["company_id"] if "company_id" in row.keys() else None)

        if row["return_on_equity_pct"] is not None:
            sectors[sector]["roe"].append(row["return_on_equity_pct"])

        if row["pe_ratio"] is not None:
            sectors[sector]["pe"].append(row["pe_ratio"])

        if row["debt_to_equity"] is not None:
            sectors[sector]["de"].append(row["debt_to_equity"])

    result = []

    for sector, data in sectors.items():
        result.append({
            "sector": sector,
            "company_count": len(data["companies"]),
            "median_roe": round(median(data["roe"]), 2) if data["roe"] else None,
            "median_pe": round(median(data["pe"]), 2) if data["pe"] else None,
            "median_de": round(median(data["de"]), 2) if data["de"] else None
        })

    return sorted(result, key=lambda x: x["sector"])


#======================================================================================
#                     Endpoint 2 — /sectors/{sector}/companies
#======================================================================================

@router.get("/{sector}/companies")
def sector_companies(
    sector: str = Path(
        ...,
        description="Sector name. Examples: Financials, Energy, Healthcare, Industrials",
        example="Financials"
    )
):

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                c.id AS company_id,
                c.company_name,
                fr.year,
                fr.return_on_equity_pct,
                fr.return_on_capital_employed_pct,
                fr.debt_to_equity,
                fr.revenue_cagr_5yr,
                fr.pat_cagr_5yr,
                fr.operating_profit_margin_pct
            FROM companies c
            JOIN sectors s
                ON c.id = s.company_id
            JOIN financial_ratios fr
                ON c.id = fr.company_id
            WHERE s.broad_sector = ?
              AND fr.year != 'TTM'
            ORDER BY c.company_name, fr.year DESC
        """, (sector,))

        rows = cur.fetchall()

        print("Rows fetched:", len(rows))

        if rows:
            print("First row keys:", rows[0].keys())
            print(dict(rows[0]))

        conn.close()

        latest = {}

        for row in rows:
            if row["company_id"] not in latest:
                latest[row["company_id"]] = dict(row)

        return list(latest.values())

    except Exception as e:
        conn.close()
        return {"error": str(e), "type": type(e).__name__}