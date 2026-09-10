from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CostEstimateRequest(BaseModel):
    institution_id: int
    claim_amount: float = Field(gt=0)
    currency: str = "USD"


class CostEstimateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution_id: int
    claim_amount: float
    currency: str
    estimated_admin_fee: float
    estimated_tribunal_fee_min: float
    estimated_tribunal_fee_max: float
    estimated_duration_months_min: int
    estimated_duration_months_max: int
    breakdown: dict
    created_at: datetime
