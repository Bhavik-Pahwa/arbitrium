import pytest

from ingestion.chunker import chunk_text


def test_short_text_produces_single_chunk():
    chunks = chunk_text("hello world", source_url="http://x", institution="SIAC", chunk_size=100, overlap=10)
    assert len(chunks) == 1
    assert chunks[0].text == "hello world"
    assert chunks[0].char_start == 0
    assert chunks[0].char_end == len("hello world")


def test_long_text_splits_with_overlap():
    text = "a" * 250
    chunks = chunk_text(text, source_url="http://x", institution="SIAC", chunk_size=100, overlap=20)
    assert len(chunks) > 1
    # consecutive chunks overlap by exactly `overlap` characters
    for i in range(len(chunks) - 1):
        assert chunks[i + 1].char_start == chunks[i].char_end - 20


def test_chunks_cover_entire_text():
    text = "abcdefghij" * 30
    chunks = chunk_text(text, source_url="http://x", institution="SIAC", chunk_size=50, overlap=10)
    assert chunks[-1].char_end == len(text)
    assert chunks[0].char_start == 0


def test_source_metadata_propagated():
    chunks = chunk_text("some text here", source_url="http://example.com/report.pdf", institution="HKIAC")
    assert all(c.source_url == "http://example.com/report.pdf" for c in chunks)
    assert all(c.institution == "HKIAC" for c in chunks)


def test_invalid_chunk_size_raises():
    with pytest.raises(ValueError):
        chunk_text("text", source_url="http://x", institution="SIAC", chunk_size=10, overlap=20)


def test_whitespace_only_segments_are_skipped():
    text = "real content" + " " * 300 + "more content"
    chunks = chunk_text(text, source_url="http://x", institution="SIAC", chunk_size=100, overlap=10)
    assert all(c.text.strip() for c in chunks)
