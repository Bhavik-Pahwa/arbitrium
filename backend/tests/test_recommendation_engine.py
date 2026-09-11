from app.models.institution import Institution
from app.models.seat import Seat
from app.models.seat_rating import SeatInstitutionRating
from app.services import recommendation_engine as engine


def make_rating(
    speed,
    cost,
    neutrality,
    enforceability,
    seat_name="Singapore",
    country="Singapore",
    institution_code="SIAC",
    institution_name="Singapore International Arbitration Centre",
) -> SeatInstitutionRating:
    seat = Seat(
        name=seat_name,
        country=country,
        ny_convention_member=True,
        supervisory_court="Test court",
        governing_statute="Test statute",
    )
    institution = Institution(short_code=institution_code, name=institution_name)
    rating = SeatInstitutionRating(
        speed_score=speed,
        cost_score=cost,
        neutrality_score=neutrality,
        enforceability_score=enforceability,
        rationale="test",
    )
    rating.seat = seat
    rating.institution = institution
    return rating


def test_weighted_score_favors_highest_weighted_dimension():
    rating = make_rating(speed=5, cost=1, neutrality=1, enforceability=1)
    weights_speed_heavy = {
        "priority_speed": 1.0,
        "priority_cost": 0.0,
        "priority_neutrality": 0.0,
        "priority_enforceability": 0.0,
    }
    weights_cost_heavy = {
        "priority_speed": 0.0,
        "priority_cost": 1.0,
        "priority_neutrality": 0.0,
        "priority_enforceability": 0.0,
    }
    speed_score = engine._weighted_score(rating, weights_speed_heavy)
    cost_score = engine._weighted_score(rating, weights_cost_heavy)
    assert speed_score == 1.0
    assert cost_score == 0.2
    assert speed_score > cost_score


def test_equal_weights_average_all_dimensions():
    rating = make_rating(speed=4, cost=4, neutrality=4, enforceability=4)
    equal_weights = {
        "priority_speed": 0.25,
        "priority_cost": 0.25,
        "priority_neutrality": 0.25,
        "priority_enforceability": 0.25,
    }
    assert engine._weighted_score(rating, equal_weights) == 0.8


def test_pros_cons_surfaces_strongest_and_weakest_dimensions():
    rating = make_rating(speed=5, cost=5, neutrality=2, enforceability=2)
    pros, cons = engine._pros_cons(rating)
    assert any("Speed" in p for p in pros)
    assert any("Cost" in p for p in pros)
    assert any("Neutrality" in c for c in cons)
    assert any("Enforceability" in c for c in cons)


def test_context_adjustment_can_break_siac_default_tie():
    siac = make_rating(speed=4, cost=4, neutrality=5, enforceability=5)
    icc = make_rating(
        speed=3,
        cost=3,
        neutrality=5,
        enforceability=5,
        seat_name="Paris, France",
        country="France",
        institution_code="ICC",
        institution_name="International Chamber of Commerce",
    )
    context = "Preferred institution: ICC. Europe and Paris nexus."

    assert engine._context_adjustment(icc, context) > engine._context_adjustment(siac, context)


def test_hong_kong_context_overrides_generic_finance_pull():
    hkiac = make_rating(
        speed=4,
        cost=4,
        neutrality=4,
        enforceability=4,
        seat_name="Hong Kong SAR",
        country="Hong Kong SAR, China",
        institution_code="HKIAC",
        institution_name="Hong Kong International Arbitration Centre",
    )
    lcia = make_rating(
        speed=4,
        cost=3,
        neutrality=5,
        enforceability=5,
        seat_name="London, UK",
        country="United Kingdom",
        institution_code="LCIA",
        institution_name="London Court of International Arbitration",
    )
    context = "Sector: financial services banking. China assets, Hong Kong enforcement."

    assert engine._context_adjustment(hkiac, context) > engine._context_adjustment(lcia, context)


def test_section_9_context_overrides_generic_london_pull():
    diac = make_rating(
        speed=4,
        cost=5,
        neutrality=3,
        enforceability=4,
        seat_name="New Delhi, India",
        country="India",
        institution_code="DIAC-DELHI",
        institution_name="Delhi International Arbitration Centre",
    )
    lcia = make_rating(
        speed=4,
        cost=3,
        neutrality=5,
        enforceability=5,
        seat_name="London, UK",
        country="United Kingdom",
        institution_code="LCIA",
        institution_name="London Court of International Arbitration",
    )
    context = "Sector: financial services banking. India project with Section 9 interim relief and Delhi High Court urgency."

    assert engine._context_adjustment(diac, context) > engine._context_adjustment(lcia, context)


def test_display_score_is_calibrated_below_perfect():
    assert engine._display_score(1.5) == 0.95
