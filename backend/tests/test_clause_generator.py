from app.models.institution import Institution
from app.models.seat import Seat
from app.schemas.seat_allocation import PartyDetail
from app.services import clause_generator


def make_seat(id_=1) -> Seat:
    seat = Seat(name="Singapore", country="Singapore", ny_convention_member=True)
    seat.id = id_
    return seat


def make_institution(home_seat_id=1, short_code="SIAC") -> Institution:
    inst = Institution(short_code=short_code, name="Singapore International Arbitration Centre")
    inst.home_seat_id = home_seat_id
    return inst


def make_parties():
    return [
        PartyDetail(name="Acme Corp", role="Claimant"),
        PartyDetail(name="Globex Ltd", role="Respondent"),
    ]


def test_generated_text_includes_seat_and_institution():
    seat = make_seat()
    institution = make_institution()
    result = clause_generator.generate(
        seat=seat,
        institution=institution,
        num_arbitrators="three",
        appointment_mechanism="co_arbitrator_nomination",
        language="English",
        governing_law_contract="Singapore",
        governing_law_arbitration="Singapore",
        party_details=make_parties(),
    )
    assert "Singapore" in result.text
    assert "Singapore International Arbitration Centre" in result.text
    assert "three (3) arbitrators" in result.text


def test_sole_arbitrator_with_co_arbitrator_nomination_flags_pathology():
    seat = make_seat()
    institution = make_institution()
    result = clause_generator.generate(
        seat=seat,
        institution=institution,
        num_arbitrators="sole",
        appointment_mechanism="co_arbitrator_nomination",
        language="English",
        governing_law_contract="Singapore",
        governing_law_arbitration="Singapore",
        party_details=make_parties(),
    )
    assert any("inconsistent with a sole-arbitrator tribunal" in note for note in result.pathology_notes)


def test_clean_configuration_has_no_pathology_flags():
    seat = make_seat()
    institution = make_institution()
    result = clause_generator.generate(
        seat=seat,
        institution=institution,
        num_arbitrators="three",
        appointment_mechanism="co_arbitrator_nomination",
        language="English",
        governing_law_contract="Singapore",
        governing_law_arbitration="Singapore",
        party_details=make_parties(),
    )
    assert result.pathology_notes == ["No pathologies detected against the structural checks applied."]


def test_fewer_than_two_parties_flags_pathology():
    seat = make_seat()
    institution = make_institution()
    result = clause_generator.generate(
        seat=seat,
        institution=institution,
        num_arbitrators="sole",
        appointment_mechanism="institutional_default",
        language="English",
        governing_law_contract="Singapore",
        governing_law_arbitration="Singapore",
        party_details=[PartyDetail(name="Acme Corp", role="Claimant")],
    )
    assert any("Fewer than two parties" in note for note in result.pathology_notes)
