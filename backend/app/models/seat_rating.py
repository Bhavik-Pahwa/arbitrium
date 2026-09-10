from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class SeatInstitutionRating(Base):
    """Qualitative 1-5 ratings feeding the seat-allocation recommendation engine.

    Scores are curated judgments grounded in the cited sources (supervisory
    court reputation, New York Convention standing, institutional rules
    maturity, published fee/caseload data) rather than a single hard metric.
    """

    __tablename__ = "seat_institution_ratings"

    id: Mapped[int] = mapped_column(primary_key=True)
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id"), nullable=False)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"), nullable=False)
    speed_score: Mapped[int] = mapped_column(Integer, nullable=False)
    cost_score: Mapped[int] = mapped_column(Integer, nullable=False)
    neutrality_score: Mapped[int] = mapped_column(Integer, nullable=False)
    enforceability_score: Mapped[int] = mapped_column(Integer, nullable=False)
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)

    seat = relationship("Seat")
    institution = relationship("Institution", back_populates="ratings")
