from extraction.hallucination_guard import check_fact, filter_verified_facts
from extraction.schemas import ExtractedFact
from ingestion.corpus_store import CorpusStore
from ingestion.fetch import FetchedDocument


def make_store(tmp_path, url, text, institution="SIAC"):
    store = CorpusStore(tmp_path)
    doc = FetchedDocument(url=url, content_type="html", text=text, fetched_at="2026-01-01T00:00:00")
    store.ingest_document(doc, institution=institution)
    return store


def test_accepts_fact_with_real_verbatim_excerpt(tmp_path):
    store = make_store(tmp_path, "http://x/report", "SIAC administered 663 new cases in 2024.")
    fact = ExtractedFact(
        institution="SIAC",
        report_year=2024,
        metric="new_cases_filed",
        status="disclosed",
        numeric_value=663,
        unit="cases",
        source_url="http://x/report",
        source_excerpt="SIAC administered 663 new cases in 2024.",
    )
    passed, reason = check_fact(fact, store)
    assert passed, reason


def test_rejects_fact_with_invented_excerpt(tmp_path):
    store = make_store(tmp_path, "http://x/report", "SIAC administered 663 new cases in 2024.")
    fact = ExtractedFact(
        institution="SIAC",
        report_year=2024,
        metric="new_cases_filed",
        status="disclosed",
        numeric_value=999,
        unit="cases",
        source_url="http://x/report",
        source_excerpt="SIAC administered 999 new cases in 2024.",  # not actually in the source
    )
    passed, reason = check_fact(fact, store)
    assert not passed


def test_rejects_fact_whose_number_is_not_in_the_excerpt(tmp_path):
    store = make_store(
        tmp_path,
        "http://x/report",
        "SIAC's caseload grew steadily. The tribunal noted various figures throughout the year.",
    )
    fact = ExtractedFact(
        institution="SIAC",
        report_year=2024,
        metric="new_cases_filed",
        status="disclosed",
        numeric_value=663,
        unit="cases",
        source_url="http://x/report",
        # excerpt is a real substring, but never actually states 663
        source_excerpt="SIAC's caseload grew steadily.",
    )
    passed, reason = check_fact(fact, store)
    assert not passed


def test_not_disclosed_facts_require_no_excerpt(tmp_path):
    store = make_store(tmp_path, "http://x/report", "SIAC did not break down cases by sector this year.")
    fact = ExtractedFact(
        institution="SIAC",
        report_year=2024,
        metric="case_count_by_sector",
        dimension="sector",
        dimension_value="construction",
        status="not_disclosed",
        numeric_value=None,
        source_url="http://x/report",
        source_excerpt=None,
    )
    passed, reason = check_fact(fact, store)
    assert passed, reason


def test_unknown_source_url_is_rejected(tmp_path):
    store = CorpusStore(tmp_path)
    fact = ExtractedFact(
        institution="SIAC",
        metric="new_cases_filed",
        status="disclosed",
        numeric_value=663,
        source_url="http://never-ingested.example",
        source_excerpt="663 new cases",
    )
    passed, reason = check_fact(fact, store)
    assert not passed


def test_filter_verified_facts_splits_accepted_and_rejected(tmp_path):
    store = make_store(tmp_path, "http://x/report", "SIAC administered 663 new cases in 2024.")
    good = ExtractedFact(
        institution="SIAC",
        metric="new_cases_filed",
        status="disclosed",
        numeric_value=663,
        source_url="http://x/report",
        source_excerpt="SIAC administered 663 new cases in 2024.",
    )
    bad = ExtractedFact(
        institution="SIAC",
        metric="new_cases_filed",
        status="disclosed",
        numeric_value=42,
        source_url="http://x/report",
        source_excerpt="a made up sentence with 42 in it",
    )
    accepted, rejected = filter_verified_facts([good, bad], store)
    assert len(accepted) == 1
    assert len(rejected) == 1
    assert accepted[0].numeric_value == 663
