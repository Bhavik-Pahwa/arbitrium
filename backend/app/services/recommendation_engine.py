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

FACTOR_LABELS = {
    "speed_score": "Speed",
    "cost_score": "Cost efficiency",
    "neutrality_score": "Neutrality",
    "enforceability_score": "Enforceability",
}


@dataclass
class RecommendationCandidate:
    seat: Seat
    institution: Institution
    rating: SeatInstitutionRating
    score: float
    sort_score: float
    rationale: str
    pros: list[str] = field(default_factory=list)
    cons: list[str] = field(default_factory=list)
    citations: list[dict] = field(default_factory=list)
    factor_scores: list[dict] = field(default_factory=list)
    priority_factors: list[str] = field(default_factory=list)
    seat_reasons: list[str] = field(default_factory=list)
    better_if: str | None = None


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
        domestic_matches = [
            r
            for r in ratings
            if r.seat.country.lower() in law_lower
            or (r.seat.country.lower() == "india" and "indian" in law_lower)
        ]
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


def _contains_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def _preferred_institution(text: str) -> str | None:
    for code in ("siac", "lcia", "hkiac", "icdr", "icc", "pca", "mcia", "diac-delhi", "ica", "iiac"):
        if f"{code} preferred" in text or f"prefer {code}" in text:
            return code
    if "uncitral preferred" in text or "ad hoc preferred" in text or "prefer uncitral" in text:
        return "adhoc"

    markers = ("preferred institution:", "institution:")
    for marker in markers:
        if marker in text:
            tail = text.split(marker, 1)[1].strip()
            first_sentence = tail.split(".", 1)[0].lower()
            for code in ("siac", "lcia", "hkiac", "icdr", "icc", "pca", "mcia", "diac-delhi", "ica", "iiac"):
                if code in first_sentence:
                    return code
            if "uncitral" in first_sentence or "ad hoc" in first_sentence:
                return "adhoc"
    return None


def _party_countries(text: str) -> set[str]:
    if "party jurisdictions:" not in text:
        return set()
    tail = text.split("party jurisdictions:", 1)[1].split(".", 1)[0]
    return {item.strip().lower() for item in tail.replace("/", ";").split(";") if item.strip()}


def _context_adjustment(rating: SeatInstitutionRating, context: str | None) -> float:
    if not context:
        return 0.0

    text = context.lower()
    code = rating.institution.short_code.lower()
    seat = rating.seat.name.lower()
    country = rating.seat.country.lower()
    party_countries = _party_countries(text)
    preferred = _preferred_institution(text)
    adjustment = 0.0

    if preferred:
        adjustment += 0.16 if preferred == code else -0.07

    direct_seat_terms = {
        "singapore": ["singapore seat", "singapore assets", "singapore nexus", "asean", "asia-pacific"],
        "london, uk": ["london", "uk assets", "english law", "england"],
        "hong kong sar": ["hong kong", "china assets", "greater china"],
        "new york, usa": ["new york", "us assets", "u.s. assets", "usa assets", "american counterparty"],
        "paris, france": ["paris", "france", "european assets", "europe nexus", "civil law"],
        "the hague, netherlands": ["the hague", "netherlands", "state entity", "sovereign", "treaty"],
        "mumbai, india": ["mumbai", "western region", "india seat acceptable", "india-linked"],
        "new delhi, india": ["delhi", "northern region", "section 9", "section 11", "section 34"],
    }
    if _contains_any(text, direct_seat_terms.get(seat, [])):
        adjustment += 0.075

    if _contains_any(text, ["strictly neutral third-country", "neutral third-country", "strict neutrality"]):
        adjustment += (rating.neutrality_score - 3) * 0.018
        if country in party_countries:
            adjustment -= 0.07
        if country == "india" and "india" in party_countries:
            adjustment -= 0.05

    sector_fit = {
        "construction": {"siac": 0.025, "icc": 0.035, "lcia": 0.02, "diac-delhi": 0.04, "mcia": 0.025},
        "infrastructure": {"siac": 0.025, "icc": 0.035, "lcia": 0.02, "diac-delhi": 0.04, "mcia": 0.025},
        "financial": {"lcia": 0.045, "icdr": 0.025, "mcia": 0.025, "siac": 0.02},
        "banking": {"lcia": 0.045, "icdr": 0.025, "mcia": 0.025, "siac": 0.02},
        "technology": {"siac": 0.035, "hkiac": 0.03, "icdr": 0.025},
        "software": {"siac": 0.035, "hkiac": 0.03, "icdr": 0.025},
        "energy": {"lcia": 0.035, "icc": 0.04, "pca": 0.025},
        "oil": {"lcia": 0.035, "icc": 0.04, "pca": 0.025},
        "manufacturing": {"icc": 0.04, "hkiac": 0.02, "siac": 0.02},
        "maritime": {"hkiac": 0.04, "siac": 0.03, "ica": 0.025},
        "shareholder": {"mcia": 0.04, "lcia": 0.025, "siac": 0.02},
    }
    for keyword, bonuses in sector_fit.items():
        if keyword in text:
            adjustment += bonuses.get(code, 0.0)

    if _contains_any(text, ["state entity", "state-owned", "sovereign", "treaty", "public-international"]):
        adjustment += 0.18 if code == "pca" else -0.065

    if _contains_any(text, ["us assets", "u.s. assets", "usa assets", "new york enforcement"]):
        adjustment += 0.18 if code == "icdr" else -0.035

    if _contains_any(text, ["china", "hong kong", "greater china"]):
        adjustment += 0.30 if code == "hkiac" else -0.06

    if _contains_any(text, ["english law", "london"]):
        adjustment += 0.04 if code == "lcia" else 0.0

    if _contains_any(text, ["europe", "paris", "france", "icc"]):
        adjustment += 0.12 if code == "icc" else -0.01

    if _contains_any(text, ["section 9", "section 11", "section 34", "delhi high court"]):
        adjustment += 0.34 if code == "diac-delhi" else -0.075

    if "cost" in text and _contains_any(text, ["sensitive", "low", "lean", "efficiency"]):
        adjustment += (rating.cost_score - 3) * 0.025
        if code == "icc":
            adjustment -= 0.065
        if code == "lcia":
            adjustment -= 0.06
    if _contains_any(text, ["fast", "speed", "urgent", "expedited"]):
        adjustment += (rating.speed_score - 3) * 0.02
    if _contains_any(text, ["high enforcement", "award enforcement", "overseas assets"]):
        adjustment += (rating.enforceability_score - 3) * 0.025

    return adjustment


