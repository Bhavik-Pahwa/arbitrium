from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user_optional, get_db
from app.models import Clause, Institution, Seat, User
from app.schemas.clause import ClauseGenerateRequest, ClauseRead
from app.services import clause_generator

router = APIRouter(prefix="/clauses", tags=["clauses"])


@router.post("/generate", response_model=ClauseRead)
def generate_clause(
    payload: ClauseGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    seat = db.get(Seat, payload.seat_id)
    institution = db.get(Institution, payload.institution_id)
    if not seat or not institution:
        raise HTTPException(status_code=404, detail="Seat or institution not found")

    result = clause_generator.generate(
        seat=seat,
        institution=institution,
        num_arbitrators=payload.num_arbitrators,
        appointment_mechanism=payload.appointment_mechanism,
        language=payload.language,
        governing_law_contract=payload.governing_law_contract,
        governing_law_arbitration=payload.governing_law_arbitration,
        party_details=payload.party_details,
    )

    clause = Clause(
        user_id=current_user.id if current_user else None,
        source_seat_allocation_result_id=payload.source_seat_allocation_result_id,
        seat_id=seat.id,
        institution_id=institution.id,
        num_arbitrators=payload.num_arbitrators,
        appointment_mechanism=payload.appointment_mechanism,
        language=payload.language,
        governing_law_contract=payload.governing_law_contract,
        governing_law_arbitration=payload.governing_law_arbitration,
        party_details=[p.model_dump() for p in payload.party_details],
        generated_text=result.text,
        pathology_check_notes=result.pathology_notes,
    )
    db.add(clause)
    db.commit()
    db.refresh(clause)
    return clause


@router.get("/{clause_id}", response_model=ClauseRead)
def get_clause(clause_id: int, db: Session = Depends(get_db)):
    clause = db.get(Clause, clause_id)
    if not clause:
        raise HTTPException(status_code=404, detail="Clause not found")
    return clause


@router.get("", response_model=list[ClauseRead])
def list_clauses(
    db: Session = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
):
    if not current_user:
        return []
    return (
        db.query(Clause)
        .filter(Clause.user_id == current_user.id)
        .order_by(Clause.created_at.desc())
        .all()
    )
