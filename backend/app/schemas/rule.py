from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class InstitutionRuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    institution_id: int
    rules_name: str
    version_year: int | None
    effective_date: date | None
    summary: str | None
    source_url: str
    last_checked_at: datetime


class SourceIndexEntry(BaseModel):
    label: str
    source_url: str
    category: str
