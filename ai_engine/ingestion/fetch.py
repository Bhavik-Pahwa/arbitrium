"""Fetches a URL (PDF or HTML) and returns plain text plus metadata.

No fabrication happens here — this is pure retrieval. If a fetch fails,
that failure is returned/raised explicitly rather than papered over.
"""

import io
from dataclasses import dataclass
from datetime import datetime, timezone

import pdfplumber
import requests
from bs4 import BeautifulSoup

USER_AGENT = "ArbitriumAIEngine/1.0 (research tool; contact: project maintainer)"
TIMEOUT_SECONDS = 30


@dataclass
class FetchedDocument:
    url: str
    content_type: str  # "pdf" | "html"
    text: str
    fetched_at: str


def _extract_pdf_text(content: bytes) -> str:
    parts = []
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return "\n".join(parts)


def _extract_html_text(content: bytes) -> str:
    soup = BeautifulSoup(content, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def fetch(url: str) -> FetchedDocument:
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
    response.raise_for_status()

    content_type_header = response.headers.get("Content-Type", "")
    is_pdf = "pdf" in content_type_header.lower() or url.lower().endswith(".pdf")

    if is_pdf:
        text = _extract_pdf_text(response.content)
        content_type = "pdf"
    else:
        text = _extract_html_text(response.content)
        content_type = "html"

    return FetchedDocument(
        url=url,
        content_type=content_type,
        text=text,
        fetched_at=datetime.now(timezone.utc).isoformat(),
    )
