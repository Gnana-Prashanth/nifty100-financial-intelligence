from fastapi import APIRouter
from pathlib import Path
from fastapi import Path as ApiPath
import pandas as pd
from fastapi import HTTPException, Query

from ..database import get_connection

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)

BASE_DIR = Path(__file__).resolve().parents[3]

#==================================================
#        Endpoint 1 - Portfolio Stats
#==================================================

@router.get("/stats")
def portfolio_stats():

    csv_path = BASE_DIR / "output" / "portfolio_stats.csv"

    df = pd.read_csv(csv_path)

    return df.to_dict(orient="records")
    

