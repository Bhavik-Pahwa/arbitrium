from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.schemas.seat_allocation import PartyDetail


class ClauseGenerateRequest(BaseModel):
    source_seat_allocation_result_id: int | None = None
    seat_id: int
    institution_id: int
    num_arbitrators: Literal["sole", "three", "emergency"]
    appointment_mechanism: Literal["institutional_default", "co_arbitrator_nomination", "presiding_officer"]
    language: str = "English"
    governing_law_contract: str
    governing_law_arbitration: str
    party_details: list[PartyDetail] = []


class ClauseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    seat_id: int
    institution_id: int
    num_arbitrators: str
    appointment_mechanism: str
    language: str
    governing_law_contract: str
    governing_law_arbitration: str
    generated_text: str
    pathology_check_notes: list[str]
    created_at: datetime
