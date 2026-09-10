from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class Seat(Base):
    __tablename__ = "seats"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    country: Mapped[str] = mapped_column(String(120), nullable=False)
    ny_convention_member: Mapped[bool] = mapped_column(Boolean, default=True)
    supervisory_court: Mapped[str | None] = mapped_column(String(255), nullable=True)
    governing_statute: Mapped[str | None] = mapped_column(String(255), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    institutions = relationship("Institution", back_populates="home_seat")
