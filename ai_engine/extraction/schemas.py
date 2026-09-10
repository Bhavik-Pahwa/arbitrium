from typing import Literal

from pydantic import BaseModel, Field

Dimension = Literal["sector", "country", "seat", "tribunal_composition", None]
Status = Literal["disclosed", "not_disclosed"]


class ExtractedFact(BaseModel):
    institution: str
    report_year: int | None = None
    metric: str  # e.g. "new_cases_filed", "case_count_by_sector", "avg_duration_months"
    dimension: Dimension = None  # what the metric is broken down by, if anything
    dimension_value: str | None = None  # e.g. "construction", "Singapore"
    numeric_value: float | None = None
    unit: str | None = None  # e.g. "cases", "percent", "months", "USD"
    status: Status
    source_url: str
    source_excerpt: str | None = None
    hallucination_check_passed: bool | None = None

    def requires_excerpt(self) -> bool:
        return self.status == "disclosed" and self.numeric_value is not None


class ExtractionResult(BaseModel):
    institution: str
    facts: list[ExtractedFact] = Field(default_factory=list)
    raw_model_output: str
