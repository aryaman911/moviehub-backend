from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import ADPSeries
from app.schemas import SeriesOut

router = APIRouter(prefix="/series", tags=["series"])


@router.get("/", response_model=List[SeriesOut])
def list_series(db: Session = Depends(get_db)):
    rows = db.query(ADPSeries).all()
    return [
        SeriesOut(
            series_id=r.series_id,
            name=r.name,
            num_episodes=r.num_episodes,
            release_date=r.release_date,
            language_code=r.adp_language_language_code,
            origin_country=r.origin_country,
        )
        for r in rows
    ]


@router.get("/{series_id}", response_model=SeriesOut)
def get_series(series_id: int, db: Session = Depends(get_db)):
    r = db.query(ADPSeries).filter(ADPSeries.series_id == series_id).first()
    if not r:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Series not found")
    return SeriesOut(
        series_id=r.series_id,
        name=r.name,
        num_episodes=r.num_episodes,
        release_date=r.release_date,
        language_code=r.adp_language_language_code,
        origin_country=r.origin_country,
    )
