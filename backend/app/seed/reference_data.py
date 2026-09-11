"""Curated seed reference data for Arbitrium.

IMPORTANT — read before trusting this data in production:

* `SEATS`, `INSTITUTIONS`: structural/factual (jurisdiction, home seat,
  website) — low risk of being wrong, but still worth a periodic check.
* `INSTITUTION_RULES`: the five primary rule sources named explicitly in the
  PRD (Page 3). URLs and titles are taken verbatim from the PRD; version
  years are as published at time of writing.
* `ANNUAL_REPORT_STATS`: the four primary annual-report sources named in the
  PRD (Section 4). Numeric fields (case counts, average claim value, average
  duration) are deliberately left as `None` and `verified=False` — this
  project has no live access to those reports' actual figures, and
  fabricating plausible-looking statistics for a legal decision-support tool
  would be actively harmful. A human must pull the real numbers from the
  cited source and set `verified=True` before these are surfaced as fact.
* `FEE_SCHEDULES`: tier *structure* (ad valorem, declining marginal rate) is
  representative of how these institutions actually price claims, but the
  specific base/rate figures are illustrative placeholders, not the
  institutions' real published fee tables. `verified=False` on every row.
  Replace with the real numbers from each institution's fee calculator
  before using this for anything client-facing.
* `SEAT_INSTITUTION_RATINGS`: qualitative 1-5 judgments (not derived from a
  single hard metric) reflecting general, broadly-published reputational
  characteristics of these seats/institutions. Each carries a `rationale`
  explaining the judgment. These should be revisited once `verified=True`
  annual report data is loaded, so the recommendation engine can eventually
  be grounded in the real caseload/fee numbers rather than qualitative
  judgment alone.
"""

SEATS = [
    {
        "name": "London, UK",
        "country": "United Kingdom",
        "ny_convention_member": True,
        "supervisory_court": "High Court of Justice (Commercial Court)",
        "governing_statute": "Arbitration Act 1996 (England & Wales)",
        "notes": "Long-established seat with a well-developed supervisory case law body.",
    },
    {
        "name": "Singapore",
        "country": "Singapore",
        "ny_convention_member": True,
        "supervisory_court": "Singapore International Commercial Court / High Court",
        "governing_statute": "International Arbitration Act 1994",
        "notes": "Widely used neutral cross-border seat in Asia-Pacific.",
    },
    {
        "name": "Hong Kong SAR",
        "country": "Hong Kong SAR, China",
        "ny_convention_member": True,
        "supervisory_court": "Hong Kong Court of First Instance",
        "governing_statute": "Arbitration Ordinance (Cap. 609)",
        "notes": "NY Convention applies via China's accession, extended to Hong Kong SAR.",
    },
    {
        "name": "New York, USA",
        "country": "United States",
        "ny_convention_member": True,
        "supervisory_court": "U.S. District Court (S.D.N.Y.) / New York State courts",
        "governing_statute": "Federal Arbitration Act; New York CPLR Article 75",
        "notes": "Common choice for cross-border disputes with US-connected parties or assets.",
    },
    {
        "name": "Mumbai, India",
        "country": "India",
        "ny_convention_member": True,
        "supervisory_court": "Bombay High Court",
        "governing_statute": "Arbitration and Conciliation Act 1996 (India)",
        "notes": "Home seat of MCIA; also used for India-seated cross-border arbitration.",
    },
    {
        "name": "New Delhi, India",
        "country": "India",
        "ny_convention_member": True,
        "supervisory_court": "Delhi High Court",
        "governing_statute": "Arbitration and Conciliation Act 1996 (India)",
        "notes": "Common seat for domestic Indian arbitration.",
    },
]

INSTITUTIONS = [
    {
        "short_code": "LCIA",
        "name": "London Court of International Arbitration",
        "website_url": "https://www.lcia.org/",
        "home_seat_name": "London, UK",
    },
    {
        "short_code": "HKIAC",
        "name": "Hong Kong International Arbitration Centre",
        "website_url": "https://hkiac.org/",
        "home_seat_name": "Hong Kong SAR",
    },
    {
        "short_code": "ICDR",
        "name": "International Centre for Dispute Resolution (AAA)",
        "website_url": "https://www.icdr.org/",
        "home_seat_name": "New York, USA",
    },
    {
        "short_code": "SIAC",
        "name": "Singapore International Arbitration Centre",
        "website_url": "https://siac.org.sg/",
        "home_seat_name": "Singapore",
    },
    {
        "short_code": "MCIA",
        "name": "Mumbai Centre for International Arbitration",
        "website_url": "https://mcia.org.in/",
        "home_seat_name": "Mumbai, India",
    },
    {
        "short_code": "DIAC-DELHI",
        "name": "Delhi International Arbitration Centre",
        "website_url": "https://dhcdiac.nic.in/",
        "home_seat_name": "New Delhi, India",
    },
    {
        "short_code": "ICA",
        "name": "Indian Council of Arbitration",
        "website_url": "https://www.icaindia.co.in/",
        "home_seat_name": "New Delhi, India",
    },
    {
        "short_code": "IIAC",
        "name": "India International Arbitration Centre",
        "website_url": "https://iiac.gov.in/",
        "home_seat_name": "New Delhi, India",
    },
    {
        "short_code": "ADHOC",
        "name": "Ad Hoc (UNCITRAL Rules, no administering institution)",
        "website_url": None,
        "home_seat_name": None,
    },
]

