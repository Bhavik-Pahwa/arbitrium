from app.models.institution import Institution
from app.models.seat import Seat
from app.models.seat_rating import SeatInstitutionRating
from app.services import recommendation_engine as engine


def make_rating(speed, cost, neutrality, enforceability) -> SeatInstitutionRating:
    seat = Seat(name="Singapore", country="Singapore", ny_convention_member=True)
    institution = Institution(short_code="SIAC", name="Singapore International Arbitration Centre")
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
