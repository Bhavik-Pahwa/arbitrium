from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Clause(Base):
    __tablename__ = "clauses"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    source_seat_allocation_result_id: Mapped[int | None] = mapped_column(
        ForeignKey("seat_allocation_results.id"), nullable=True
    )
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id"), nullable=False)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"), nullable=False)
    num_arbitrators: Mapped[str] = mapped_column(String(30), nullable=False)  # sole | three | emergency
    appointment_mechanism: Mapped[str] = mapped_column(String(50), nullable=False)
    language: Mapped[str] = mapped_column(String(60), nullable=False)
    governing_law_contract: Mapped[str] = mapped_column(String(255), nullable=False)
    governing_law_arbitration: Mapped[str] = mapped_column(String(255), nullable=False)
    party_details: Mapped[list | None] = mapped_column(JSON, nullable=True)
    generated_text: Mapped[str] = mapped_column(Text, nullable=False)
    pathology_check_notes: Mapped[list] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="clauses")
    seat = relationship("Seat")
    institution = relationship("Institution")
