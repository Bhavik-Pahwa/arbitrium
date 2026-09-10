"""Creates tables (dev convenience — use Alembic in real deployments) and
loads app.seed.reference_data. Idempotent: re-running upserts by natural key
instead of duplicating rows.

Usage:
    python -m app.seed.seed_db
"""

from sqlalchemy.orm import Session

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models import (
    AnnualReportStat,
    FeeSchedule,
    Institution,
    InstitutionRule,
    Seat,
    SeatInstitutionRating,
)
from app.seed.reference_data import (
    ANNUAL_REPORT_STATS,
    FEE_SCHEDULES,
    INSTITUTION_RULES,
    INSTITUTIONS,
    SEAT_INSTITUTION_RATINGS,
    SEATS,
)


def _get_or_create(db: Session, model, defaults: dict, **lookup):
    instance = db.query(model).filter_by(**lookup).first()
    if instance:
        for key, value in defaults.items():
            setattr(instance, key, value)
        return instance
    instance = model(**lookup, **defaults)
    db.add(instance)
    db.flush()
    return instance


def seed(db: Session) -> None:
    seat_by_name: dict[str, Seat] = {}
    for row in SEATS:
        seat = _get_or_create(
            db,
            Seat,
            defaults={k: v for k, v in row.items() if k != "name"},
            name=row["name"],
        )
        seat_by_name[row["name"]] = seat
    db.flush()

    institution_by_code: dict[str, Institution] = {}
    for row in INSTITUTIONS:
        home_seat = seat_by_name.get(row["home_seat_name"]) if row["home_seat_name"] else None
        institution = _get_or_create(
            db,
            Institution,
            defaults={
                "name": row["name"],
                "website_url": row["website_url"],
                "home_seat_id": home_seat.id if home_seat else None,
            },
            short_code=row["short_code"],
        )
        institution_by_code[row["short_code"]] = institution
    db.flush()

    for row in INSTITUTION_RULES:
        institution = institution_by_code[row["institution_short_code"]]
        _get_or_create(
            db,
            InstitutionRule,
            defaults={
                "version_year": row["version_year"],
                "summary": row["summary"],
                "source_url": row["source_url"],
            },
            institution_id=institution.id,
            rules_name=row["rules_name"],
        )

    for row in ANNUAL_REPORT_STATS:
        institution = institution_by_code[row["institution_short_code"]]
        _get_or_create(
            db,
            AnnualReportStat,
            defaults={
                "new_cases_filed": None,
                "avg_claim_value_usd": None,
                "avg_duration_months": None,
                "source_url": row["source_url"],
                "verified": False,
                "notes": row["notes"],
            },
            institution_id=institution.id,
            report_year=row["report_year"],
        )

    for row in FEE_SCHEDULES:
        institution = institution_by_code[row["institution_short_code"]]
        _get_or_create(
            db,
            FeeSchedule,
            defaults={
                "currency": row["currency"],
                "admin_fee_tiers": row["admin_fee_tiers"],
                "tribunal_fee_tiers": row["tribunal_fee_tiers"],
                "typical_duration_months_min": row["typical_duration_months_min"],
                "typical_duration_months_max": row["typical_duration_months_max"],
                "source_url": row["source_url"],
                "verified": False,
            },
            institution_id=institution.id,
            schedule_name=row["schedule_name"],
        )

    for seat_name, code, speed, cost, neutrality, enforceability, rationale in SEAT_INSTITUTION_RATINGS:
        seat = seat_by_name[seat_name]
        institution = institution_by_code[code]
        _get_or_create(
            db,
            SeatInstitutionRating,
            defaults={
                "speed_score": speed,
                "cost_score": cost,
                "neutrality_score": neutrality,
                "enforceability_score": enforceability,
                "rationale": rationale,
            },
            seat_id=seat.id,
            institution_id=institution.id,
        )

    db.commit()


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
