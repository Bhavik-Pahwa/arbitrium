from app.db.base_class import Base
from app.models import (  # noqa: F401 — imported for metadata registration
    User,
    Seat,
    Institution,
    InstitutionRule,
    AnnualReportStat,
    FeeSchedule,
    SeatInstitutionRating,
    ContractUpload,
    SeatAllocationRequest,
    SeatAllocationResult,
    Clause,
    CostEstimate,
)

__all__ = ["Base"]
