from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import Institution, Seat
from app.schemas.institution import InstitutionRead
from app.schemas.seat import SeatRead

router = APIRouter(tags=["seats"])


@router.get("/seats", response_model=list[SeatRead])
def list_seats(db: Session = Depends(get_db)):
    return db.query(Seat).order_by(Seat.name).all()


@router.get("/institutions", response_model=list[InstitutionRead])
def list_institutions(db: Session = Depends(get_db)):
    return db.query(Institution).order_by(Institution.name).all()
