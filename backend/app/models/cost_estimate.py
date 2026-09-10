from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class CostEstimate(Base):
    __tablename__ = "cost_estimates"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"), nullable=False)
    claim_amount: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    estimated_admin_fee: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_tribunal_fee_min: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_tribunal_fee_max: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_duration_months_min: Mapped[int] = mapped_column(nullable=False)
    estimated_duration_months_max: Mapped[int] = mapped_column(nullable=False)
    breakdown: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="cost_estimates")
    institution = relationship("Institution")
