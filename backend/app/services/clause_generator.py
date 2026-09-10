"""Template-based arbitration clause assembly + pathology checks.

Uses a generic clause skeleton (the common structure shared by essentially
all institutional model clauses: dispute reference, rules, seat, tribunal
size, appointment mechanism, language, governing law) rather than
reproducing any single institution's copyrighted model clause verbatim.
Users should still cross-check the final clause against the institution's
own published model clause before use.
"""

from dataclasses import dataclass

from app.models import Institution, Seat

ARBITRATOR_COUNT_TEXT = {
    "sole": "a sole arbitrator",
    "three": "three (3) arbitrators",
    "emergency": (
        "a sole arbitrator, provided that either party may apply for the "
        "emergency arbitrator provisions of the applicable rules pending "
        "constitution of the tribunal"
    ),
}

APPOINTMENT_TEXT = {
    "institutional_default": "in accordance with the default appointment procedure of the applicable rules",
    "co_arbitrator_nomination": (
        "with each party nominating one co-arbitrator and the two "
        "co-arbitrators nominating the presiding arbitrator"
    ),
    "presiding_officer": (
        "with the presiding arbitrator appointed by the appointing "
        "authority under the applicable rules"
    ),
}


@dataclass
class ClauseResult:
    text: str
    pathology_notes: list[str]


def _rules_reference(institution: Institution) -> str:
    if institution.short_code == "ADHOC":
        return "the UNCITRAL Arbitration Rules"
    return f"the Arbitration Rules of {institution.name} (the \"Rules\")"


def _administering_body(institution: Institution) -> str:
    if institution.short_code == "ADHOC":
        return "an ad hoc tribunal constituted under those rules, with no administering institution"
    return f"{institution.name} (\"{institution.short_code}\")"


def check_pathologies(
    seat: Seat,
    institution: Institution,
    num_arbitrators: str,
    appointment_mechanism: str,
    party_details: list,
) -> list[str]:
    notes: list[str] = []

    if num_arbitrators == "sole" and appointment_mechanism == "co_arbitrator_nomination":
        notes.append(
            "Co-arbitrator nomination is inconsistent with a sole-arbitrator tribunal "
            "(there are no co-arbitrators to nominate); the institutional default "
            "appointment procedure will apply instead."
        )

    if num_arbitrators == "three" and appointment_mechanism == "presiding_officer":
        notes.append(
            "Presiding-officer appointment alone does not specify how the two "
            "co-arbitrators are nominated for a three-member tribunal; consider "
            "co-arbitrator nomination plus a presiding-officer mechanism instead."
        )

    if institution.short_code == "ADHOC" and appointment_mechanism == "institutional_default":
        notes.append(
            "Ad hoc arbitration has no administering institution to apply an "
            "'institutional default' — the UNCITRAL Rules' appointing-authority "
            "mechanism will govern instead."
        )

    if institution.home_seat_id and institution.home_seat_id != seat.id:
        notes.append(
            f"{institution.short_code}'s home jurisdiction differs from the selected "
            f"seat ({seat.name}); confirm {institution.short_code} can administer "
            f"cases seated outside its home jurisdiction (most major institutions can, "
            f"but this should be verified against the current Rules)."
        )

    if len(party_details) < 2:
        notes.append(
            "Fewer than two parties supplied — a clause needs at least two identified "
            "parties to be complete."
        )

    if not notes:
        notes.append("No pathologies detected against the structural checks applied.")

    return notes


def generate(
    seat: Seat,
    institution: Institution,
    num_arbitrators: str,
    appointment_mechanism: str,
    language: str,
    governing_law_contract: str,
    governing_law_arbitration: str,
    party_details: list,
) -> ClauseResult:
    pathology_notes = check_pathologies(
        seat, institution, num_arbitrators, appointment_mechanism, party_details
    )

    text = (
        f"Any dispute, controversy, or claim arising out of or relating to this contract, "
        f"including its formation, interpretation, breach, or termination, shall be referred "
        f"to and finally resolved by arbitration administered by {_administering_body(institution)} "
        f"under {_rules_reference(institution)} in force at the time the arbitration is commenced.\n\n"
        f"The seat (legal place) of arbitration shall be {seat.name}, {seat.country}.\n\n"
        f"The arbitral tribunal shall consist of {ARBITRATOR_COUNT_TEXT[num_arbitrators]}, "
        f"appointed {APPOINTMENT_TEXT[appointment_mechanism]}.\n\n"
        f"The language of the arbitration shall be {language}.\n\n"
        f"This contract shall be governed by and construed in accordance with the laws of "
        f"{governing_law_contract}. This arbitration agreement shall be governed by the laws of "
        f"{governing_law_arbitration}, without prejudice to the substantive law governing the "
        f"contract as a whole."
    )

    return ClauseResult(text=text, pathology_notes=pathology_notes)
