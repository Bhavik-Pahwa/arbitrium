"""CLI entrypoint for the AI Engine. Run with cwd=ai_engine/.

Usage:
    python main.py ingest <institution> <url>
    python main.py extract <institution> "<task description>"
    python main.py sources
    python main.py export
"""

import argparse
import sys
from pathlib import Path

from core.config import get_settings
from ingestion.corpus_store import CorpusStore
from ingestion.fetch import fetch
from storage.export import export_bundle
from storage.fact_store import FactStore


def _corpus_store() -> CorpusStore:
    return CorpusStore(get_settings().data_dir / "corpus")


def cmd_ingest(args: argparse.Namespace) -> None:
    store = _corpus_store()
    document = fetch(args.url)
    count = store.ingest_document(document, institution=args.institution)
    print(f"Ingested {count} chunks from {args.url} ({document.content_type}) for {args.institution}")


def cmd_sources(args: argparse.Namespace) -> None:
    store = _corpus_store()
    for source in store.list_sources():
        print(f"[{source['institution']}] {source['source_url']} "
              f"({source['chunk_count']} chunks, fetched {source['fetched_at']})")


def cmd_extract(args: argparse.Namespace) -> None:
    from extraction.extractor import extract  # deferred: needs API key at call time

    store = _corpus_store()
    result = extract(args.institution, args.task, store)

    print(f"Accepted facts: {len(result['accepted_facts'])}")
    for fact in result["accepted_facts"]:
        print(f"  - {fact.metric} [{fact.dimension}={fact.dimension_value}] "
              f"= {fact.numeric_value} {fact.unit or ''} ({fact.status})")
    if result["rejected_facts"]:
        print(f"Rejected facts (failed hallucination check): {len(result['rejected_facts'])}", file=sys.stderr)
        for r in result["rejected_facts"]:
            print(f"  - {r['reason']}: {r['fact']}", file=sys.stderr)

    fact_store = FactStore(get_settings().data_dir / "facts" / "facts.db")
    fact_store.save_many(result["accepted_facts"])
    fact_store.close()


def cmd_export(args: argparse.Namespace) -> None:
    fact_store = FactStore(get_settings().data_dir / "facts" / "facts.db")
    output_path = Path(args.output)
    bundle = export_bundle(fact_store, output_path)
    fact_store.close()
    total = sum(len(v) for v in bundle["institutions"].values())
    print(f"Exported {total} facts across {len(bundle['institutions'])} institutions to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="ai_engine")
    subparsers = parser.add_subparsers(required=True)

    p_ingest = subparsers.add_parser("ingest", help="Fetch and ingest a source URL")
    p_ingest.add_argument("institution")
    p_ingest.add_argument("url")
    p_ingest.set_defaults(func=cmd_ingest)

    p_sources = subparsers.add_parser("sources", help="List ingested sources")
    p_sources.set_defaults(func=cmd_sources)

    p_extract = subparsers.add_parser("extract", help="Run the extraction agent")
    p_extract.add_argument("institution")
    p_extract.add_argument("task")
    p_extract.set_defaults(func=cmd_extract)

    p_export = subparsers.add_parser("export", help="Export accepted facts to JSON")
    p_export.add_argument("--output", default="data/facts/export.json")
    p_export.set_defaults(func=cmd_export)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
