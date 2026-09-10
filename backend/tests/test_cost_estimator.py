from app.models.fee_schedule import FeeSchedule
from app.services import cost_estimator

TIERS = [
    {"claim_min": 0, "claim_max": 100_000, "base": 1000, "rate_pct": 2.0},
    {"claim_min": 100_000, "claim_max": 1_000_000, "base": 3000, "rate_pct": 1.0},
    {"claim_min": 1_000_000, "claim_max": None, "base": 12000, "rate_pct": 0.5},
]


def make_schedule() -> FeeSchedule:
    return FeeSchedule(
        schedule_name="Test Schedule",
        currency="USD",
        admin_fee_tiers=TIERS,
        tribunal_fee_tiers=TIERS,
        typical_duration_months_min=12,
        typical_duration_months_max=24,
        source_url="https://example.com",
        verified=False,
    )


def test_low_tier_claim_uses_first_bracket():
    result = cost_estimator.estimate(make_schedule(), 50_000)
    # base 1000 + 2% of 50,000 = 1000 + 1000 = 2000
    assert result["estimated_admin_fee"] == 2000.0


def test_mid_tier_claim_uses_correct_bracket():
    result = cost_estimator.estimate(make_schedule(), 500_000)
    # base 3000 + 1% of (500,000 - 100,000) = 3000 + 4000 = 7000
    assert result["estimated_admin_fee"] == 7000.0


def test_top_open_ended_tier():
    result = cost_estimator.estimate(make_schedule(), 5_000_000)
    # base 12000 + 0.5% of (5,000,000 - 1,000,000) = 12000 + 20000 = 32000
    assert result["estimated_admin_fee"] == 32000.0


def test_tribunal_fee_range_brackets_point_estimate():
    result = cost_estimator.estimate(make_schedule(), 500_000)
    point = result["breakdown"]["tribunal_fee_point_estimate"]
    assert result["estimated_tribunal_fee_min"] == round(point * 0.8, 2)
    assert result["estimated_tribunal_fee_max"] == round(point * 1.2, 2)


def test_duration_passed_through_from_schedule():
    result = cost_estimator.estimate(make_schedule(), 100_000)
    assert result["estimated_duration_months_min"] == 12
    assert result["estimated_duration_months_max"] == 24
