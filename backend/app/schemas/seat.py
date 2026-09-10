from pydantic import BaseModel, ConfigDict


class SeatRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    country: str
    ny_convention_member: bool
    supervisory_court: str | None
    governing_statute: str | None
    notes: str | None
