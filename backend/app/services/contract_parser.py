"""Best-effort heuristic contract intake extraction.

Not a legal-NLP system: uses regex/keyword heuristics to pre-fill the Seat
Allocation intake form from an uploaded contract. Extraction results are
always presented to the user as editable defaults, never as final data —
the intake form remains the source of truth.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

import pdfplumber
from docx import Document

CURRENCY_AMOUNT_RE = re.compile(
    r"(USD|US\$|\$|INR|Rs\.?|GBP|£|EUR|€|SGD|HKD)\s?([\d,]+(?:\.\d+)?)\s?(million|mn|crore|lakh)?",
    re.IGNORECASE,
)
GOVERNING_LAW_RE = re.compile(
    r"govern(?:ed|ing)\s+(?:by|in accordance with)\s+the\s+laws?\s+of\s+([A-Z][A-Za-z\s]+?)(?:[.,;\n]|$)",
    re.IGNORECASE,
)
PARTIES_RE = re.compile(
    r"between\s+(.+?)\s+\(.*?\)\s+and\s+(.+?)\s+\(.*?\)", re.IGNORECASE
)

CURRENCY_MULTIPLIER = {"million": 1_000_000, "mn": 1_000_000, "crore": 10_000_000, "lakh": 100_000}
CURRENCY_SYMBOL_TO_CODE = {
    "$": "USD", "US$": "USD", "USD": "USD",
    "£": "GBP", "GBP": "GBP",
    "€": "EUR", "EUR": "EUR",
    "RS.": "INR", "RS": "INR", "INR": "INR",
    "SGD": "SGD", "HKD": "HKD",
}


@dataclass
class ExtractionResult:
    parties: list[dict] = field(default_factory=list)
    scope: str | None = None
    claim_quantum: float | None = None
    claim_currency: str | None = None
    governing_law: str | None = None


def extract_text(file_path: str) -> str:
    path = Path(file_path)
    if path.suffix.lower() == ".pdf":
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text_parts.append(page.extract_text() or "")
        return "\n".join(text_parts)
    if path.suffix.lower() == ".docx":
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    raise ValueError(f"Unsupported contract file type: {path.suffix}")


def parse(file_path: str) -> ExtractionResult:
    text = extract_text(file_path)
    result = ExtractionResult()

    parties_match = PARTIES_RE.search(text)
    if parties_match:
        result.parties = [
            {"name": parties_match.group(1).strip(), "role": "Party A"},
            {"name": parties_match.group(2).strip(), "role": "Party B"},
        ]

    law_match = GOVERNING_LAW_RE.search(text)
    if law_match:
        result.governing_law = law_match.group(1).strip()

    amount_match = CURRENCY_AMOUNT_RE.search(text)
    if amount_match:
        symbol, amount_str, multiplier_word = amount_match.groups()
        amount = float(amount_str.replace(",", ""))
        if multiplier_word:
            amount *= CURRENCY_MULTIPLIER.get(multiplier_word.lower(), 1)
        result.claim_quantum = amount
        result.claim_currency = CURRENCY_SYMBOL_TO_CODE.get(symbol.upper(), symbol.upper())

    paragraphs = [p.strip() for p in text.split("\n") if len(p.strip()) > 80]
    if paragraphs:
        result.scope = paragraphs[0][:1000]

    return result
