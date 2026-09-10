"""Tool schemas + dispatch for the agentic loop. Deliberately small and
auditable: the model can search what's already been ingested, pull a new
source into the corpus, or list what's available — nothing broader (no
general web browsing, no arbitrary code execution).
"""

import json
from typing import Callable

from ingestion.corpus_store import CorpusStore
from ingestion.fetch import fetch

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "search_corpus",
            "description": (
                "Search previously-ingested document chunks (annual reports, rules pages) "
                "for text relevant to a query. Returns ranked chunks with source_url and "
                "exact char_start/char_end spans — quote directly from these, do not "
                "paraphrase numbers."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"},
                    "institution": {
                        "type": "string",
                        "description": "Optional institution short code filter, e.g. SIAC",
                    },
                    "top_k": {"type": "integer", "description": "Max results (default 5)"},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_source",
            "description": (
                "Fetch and ingest a new PDF or HTML source URL into the corpus so it can "
                "then be searched with search_corpus. Only call this for URLs you were "
                "explicitly given or that came from a prior tool result — never invent a URL."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {"type": "string", "description": "Source URL to fetch"},
                    "institution": {
                        "type": "string",
                        "description": "Institution short code this source belongs to, e.g. SIAC",
                    },
                },
                "required": ["url", "institution"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_ingested_sources",
            "description": "List all sources currently ingested into the corpus.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]


class ToolRegistry:
    def __init__(self, corpus_store: CorpusStore):
        self.corpus_store = corpus_store
        self._handlers: dict[str, Callable[[dict], dict]] = {
            "search_corpus": self._search_corpus,
            "fetch_source": self._fetch_source,
            "list_ingested_sources": self._list_ingested_sources,
        }

    def dispatch(self, name: str, arguments_json: str) -> str:
        try:
            arguments = json.loads(arguments_json) if arguments_json else {}
        except json.JSONDecodeError as exc:
            return json.dumps({"error": f"Invalid tool arguments JSON: {exc}"})

        handler = self._handlers.get(name)
        if handler is None:
            return json.dumps({"error": f"Unknown tool '{name}'"})

        try:
            result = handler(arguments)
        except Exception as exc:  # tool failures are surfaced to the model, not raised
            result = {"error": f"{type(exc).__name__}: {exc}"}
        return json.dumps(result)

    def _search_corpus(self, args: dict) -> dict:
        results = self.corpus_store.search(
            query=args["query"],
            top_k=args.get("top_k", 5),
            institution=args.get("institution"),
        )
        return {"results": results}

    def _fetch_source(self, args: dict) -> dict:
        document = fetch(args["url"])
        chunk_count = self.corpus_store.ingest_document(document, institution=args["institution"])
        return {
            "source_url": document.url,
            "content_type": document.content_type,
            "chunks_ingested": chunk_count,
        }

    def _list_ingested_sources(self, args: dict) -> dict:
        return {"sources": self.corpus_store.list_sources()}