# Page 3 — Live Rule Tracking & Components primary sources, taken from the PRD.
INSTITUTION_RULES = [
    {
        "institution_short_code": "LCIA",
        "rules_name": "LCIA Arbitration Rules 2020",
        "version_year": 2020,
        "source_url": "https://www.lcia.org/Dispute_Resolution_Services/lcia-arbitration-rules-2020.aspx",
        "summary": "Governs LCIA-administered arbitrations; covers commencement, tribunal formation, "
        "conduct of proceedings, and emergency arbitrator provisions.",
    },
    {
        "institution_short_code": "HKIAC",
        "rules_name": "HKIAC 2024 Administered Arbitration Rules",
        "version_year": 2024,
        "source_url": "https://hkiac.org/arbitration/rules-and-practice-notes/2024-administered-arbitration-rules/",
        "summary": "HKIAC's primary administered-arbitration rules, effective 2024.",
    },
    {
        "institution_short_code": "HKIAC",
        "rules_name": "HKIAC Procedures for Administration under UNCITRAL Rules (2015)",
        "version_year": 2015,
        "source_url": "https://hkiac.org/arbitration/rules-and-practice-notes/2015-procedures-administration-under-uncitral-rules/",
        "summary": "Procedures HKIAC applies when appointed to administer a case under the UNCITRAL "
        "Arbitration Rules rather than HKIAC's own rules.",
    },
    {
        "institution_short_code": "ICDR",
        "rules_name": "ICDR Rules, Forms & Fees",
        "version_year": None,
        "source_url": "https://www.icdr.org/rules_forms_fees",
        "summary": "ICDR's (AAA international division) current arbitration rules, forms, and fee schedule hub.",
    },
    {
        "institution_short_code": "SIAC",
        "rules_name": "SIAC Rules 2025",
        "version_year": 2025,
        "source_url": "https://siac.org.sg/siac-rules-2025",
        "summary": "SIAC's current administered-arbitration rules, effective 2025.",
    },
    {
        "institution_short_code": "MCIA",
        "rules_name": "MCIA Arbitration Rules 2016, revised 2025",
        "version_year": 2025,
        "source_url": "https://blog.ipleaders.in/arbitral-institutions-in-india/",
        "summary": "Domestic India-focused institutional rules noted by iPleaders as a natural fit for commercial disputes.",
    },
    {
        "institution_short_code": "DIAC-DELHI",
        "rules_name": "Delhi International Arbitration Centre Rules 2023",
        "version_year": 2023,
        "source_url": "https://blog.ipleaders.in/arbitral-institutions-in-india/",
        "summary": "Court-annexed Delhi rules; spell out the full institution name to avoid confusion with Dubai DIAC.",
    },
    {
        "institution_short_code": "ICA",
        "rules_name": "Indian Council of Arbitration Rules",
        "version_year": None,
        "source_url": "https://blog.ipleaders.in/arbitral-institutions-in-india/",
        "summary": "Older domestic institution with continued relevance for trade, commodity, and maritime disputes.",
    },
    {
        "institution_short_code": "IIAC",
        "rules_name": "India International Arbitration Centre Rules",
        "version_year": None,
        "source_url": "https://blog.ipleaders.in/arbitral-institutions-in-india/",
        "summary": "Statutory New Delhi institution created to support India's institutional arbitration framework.",
    },
]

