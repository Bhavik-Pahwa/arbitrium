from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_optional, get_db
from app.models import CostEstimate, FeeSchedule, User
from app.schemas.cost_estimate import CostEstimateRead, CostEstimateRequest
from app.services import cost_estimator

router = APIRouter(prefix="/cost-estimate", tags=["cost-estimate"])


@router.post("/calculate", response_model=CostEstimateRead)
def calculate(
    payload: CostEstimateRequest,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    fee_schedule = (
        db.query(FeeSchedule)
        .filter(FeeSchedule.institution_id == payload.institution_id)
        .first()
    )
    if not fee_schedule:
        raise HTTPException(status_code=404, detail="No fee schedule found for this institution")

    result = cost_estimator.estimate(fee_schedule, payload.claim_amount)

    estimate = CostEstimate(
        user_id=current_user.id if current_user else None,
        institution_id=payload.institution_id,
        claim_amount=payload.claim_amount,
        currency=payload.currency,
        **result,
    )
    db.add(estimate)
    db.commit()
    db.refresh(estimate)
    return estimate
