from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class AnnualReportStat(Base):
    __tablename__ = "annual_report_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    institution_id: Mapped[int] = mapped_column(ForeignKey("institutions.id"), nullable=False)
    report_year: Mapped[int] = mapped_column(Integer, nullable=False)
    new_cases_filed: Mapped[int | None] = mapped_column(Integer, nullable=True)
    avg_claim_value_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    avg_duration_months: Mapped[float | None] = mapped_column(Float, nullable=True)
    source_url: Mapped[str] = mapped_column(String(500), nullable=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    institution = relationship("Institution", back_populates="annual_report_stats")