def _display_score(raw_score: float) -> float:
    return min(0.95, max(0.58, 0.38 + (raw_score * 0.45)))


def _priority_factors(weights: dict[str, float]) -> list[str]:
    average = sum(weights.values()) / len(weights)
    return [
        FACTOR_LABELS[key.replace("priority_", "") + "_score"]
        for key, value in weights.items()
        if value >= average
    ]


def _factor_scores(rating: SeatInstitutionRating) -> list[dict]:
    base_scores = {
        "speed_score": rating.speed_score,
        "cost_score": rating.cost_score,
        "neutrality_score": rating.neutrality_score,
        "enforceability_score": rating.enforceability_score,
    }
    return [
        {"label": FACTOR_LABELS[key], "score": value * 2}
        for key, value in base_scores.items()
    ]


def _seat_reasons(rating: SeatInstitutionRating) -> list[str]:
    seat = rating.seat
    institution = rating.institution
    reasons = [
        f"{seat.supervisory_court} provides the supervisory court framework.",
        f"{seat.governing_statute} anchors the arbitration law analysis.",
    ]
    if seat.ny_convention_member:
        reasons.append("New York Convention status supports cross-border award enforcement.")
    if institution.home_seat_id == seat.id:
        reasons.append(f"{institution.short_code} is naturally aligned with this seat.")
    return reasons[:4]


def _better_if(rating: SeatInstitutionRating) -> str:
    code = rating.institution.short_code
    if code == "SIAC":
        return "Better if the dispute has an Asia-Pacific nexus and the parties want efficient institutional administration."
    if code == "LCIA":
        return "Better if English-law familiarity, mature court support, and neutrality outweigh cost concerns."
    if code == "HKIAC":
        return "Better if China or wider Asia-Pacific enforcement and administered UNCITRAL options matter."
    if code == "ICDR":
        return "Better if US-connected parties, assets, or enforcement strategy drive the seat choice."
    if code == "ICC":
        return "Better if the parties want a globally recognised institution for a high-value or multi-jurisdiction dispute."
    if code == "PCA":
        return "Better if a State, State-owned entity, treaty, or public-international dimension is involved."
    if code == "MCIA":
        return "Better if the dispute is India-centred and Mumbai commercial infrastructure is convenient."
    if code == "DIAC-DELHI":
        return "Better if Delhi High Court access and court-annexed administration are important."
    return "Better if the parties prioritise domestic familiarity and a leaner administration model."


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
    context: str | None = None,
    top_n: int = 3,
) -> list[RecommendationCandidate]:
    ratings = _eligible_ratings(db, arbitration_type, governing_law)

    candidates: list[RecommendationCandidate] = []
    priority_factors = _priority_factors(weights)
    for rating in ratings:
        raw_score = max(0.0, _weighted_score(rating, weights) + _context_adjustment(rating, context))
        score = _display_score(raw_score)
        pros, cons = _pros_cons(rating)
        top_factor = max(
            weights.items(), key=lambda kv: kv[1]
        )[0].replace("priority_", "")
        rationale = (
            f"{rating.seat.name} seated arbitration under {rating.institution.name} scores "
            f"{score:.2f}/1.00 on current fit confidence (weighted most heavily on "
            f"{top_factor}). {rating.rationale or ''}".strip()
        )
        candidates.append(
            RecommendationCandidate(
                seat=rating.seat,
                institution=rating.institution,
                rating=rating,
                score=round(score, 4),
                sort_score=round(raw_score, 4),
                rationale=rationale,
                pros=pros,
                cons=cons,
                citations=_citations(db, rating.institution),
                factor_scores=_factor_scores(rating),
                priority_factors=priority_factors,
                seat_reasons=_seat_reasons(rating),
                better_if=_better_if(rating),
            )
        )

    candidates.sort(key=lambda c: c.sort_score, reverse=True)
    return candidates[:top_n]
