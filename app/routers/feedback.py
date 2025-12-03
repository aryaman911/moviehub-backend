from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import ADPFeedback, ADPSeries
from app.schemas import FeedbackCreate, FeedbackOut
from app.deps import get_current_user

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/", response_model=FeedbackOut)
def create_feedback(
    payload: FeedbackCreate,
    db: Session = Depends(get_db),
    current = Depends(get_current_user),
):
    series = db.query(ADPSeries).filter(ADPSeries.series_id == payload.series_id).first()
    if not series:
        raise HTTPException(status_code=404, detail="Series not found")

    fb = ADPFeedback(
        adp_account_account_id=payload.account_id,
        adp_series_series_id=payload.series_id,
        rating=payload.rating,
        feedback_text=payload.feedback_text,
        feedback_date=date.today(),
    )
    db.merge(fb)  # upsert by PK
    db.commit()
    return FeedbackOut(
        account_id=fb.adp_account_account_id,
        rating=fb.rating,
        feedback_text=fb.feedback_text,
        feedback_date=fb.feedback_date,
    )


@router.get("/{series_id}", response_model=List[FeedbackOut])
def list_feedback(series_id: int, db: Session = Depends(get_db)):
    rows = (
        db.query(ADPFeedback)
        .filter(ADPFeedback.adp_series_series_id == series_id)
        .all()
    )
    return [
        FeedbackOut(
            account_id=r.adp_account_account_id,
            rating=r.rating,
            feedback_text=r.feedback_text,
            feedback_date=r.feedback_date,
        )
        for r in rows
    ]
