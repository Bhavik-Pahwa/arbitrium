from ingestion.corpus_store import CorpusStore
from ingestion.fetch import FetchedDocument


def make_doc(url, text, content_type="html"):
    return FetchedDocument(url=url, content_type=content_type, text=text, fetched_at="2026-01-01T00:00:00")


def test_ingest_and_list_sources(tmp_path):
    store = CorpusStore(tmp_path)
    doc = make_doc("http://siac.example/report", "SIAC administered 500 new cases in 2024, mostly construction disputes.")
    count = store.ingest_document(doc, institution="SIAC")
    assert count >= 1

    sources = store.list_sources()
    assert len(sources) == 1
    assert sources[0]["institution"] == "SIAC"
    assert sources[0]["source_url"] == "http://siac.example/report"


def test_search_returns_relevant_chunk(tmp_path):
    store = CorpusStore(tmp_path)
    store.ingest_document(
        make_doc("http://siac.example/report", "SIAC administered 500 new construction cases in 2024."),
        institution="SIAC",
    )
    store.ingest_document(
        make_doc("http://hkiac.example/report", "HKIAC handled 300 shipping disputes in 2024."),
        institution="HKIAC",
    )

    results = store.search("construction cases")
    assert len(results) >= 1
    assert results[0]["institution"] == "SIAC"
    assert "construction" in results[0]["text"].lower()


def test_search_filters_by_institution(tmp_path):
    store = CorpusStore(tmp_path)
    store.ingest_document(
        make_doc("http://siac.example/report", "SIAC administered 500 construction cases."),
        institution="SIAC",
    )
    store.ingest_document(
        make_doc("http://hkiac.example/report", "HKIAC administered 500 construction cases too."),
        institution="HKIAC",
    )

    results = store.search("construction cases", institution="HKIAC")
    assert all(r["institution"] == "HKIAC" for r in results)


def test_get_source_text_exact_for_single_chunk_document(tmp_path):
    store = CorpusStore(tmp_path)
    original = "The quick brown fox jumps over the lazy dog."
    store.ingest_document(make_doc("http://x/report", original), institution="SIAC")

    assert store.get_source_text("http://x/report") == original


def test_get_source_text_preserves_substrings_across_chunk_boundaries(tmp_path):
    store = CorpusStore(tmp_path)
    original = "The quick brown fox jumps over the lazy dog. " * 200
    store.ingest_document(make_doc("http://x/report", original), institution="SIAC")

    reassembled = store.get_source_text("http://x/report")
    assert reassembled is not None
    # any substring present in the original must still be findable after reassembly,
    # which is the property extraction/hallucination_guard.py actually relies on
    assert "quick brown fox jumps" in reassembled


def test_get_source_text_returns_none_for_unknown_source(tmp_path):
    store = CorpusStore(tmp_path)
    assert store.get_source_text("http://never-ingested.example") is None


def test_search_empty_corpus_returns_empty_list(tmp_path):
    store = CorpusStore(tmp_path)
    assert store.search("anything") == []
