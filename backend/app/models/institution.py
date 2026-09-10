from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Institution(Base):
    __tablename__ = "institutions"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    website_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    home_seat_id: Mapped[int | None] = mapped_column(ForeignKey("seats.id"), nullable=True)

    home_seat = relationship("Seat", back_populates="institutions")
    rules = relationship("InstitutionRule", back_populates="institution")
    annual_report_stats = relationship("AnnualReportStat", back_populates="institution")
    fee_schedules = relationship("FeeSchedule", back_populates="institution")
    ratings = relationship("SeatInstitutionRating", back_populates="institution")
