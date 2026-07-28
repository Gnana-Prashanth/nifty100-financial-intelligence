from fastapi import APIRouter
from ..database import get_connection
import time

router = APIRouter()

START_TIME = time.time()

VERSION = "1.0.0"


@router.get("/health")
def health():

    conn = get_connection()

    cur = conn.cursor()

    tables = [

        "companies",

        "profitandloss",

        "balancesheet",

        "cashflow",

        "analysis",

        "documents",

        "prosandcons",

        "sectors",

        "market_cap",

        "financial_ratios"

    ]

    counts = {}

    for table in tables:

        cur.execute(f"SELECT COUNT(*) FROM {table}")

        counts[table] = cur.fetchone()[0]

    conn.close()

    return {

        "status": "ok",

        "db_row_counts": counts,

        "uptime_seconds": round(
            time.time() - START_TIME,
            2
        ),

        "version": VERSION

    }