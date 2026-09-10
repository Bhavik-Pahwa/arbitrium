from pydantic import BaseModel, ConfigDict


class InstitutionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    short_code: str
    name: str
    website_url: str | None
    home_seat_id: int | None
