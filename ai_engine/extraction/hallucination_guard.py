"""Validates that a model-claimed source_excerpt actually appears in the
retrieved source text, and that the claimed numeric_value is plausibly
represented within that excerpt. This is the last line of defense against
the model inventing a citation-shaped string rather than quoting real text.

A fact that fails this check is not silently dropped by this module — the
caller decides what to do (typically: reject and log), so a failure is
still visible rather than swallowed.
"""

import re

from extraction.schemas import ExtractedFact
from ingestion.corpus_store import CorpusStore


def _normalize(text: str) -> str:
    return " ".join(text.split())


def _numeric_representations(value: float) -> list[str]:
    reps = {str(value)}
    if value == int(value):
        reps.add(str(int(value)))
        reps.add(f"{int(value):,}")
    reps.add(f"{value:,.2f}".rstrip("0").rstrip("."))
    reps.add(f"{value:,}")
    return list(reps)


def _excerpt_mentions_number(excerpt: str, value: float) -> bool:
    stripped = re.sub(r"[,\s]", "", excerpt)
    for rep in _numeric_representations(value):
        if re.sub(r"[,\s]", "", rep) in stripped:
            return True
    return False


def check_fact(fact: ExtractedFact, corpus_store: CorpusStore) -> tuple[bool, str]:
    if not fact.requires_excerpt():
        return True, "no excerpt required (not_disclosed or non-numeric fact)"

    if not fact.source_excerpt:
        return False, "numeric fact missing source_excerpt"

    source_text = corpus_store.get_source_text(fact.source_url)
    if source_text is None:
        return False, f"source_url not found in corpus: {fact.source_url}"

    if _normalize(fact.source_excerpt) not in _normalize(source_text):
        return False, "source_excerpt is not a verbatim substring of the ingested source text"

    if fact.numeric_value is not None and not _excerpt_mentions_number(
        fact.source_excerpt, fact.numeric_value
    ):
        return False, "numeric_value not found within the claimed source_excerpt"

    return True, "verified"


def filter_verified_facts(
    facts: list[ExtractedFact], corpus_store: CorpusStore
) -> tuple[list[ExtractedFact], list[dict]]:
    accepted: list[ExtractedFact] = []
    rejected: list[dict] = []

    for fact in facts:
        passed, reason = check_fact(fact, corpus_store)
        fact.hallucination_check_passed = passed
        if passed:
            accepted.append(fact)
        else:
            rejected.append({"fact": fact.model_dump(), "reason": reason})

    return accepted, rejected
