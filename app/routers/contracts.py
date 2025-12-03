from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import ADPContract
from app.schemas import ContractOut
from app.deps import require_role

router = APIRouter(prefix="/contracts", tags=["contracts"])


@router.get("/", response_model=List[ContractOut])
def list_contracts(
    db: Session = Depends(get_db),
    current = Depends(require_role("EMPLOYEE")),  # EMPLOYEE-only
):
    rows = db.query(ADPContract).all()
    return [
        ContractOut(
            contract_id=r.contract_id,
            series_id=r.adp_series_series_id,
            per_episode_charge=float(r.per_episode_charge),
            status=r.status,
            contract_start_date=r.contract_start_date,
            contract_end_date=r.contract_end_date,
        )
        for r in rows
    ]

