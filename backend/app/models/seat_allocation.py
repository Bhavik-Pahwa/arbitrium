from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class SeatAllocationRequest(Base):
    __tablename__ = "seat_allocation_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    contract_upload_id: Mapped[int | None] = mapped_column(ForeignKey("contract_uploads.id"), nullable=True)
    arbitration_type: Mapped[str] = mapped_column(String(20), nullable=False)  # domestic | cross_border
    parties: Mapped[list | None] = mapped_column(JSON, nullable=True)
    scope: Mapped[str | None] = mapped_column(Text, nullable=True)
    claim_quantum: Mapped[float | None] = mapped_column(Float, nullable=True)
    claim_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    governing_law: Mapped[str | None] = mapped_column(String(255), nullable=True)
    priority_speed: Mapped[float] = mapped_column(Float, default=0.25)
    priority_cost: Mapped[float] = mapped_column(Float, default=0.25)
    priority_neutrality: Mapped[float] = mapped_column(Float, default=0.25)
    priority_enforceability: Mapped[float] = mapped_column(Float, default=0.25)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="seat_allocation_requests")
    results = relationship("SeatAllocationResult", back_populates="request", order_by="SeatAllocationResult.rank")


class SeatAllocationResult(Base):
    __tablename__ = "seat_allocation_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("seat_allocation_requests.id"), nullable=False)
    rank: Mapped[int] = mapped_column(nullable=False)
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id"), nullable=False)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"), nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    pros: Mapped[list] = mapped_column(JSON, nullable=False)
    cons: Mapped[list] = mapped_column(JSON, nullable=False)
    citations: Mapped[list] = mapped_column(JSON, nullable=False)

    request = relationship("SeatAllocationRequest", back_populates="results")
    seat = relationship("Seat")
    institution = relationship("Institution")