# Section 4 — Cross-Border Data Index primary sources, taken from the PRD.
# Numeric figures intentionally left unset (see module docstring).
ANNUAL_REPORT_STATS = [
    {
        "institution_short_code": "ICDR",
        "report_year": 2024,
        "source_url": "https://www.adr.org/annual-reports/",
        "notes": "AAA/ICDR annual reports repository — pull the latest year's case "
        "count/value/duration figures here before setting verified=True.",
    },
    {
        "institution_short_code": "HKIAC",
        "report_year": 2024,
        "source_url": "https://hkiac.org/about-us/annual-report/",
        "notes": "HKIAC case statistics & annual report page — same caveat as above.",
    },
    {
        "institution_short_code": "LCIA",
        "report_year": 2024,
        "source_url": "https://www.lcia.org/lcia/reports.aspx",
        "notes": "LCIA reports & casework data — same caveat as above.",
    },
    {
        "institution_short_code": "SIAC",
        "report_year": 2024,
        "source_url": "https://siac.org.sg/annual-reports",
        "notes": "SIAC annual reports — same caveat as above.",
    },
]

# Illustrative ad valorem fee tier structure — NOT the institutions' real
# published figures. See module docstring.
def _tiers(base_multiplier: float, rate_multiplier: float, admin: bool) -> list[dict]:
    template = (
        [
            {"claim_min": 0, "claim_max": 100_000, "base": 1000, "rate_pct": 2.0},
            {"claim_min": 100_000, "claim_max": 1_000_000, "base": 3000, "rate_pct": 1.0},
            {"claim_min": 1_000_000, "claim_max": 10_000_000, "base": 12000, "rate_pct": 0.5},
            {"claim_min": 10_000_000, "claim_max": None, "base": 57000, "rate_pct": 0.1},
        ]
        if admin
        else [
            {"claim_min": 0, "claim_max": 100_000, "base": 5000, "rate_pct": 6.0},
            {"claim_min": 100_000, "claim_max": 1_000_000, "base": 11000, "rate_pct": 3.0},
            {"claim_min": 1_000_000, "claim_max": 10_000_000, "base": 38000, "rate_pct": 1.5},
            {"claim_min": 10_000_000, "claim_max": None, "base": 173000, "rate_pct": 0.3},
        ]
    )
    return [
        {
            **tier,
            "base": round(tier["base"] * base_multiplier, 2),
            "rate_pct": round(tier["rate_pct"] * rate_multiplier, 3),
        }
        for tier in template
    ]


FEE_SCHEDULES = [
    {
        "institution_short_code": "LCIA",
        "schedule_name": "LCIA Illustrative Fee Schedule (placeholder)",
        "currency": "USD",
        "admin_fee_tiers": _tiers(1.1, 1.1, admin=True),
        "tribunal_fee_tiers": _tiers(1.1, 1.1, admin=False),
        "typical_duration_months_min": 12,
        "typical_duration_months_max": 24,
        "source_url": "https://www.lcia.org/Dispute_Resolution_Services/lcia-arbitration-rules-2020.aspx",
    },
    {
        "institution_short_code": "HKIAC",
        "schedule_name": "HKIAC Illustrative Fee Schedule (placeholder)",
        "currency": "USD",
        "admin_fee_tiers": _tiers(1.0, 1.0, admin=True),
        "tribunal_fee_tiers": _tiers(1.0, 1.0, admin=False),
        "typical_duration_months_min": 12,
        "typical_duration_months_max": 20,
        "source_url": "https://hkiac.org/arbitration/rules-and-practice-notes/2024-administered-arbitration-rules/",
    },
    {
        "institution_short_code": "ICDR",
        "schedule_name": "ICDR Illustrative Fee Schedule (placeholder)",
        "currency": "USD",
        "admin_fee_tiers": _tiers(1.15, 1.15, admin=True),
        "tribunal_fee_tiers": _tiers(1.15, 1.15, admin=False),
        "typical_duration_months_min": 12,
        "typical_duration_months_max": 24,
        "source_url": "https://www.icdr.org/rules_forms_fees",
    },
    {
        "institution_short_code": "SIAC",
        "schedule_name": "SIAC Illustrative Fee Schedule (placeholder)",
        "currency": "USD",
        "admin_fee_tiers": _tiers(1.0, 1.0, admin=True),
        "tribunal_fee_tiers": _tiers(1.0, 1.0, admin=False),
        "typical_duration_months_min": 12,
        "typical_duration_months_max": 18,
        "source_url": "https://siac.org.sg/siac-rules-2025",
    },
    {
        "institution_short_code": "MCIA",
        "schedule_name": "MCIA Illustrative Fee Schedule (placeholder)",
        "currency": "USD",
        "admin_fee_tiers": _tiers(0.5, 0.6, admin=True),
        "tribunal_fee_tiers": _tiers(0.5, 0.6, admin=False),
        "typical_duration_months_min": 12,
        "typical_duration_months_max": 24,
        "source_url": "https://mcia.org.in/",
    },
    {
        "institution_short_code": "DIAC-DELHI",
        "schedule_name": "DIAC Delhi Illustrative Fee Schedule (placeholder)",
        "currency": "USD",
        "admin_fee_tiers": _tiers(0.45, 0.55, admin=True),
        "tribunal_fee_tiers": _tiers(0.45, 0.55, admin=False),
        "typical_duration_months_min": 10,
        "typical_duration_months_max": 22,
        "source_url": "https://dhcdiac.nic.in/",
    },
    {
        "institution_short_code": "ICA",
        "schedule_name": "ICA Illustrative Fee Schedule (placeholder)",
        "currency": "USD",
        "admin_fee_tiers": _tiers(0.4, 0.5, admin=True),
        "tribunal_fee_tiers": _tiers(0.4, 0.5, admin=False),
        "typical_duration_months_min": 12,
        "typical_duration_months_max": 24,
        "source_url": "https://www.icaindia.co.in/",
    },
    {
        "institution_short_code": "IIAC",
        "schedule_name": "IIAC Illustrative Fee Schedule (placeholder)",
        "currency": "USD",
        "admin_fee_tiers": _tiers(0.45, 0.55, admin=True),
        "tribunal_fee_tiers": _tiers(0.45, 0.55, admin=False),
        "typical_duration_months_min": 12,
        "typical_duration_months_max": 24,
        "source_url": "https://iiac.gov.in/",
    },
    {
        "institution_short_code": "ADHOC",
        "schedule_name": "Ad Hoc (UNCITRAL) Illustrative Fee Schedule (placeholder)",
        "currency": "USD",
        "admin_fee_tiers": _tiers(0.05, 0.1, admin=True),
        "tribunal_fee_tiers": _tiers(0.4, 0.5, admin=False),
        "typical_duration_months_min": 15,
        "typical_duration_months_max": 30,
        "source_url": "https://uncitral.un.org/en/texts/arbitration/contractualtexts/arbitration",
    },
]

