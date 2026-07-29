from fastapi import APIRouter, HTTPException, Path
from src.api.database import get_connection

router = APIRouter(
    prefix="/peers",
    tags=["Peers"]
)

#==================================================
#        Endpoint - /peers/{group_name}
#==================================================


@router.get("/{group_name}")
def peer_group(
    group_name: str = Path(
    ...,
    description="Peer group name",
    example="Private Banks")
):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            company_id,
            year,
            metric,
            value,
            percentile_rank
        FROM peer_percentiles
        WHERE peer_group = ?
        ORDER BY company_id, metric
    """, (group_name,))

    rows = cur.fetchall()
    conn.close()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="Peer group not found"
        )

    return [dict(r) for r in rows]

