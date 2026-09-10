"""Rules-based seat/institution recommendation engine.

Deliberately transparent and deterministic rather than a black-box model:
every score is a weighted sum of curated 1-5 ratings
(SeatInstitutionRating), and every citation traces back to a stored
source_url from the seed reference data. This matches the PRD's requirement
for "defensible" recommendations with "sourced citations".
"""

from dataclasses import dataclass, field

from sqlalchemy.orm import Session

from app.models import (
    AnnualReportStat,
    Institution,
    InstitutionRule,
    Seat,
    SeatInstitutionRating,
)

DIMENSION_LABELS = {
    "speed_score": "Speed (time to award)",
    "cost_score": "Cost (administrative & tribunal fees)",
    "neutrality_score": "Neutrality (forum independence)",
    "enforceability_score": "Enforceability (asset enforcement security)",
}


@dataclass
class RecommendationCandidate:
    seat: Seat
    institution: Institution
    rating: SeatInstitutionRating
    score: float
    rationale: str
    pros: list[str] = field(default_factory=list)
    cons: list[str] = field(default_factory=list)
    citations: list[dict] = field(default_factory=list)


def _eligible_ratings(
    db: Session, arbitration_type: str, governing_law: str | None
) -> list[SeatInstitutionRating]:
    ratings = (
        db.query(SeatInstitutionRating)
        .join(Seat, SeatInstitutionRating.seat_id == Seat.id)
        .all()
    )

    if arbitration_type == "cross_border":
        return [r for r in ratings if r.seat.ny_convention_member]

    if governing_law:
        law_lower = governing_law.lower()
        domestic_matches = [r for r in ratings if r.seat.country.lower() in law_lower]
        if domestic_matches:
            return domestic_matches

    # No governing law supplied or no country match found — fall back to all
    # seats rather than returning an empty result set.
    return ratings


def _weighted_score(rating: SeatInstitutionRating, weights: dict[str, float]) -> float:
    return (
        rating.speed_score * weights["priority_speed"]
        + rating.cost_score * weights["priority_cost"]
        + rating.neutrality_score * weights["priority_neutrality"]
        + rating.enforceability_score * weights["priority_enforceability"]
    ) / 5.0


def _pros_cons(rating: SeatInstitutionRating) -> tuple[list[str], list[str]]:
    dims = {
        "speed_score": rating.speed_score,
        "cost_score": rating.cost_score,
        "neutrality_score": rating.neutrality_score,
        "enforceability_score": rating.enforceability_score,
    }
    ranked = sorted(dims.items(), key=lambda kv: kv[1], reverse=True)
    pros = [f"{DIMENSION_LABELS[k]}: {v}/5" for k, v in ranked[:2]]
    cons = [f"{DIMENSION_LABELS[k]}: {v}/5" for k, v in ranked[-2:] if v <= 3]
    return pros, cons


def _citations(db: Session, institution: Institution) -> list[dict]:
    citations: list[dict] = []
    rules = (
        db.query(InstitutionRule)
        .filter(InstitutionRule.institution_id == institution.id)
        .all()
    )
    for r in rules:
        citations.append({"label": r.rules_name, "url": r.source_url, "type": "rules"})

    stats = (
        db.query(AnnualReportStat)
        .filter(AnnualReportStat.institution_id == institution.id)
        .all()
    )
    for s in stats:
        citations.append(
            {
                "label": f"{institution.short_code} Annual Report {s.report_year}",
                "url": s.source_url,
                "type": "annual_report",
            }
        )
    return citations


def recommend(
    db: Session,
    arbitration_type: str,
    governing_law: str | None,
    weights: dict[str, float],
    top_n: int = 3,
) -> list[RecommendationCandidate]:
    ratings = _eligible_ratings(db, arbitration_type, governing_law)

    candidates: list[RecommendationCandidate] = []
    for rating in ratings:
        score = _weighted_score(rating, weights)
        pros, cons = _pros_cons(rating)
        top_factor = max(
            weights.items(), key=lambda kv: kv[1]
        )[0].replace("priority_", "")
        rationale = (
            f"{rating.seat.name} seated arbitration under {rating.institution.name} scores "
            f"{score:.2f}/1.00 given your stated priorities (weighted most heavily on "
            f"{top_factor}). {rating.rationale or ''}".strip()
        )
        candidates.append(
            RecommendationCandidate(
                seat=rating.seat,
                institution=rating.institution,
                rating=rating,
                score=round(score, 4),
                rationale=rationale,
                pros=pros,
                cons=cons,
                citations=_citations(db, rating.institution),
            )
        )

    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates[:top_n]
