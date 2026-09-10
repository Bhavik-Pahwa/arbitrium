"""Tiered ad-valorem fee calculator.

Evaluates a claim amount against a FeeSchedule's admin/tribunal fee tiers.
Each tier is {"claim_min": float, "claim_max": float|None, "base": float,
"rate_pct": float}: fee = base + rate_pct% of the portion of the claim
that falls within [claim_min, claim_max).
"""

from app.models import FeeSchedule


def _apply_tiers(tiers: list[dict], claim_amount: float) -> float:
    for tier in tiers:
        claim_min = tier["claim_min"]
        claim_max = tier.get("claim_max")
        if claim_amount >= claim_min and (claim_max is None or claim_amount < claim_max):
            portion = claim_amount - claim_min
            return round(tier["base"] + portion * (tier["rate_pct"] / 100.0), 2)
    # Claim amount below the lowest tier's floor — use the first tier's base fee.
    return round(tiers[0]["base"], 2) if tiers else 0.0


def estimate(fee_schedule: FeeSchedule, claim_amount: float) -> dict:
    admin_fee = _apply_tiers(fee_schedule.admin_fee_tiers, claim_amount)
    tribunal_fee = _apply_tiers(fee_schedule.tribunal_fee_tiers, claim_amount)

    # Tribunal fees vary more with tribunal composition/complexity than admin
    # fees do, so we present a +/-20% band around the calculated point estimate.
    tribunal_min = round(tribunal_fee * 0.8, 2)
    tribunal_max = round(tribunal_fee * 1.2, 2)

    return {
        "estimated_admin_fee": admin_fee,
        "estimated_tribunal_fee_min": tribunal_min,
        "estimated_tribunal_fee_max": tribunal_max,
        "estimated_duration_months_min": fee_schedule.typical_duration_months_min or 0,
        "estimated_duration_months_max": fee_schedule.typical_duration_months_max or 0,
        "breakdown": {
            "schedule_name": fee_schedule.schedule_name,
            "currency": fee_schedule.currency,
            "claim_amount": claim_amount,
            "admin_fee": admin_fee,
            "tribunal_fee_point_estimate": tribunal_fee,
            "tribunal_fee_range": [tribunal_min, tribunal_max],
            "source_url": fee_schedule.source_url,
            "verified": fee_schedule.verified,
        },
    }
