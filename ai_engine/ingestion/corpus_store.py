"""Persists ingested document chunks to disk and serves BM25 retrieval
over them. Local, deterministic, no external embedding API — keeps the
"only openrouter/free" model constraint honest by not introducing a second
hosted model for retrieval.
"""

import hashlib
import json
import re
from pathlib import Path

from rank_bm25 import BM25Plus

from ingestion.chunker import Chunk, chunk_text
from ingestion.fetch import FetchedDocument

TOKEN_RE = re.compile(r"[a-z0-9]+")

# Filtered so common connective words don't inflate BM25Plus scores for
# documents that share no substantive terms with the query (BM25Plus's delta
# keeps every shared-token score positive, so unfiltered stopwords would
# otherwise dilute ranking precision as the corpus grows).
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has",
    "in", "into", "is", "it", "of", "on", "or", "that", "the", "this", "to",
    "was", "were", "will", "with",
}


def _tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS]


def _slug(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:24]


class CorpusStore:
    def __init__(self, corpus_dir: Path):
        self.corpus_dir = corpus_dir
        self.corpus_dir.mkdir(parents=True, exist_ok=True)

    def _path_for(self, source_url: str) -> Path:
        return self.corpus_dir / f"{_slug(source_url)}.json"

    def ingest_document(self, document: FetchedDocument, institution: str) -> int:
        chunks = chunk_text(document.text, source_url=document.url, institution=institution)
        payload = {
            "source_url": document.url,
            "institution": institution,
            "content_type": document.content_type,
            "fetched_at": document.fetched_at,
            "chunks": [
                {
                    "chunk_index": c.chunk_index,
                    "char_start": c.char_start,
                    "char_end": c.char_end,
                    "text": c.text,
                }
                for c in chunks
            ],
        }
        self._path_for(document.url).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return len(chunks)

    def _load_all_chunks(self) -> list[Chunk]:
        all_chunks: list[Chunk] = []
        for path in self.corpus_dir.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            for c in data["chunks"]:
                all_chunks.append(
                    Chunk(
                        source_url=data["source_url"],
                        institution=data["institution"],
                        chunk_index=c["chunk_index"],
                        char_start=c["char_start"],
                        char_end=c["char_end"],
                        text=c["text"],
                    )
                )
        return all_chunks

    def list_sources(self) -> list[dict]:
        sources = []
        for path in self.corpus_dir.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            sources.append(
                {
                    "source_url": data["source_url"],
                    "institution": data["institution"],
                    "content_type": data["content_type"],
                    "fetched_at": data["fetched_at"],
                    "chunk_count": len(data["chunks"]),
                }
            )
        return sources

    def get_source_text(self, source_url: str) -> str | None:
        path = self._path_for(source_url)
        if not path.exists():
            return None
        data = json.loads(path.read_text(encoding="utf-8"))
        return "".join(c["text"] for c in sorted(data["chunks"], key=lambda c: c["chunk_index"]))

    def search(self, query: str, top_k: int = 5, institution: str | None = None) -> list[dict]:
        chunks = self._load_all_chunks()
        if institution:
            chunks = [c for c in chunks if c.institution.lower() == institution.lower()]
        if not chunks:
            return []

        tokenized_corpus = [_tokenize(c.text) for c in chunks]
        # BM25Plus, not BM25Okapi: classic BM25's idf term is 0 (or negative) for
        # any word appearing in >= half the documents, which is common with a
        # corpus of only a handful of ingested reports and silently zeroes out
        # otherwise-relevant matches. BM25Plus's delta term keeps scores positive
        # and rank-meaningful even for a small corpus.
        bm25 = BM25Plus(tokenized_corpus)
        scores = bm25.get_scores(_tokenize(query))

        ranked = sorted(zip(chunks, scores), key=lambda pair: pair[1], reverse=True)[:top_k]
        return [
            {
                "source_url": c.source_url,
                "institution": c.institution,
                "chunk_index": c.chunk_index,
                "char_start": c.char_start,
                "char_end": c.char_end,
                "text": c.text,
                "score": round(float(score), 4),
            }
            for c, score in ranked
            if score > 0
        ]