# (seat_name, institution_short_code, speed, cost, neutrality, enforceability, rationale)
SEAT_INSTITUTION_RATINGS = [
    (
        "London, UK", "LCIA", 4, 3, 5, 5,
        "Mature supervisory courts and deep NY Convention enforcement case law; "
        "premium cost profile relative to Asian hubs.",
    ),
    (
        "Singapore", "SIAC", 4, 4, 5, 5,
        "Consistently ranked among the most-used neutral cross-border seats with "
        "efficient case management and strong enforcement record.",
    ),
    (
        "Hong Kong SAR", "HKIAC", 4, 4, 4, 4,
        "Strong Asia-Pacific hub with UNCITRAL-track and administered options; "
        "enforcement generally reliable via NY Convention through China's accession.",
    ),
    (
        "New York, USA", "ICDR", 3, 3, 4, 5,
        "Preferred where US-connected assets or parties are involved; proceedings can "
        "run longer due to broader discovery norms.",
    ),
    (
        "Mumbai, India", "MCIA", 3, 5, 3, 3,
        "Domestic commercial institution with a published fee schedule and a Mumbai seat; "
        "the iPleaders institutional-arbitration overview identifies MCIA as a natural "
        "choice for purely domestic commercial contracts.",
    ),
    (
        "New Delhi, India", "DIAC-DELHI", 4, 5, 3, 4,
        "Court-annexed Delhi institution with strong fit where Section 9, Section 11, "
        "or Section 34 access to the Delhi High Court is strategically important; use "
        "the full name to avoid confusion with Dubai DIAC.",
    ),
    (
        "New Delhi, India", "ICA", 3, 5, 3, 3,
        "Older domestic institution that remains useful for trade, commodity, and "
        "maritime contracts with an established ICA drafting history.",
    ),
    (
        "New Delhi, India", "IIAC", 3, 4, 3, 4,
        "Statutory institution intended to anchor India's institutional-arbitration "
        "policy; still building market volume relative to MCIA and DIAC.",
    ),
    (
        "New Delhi, India", "ADHOC", 2, 5, 3, 3,
        "Lowest direct cost (no institutional admin fee) but slower without institutional "
        "case-management deadlines; suitable mainly for domestic disputes under the "
        "Arbitration and Conciliation Act 1996.",
    ),
    (
        "Mumbai, India", "ADHOC", 2, 5, 3, 3,
        "Same ad hoc trade-offs as New Delhi; relevant for domestic Mumbai-seated disputes.",
    ),
]
