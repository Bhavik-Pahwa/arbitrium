from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_optional, get_db
from app.models import Clause, SeatAllocationRequest, User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

GUEST_BANNER = {
    "headline": "Arbitrium — defensible arbitration seat intelligence",
    "capabilities": [
        "Recommend arbitration seats and institutions from sourced caseload, "
        "fee, and rules data.",
        "Generate pathology-checked arbitration clauses.",
        "Estimate administrative and tribunal costs and case duration.",
        "Track live institutional rule updates across major arbitral bodies.",
    ],
    "cta": {"label": "Generate a clause", "target": "clause_generation"},
}


@router.get("")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    if not current_user:
        return {"authenticated": False, **GUEST_BANNER}

    seat_allocations = (
        db.query(SeatAllocationRequest)
        .filter(SeatAllocationRequest.user_id == current_user.id)
        .order_by(SeatAllocationRequest.created_at.desc())
        .limit(20)
        .all()
    )
    clauses = (
        db.query(Clause)
        .filter(Clause.user_id == current_user.id)
        .order_by(Clause.created_at.desc())
        .limit(20)
        .all()
    )

    return {
        "authenticated": True,
        "welcome_message": f"Welcome back, {current_user.full_name or current_user.email}",
        "seat_allocations": [
            {
                "id": r.id,
                "arbitration_type": r.arbitration_type,
                "governing_law": r.governing_law,
                "created_at": r.created_at,
            }
            for r in seat_allocations
        ],
        "clauses_generated": [
            {
                "id": c.id,
                "seat_id": c.seat_id,
                "institution_id": c.institution_id,
                "num_arbitrators": c.num_arbitrators,
                "created_at": c.created_at,
            }
            for c in clauses
        ],
    }
