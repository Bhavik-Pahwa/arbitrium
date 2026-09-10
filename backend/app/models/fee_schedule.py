from sqlalchemy import Boolean, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class FeeSchedule(Base):
    """Tiered ad-valorem fee schedule.

    `admin_fee_tiers` / `tribunal_fee_tiers` are lists of
    {"claim_min": float, "claim_max": float|None, "base": float, "rate_pct": float}
    evaluated by app.services.cost_estimator against the claim amount.
    """

    __tablename__ = "fee_schedules"

    id: Mapped[int] = mapped_column(primary_key=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"), nullable=False)
    schedule_name: Mapped[str] = mapped_column(String(255), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    admin_fee_tiers: Mapped[list] = mapped_column(JSON, nullable=False)
    tribunal_fee_tiers: Mapped[list] = mapped_column(JSON, nullable=False)
    typical_duration_months_min: Mapped[int | None] = mapped_column(nullable=True)
    typical_duration_months_max: Mapped[int | None] = mapped_column(nullable=True)
    source_url: Mapped[str] = mapped_column(String(500), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)

    institution = relationship("Institution", back_populates="fee_schedules")
