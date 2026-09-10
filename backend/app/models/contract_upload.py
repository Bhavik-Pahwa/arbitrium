from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base


class ContractUpload(Base):
    __tablename__ = "contract_uploads"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    filename: Mapped[str] = mapped_column(String(500), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(1000), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="processed")
    extracted_parties: Mapped[list | None] = mapped_column(JSON, nullable=True)
    extracted_scope: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    extracted_claim_quantum: Mapped[float | None] = mapped_column(nullable=True)
    extracted_claim_currency: Mapped[str | None] = mapped_column(String(10), nullable=True)
    extracted_governing_law: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
