from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import AnnualReportStat, InstitutionRule
from app.schemas.rule import InstitutionRuleRead, SourceIndexEntry

router = APIRouter(prefix="/rules", tags=["rules"])


@router.get("", response_model=list[InstitutionRuleRead])
def list_rules(institution_id: int | None = None, db: Session = Depends(get_db)):
    query = db.query(InstitutionRule)
    if institution_id is not None:
        query = query.filter(InstitutionRule.institution_id == institution_id)
    return query.order_by(InstitutionRule.rules_name).all()


@router.get("/sources", response_model=list[SourceIndexEntry])
def list_sources(db: Session = Depends(get_db)):
    entries: list[SourceIndexEntry] = []
    for rule in db.query(InstitutionRule).all():
        entries.append(
            SourceIndexEntry(label=rule.rules_name, source_url=rule.source_url, category="rules")
        )
    for stat in db.query(AnnualReportStat).all():
        entries.append(
            SourceIndexEntry(
                label=f"{stat.institution.short_code} Annual Report {stat.report_year}",
                source_url=stat.source_url,
                category="annual_report",
            )
        )
    return entries
