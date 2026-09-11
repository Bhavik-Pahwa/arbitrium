from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PartyDetail(BaseModel):
    name: str
    role: str | None = None
    jurisdiction: str | None = None


class SeatAllocationAnalyzeRequest(BaseModel):
    arbitration_type: Literal["domestic", "cross_border"]
    contract_upload_id: int | None = None
    parties: list[PartyDetail] = Field(default_factory=list)
    scope: str | None = None
    claim_quantum: float | None = Field(default=None, ge=0)
    claim_currency: str | None = "USD"
    governing_law: str | None = None

    # Manual preference sliders — required even when other fields are auto-filled.
    priority_speed: float = Field(ge=0, le=1)
    priority_cost: float = Field(ge=0, le=1)
    priority_neutrality: float = Field(ge=0, le=1)
    priority_enforceability: float = Field(ge=0, le=1)

    @field_validator("priority_enforceability")
    @classmethod
    def weights_must_sum_to_one(cls, v, info):
        values = info.data
        total = v + sum(
            values.get(k, 0)
            for k in ("priority_speed", "priority_cost", "priority_neutrality")
        )
        if abs(total - 1.0) > 0.01:
            raise ValueError(
                f"priority_speed + priority_cost + priority_neutrality + priority_enforceability "
                f"must sum to 1.0 (got {total:.3f})"
            )
        return v


class SeatAllocationResultRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    rank: int
    seat_id: int
    institution_id: int
    seat_name: str | None = None
    seat_country: str | None = None
    institution_short_code: str | None = None
    institution_name: str | None = None
    score: float
    rationale: str
    pros: list[str]
    cons: list[str]
    citations: list[dict]
    factor_scores: list[dict] = []
    priority_factors: list[str] = []
    seat_reasons: list[str] = []
    better_if: str | None = None


class SeatAllocationResponse(BaseModel):
    request_id: int
    arbitration_type: str
    created_at: datetime
    results: list[SeatAllocationResultRead]
