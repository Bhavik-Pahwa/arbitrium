# Arbitrium AI Engine — Architecture Checklist

A standalone Python module, decoupled from `backend/`, responsible for:
turning institutional annual reports (PDF/web) into structured, source-cited
facts (case counts by sector, party nationality, seat, duration, tribunal
composition) via retrieval-augmented, tool-calling LLM extraction — feeding
the seat-suggester logic with real numbers instead of the backend's current
`verified=False` placeholders.

## Non-negotiable constraints (from the task)
- Python only.
- Separate module (`ai_engine/`), not merged into `backend/`.
- LLM calls go through the OpenAI Python SDK pointed at OpenRouter's
  OpenAI-compatible endpoint (`base_url=https://openrouter.ai/api/v1`).
- Model name is **hardcoded to `openrouter/free`** everywhere — no fallback,
  no auto-substitution if that id turns out to be wrong. A rejected model
  name is surfaced as an error, not silently swapped.
- An **agentic loop**: the model can emit tool calls, tools execute, results
  are appended to the conversation, loop continues until the model returns
  a final (non-tool-call) response or a max-iteration cap is hit.
- **RAG over PDFs and web pages** — annual reports are PDFs (per the
  backend's cited source URLs) or, for some institutions, HTML report pages.
- **Zero numeric fabrication.** Every extracted numeric fact must carry a
  verbatim source excerpt; a validation pass (`hallucination_guard`) checks
  that excerpt actually occurs in the retrieved source text before a fact is
  accepted. If a report doesn't disclose a figure, the field is recorded as
  `not_disclosed`, never estimated or interpolated.
- Ambiguous points I'm deciding unilaterally (flagged per the task's
  "choose your own path" allowance) — see "Design decisions" below.

## Design decisions (ambiguous points, resolved)
1. **Embeddings/retrieval**: no second API/model — RAG retrieval uses local
   BM25 (`rank-bm25`) over chunked source text. Keeps "only openrouter/free"
   honest (that constraint is about the *generation* model; adding a second
   hosted embedding model would quietly violate its spirit) and needs no
   extra key.
2. **Storage**: AI Engine owns its own artifact store — a local SQLite DB
   (`data/facts.db`) of `ExtractedFact` rows plus a JSON-per-source corpus
   cache (`data/corpus/`) — rather than writing into the backend's Postgres
   directly. Keeps the module genuinely separate. `storage/export.py`
   produces a JSON bundle in the shape the backend's `annual_report_stats` /
   future sector/country tables expect, for a human (or a follow-up task) to
   load in explicitly — no silent cross-module writes.
3. **Ingestion scope for this pass**: implement the general PDF+HTML
   fetch/chunk/index pipeline and wire it to the five sources already cited
   in the backend PRD data (SIAC, HKIAC, ICDR/AAA, LCIA, MCIA). A full bulk
   extraction run across every institution's full report history is a
   follow-up job, not part of standing up the engine.
4. **Tool set exposed to the model**: `search_corpus`, `fetch_source`
   (fetch+ingest a new URL on demand), `list_ingested_sources`. Kept small
   and auditable rather than a general web-browsing tool.

## 1. Module scaffold
- [x] `ai_engine/` package layout: `core/`, `ingestion/`, `extraction/`,
      `storage/`, `tests/`, `data/`
- [x] `requirements.txt`
- [x] `.env` (local, gitignored) + `.env.example`
- [x] `.gitignore`
- [x] `README.md`

## 2. Core: OpenRouter client + agentic loop
- [x] `core/config.py` — loads `OPENROUTER_API_KEY`/`OPENROUTER_MODEL`/
      `OPENROUTER_BASE_URL` from env; hard-fails fast if the model env var
      is ever set to anything other than `openrouter/free`
- [x] `core/client.py` — thin wrapper over `openai.OpenAI(base_url=...)`
      pinned to the configured model
- [x] `core/tools.py` — tool schemas (OpenAI function-calling JSON schema)
      + a `ToolRegistry` mapping name → callable
- [x] `core/agent_loop.py` — recursive/looping tool-call handler: send
      messages → if `tool_calls` present, execute each, append
      `role: tool` results, loop; else return final message. Max-iteration
      guard against runaway loops.

## 3. Ingestion (RAG corpus building)
- [x] `ingestion/fetch.py` — download a PDF or HTML URL, extract plain text
      (pdfplumber for PDF, BeautifulSoup for HTML), tag with source
      metadata (institution, url, fetched_at, content_type)
- [x] `ingestion/chunker.py` — overlapping fixed-size chunking with
      (source_url, chunk_index, char_start, char_end) metadata so any
      retrieved chunk can be traced back to an exact span of the source
- [x] `ingestion/corpus_store.py` — persists chunks to
      `data/corpus/<slug>.json`; builds a BM25 index over all ingested
      chunks for `search_corpus`

## 4. Extraction pipeline
- [x] `extraction/schemas.py` — `ExtractedFact` Pydantic model: institution,
      report_year (nullable), metric, dimension (sector/country/None),
      dimension_value, numeric_value (nullable), unit, source_url,
      source_excerpt, status (`disclosed` / `not_disclosed`)
- [x] `extraction/system_prompt.py` — the extraction instructions
      encoding the no-fabrication rule, tool-use protocol, and required
      output shape
- [x] `extraction/extractor.py` — drives `agent_loop` for a given
      institution/report target, parses the model's final JSON into
      `ExtractedFact` rows
- [x] `extraction/hallucination_guard.py` — for every fact with a
      numeric_value, verify `source_excerpt` (normalized) is actually a
      substring of the chunk text at `source_url`; reject/flag facts that
      fail this check rather than trusting the model's citation

## 5. Storage & export
- [x] `storage/fact_store.py` — SQLite-backed CRUD for `ExtractedFact`
- [x] `storage/export.py` — dumps accepted facts to a JSON bundle shaped
      for the backend's annual-report data model

## 6. CLI entrypoint
- [x] `main.py` — `python -m ai_engine.main ingest <institution>`,
      `extract <institution>`, `export`

## 7. Tests (no live API required)
- [x] `tests/test_agent_loop.py` — mocked client, verifies the loop
      executes tool calls and terminates on a final message, and that the
      max-iteration guard trips
- [x] `tests/test_chunker.py` — chunk boundaries/overlap correctness
- [x] `tests/test_corpus_store.py` — BM25 retrieval returns relevant chunks
- [x] `tests/test_hallucination_guard.py` — accepts a fact whose excerpt is
      a real substring, rejects one that isn't
- [x] `tests/test_client_model_lock.py` — client refuses to construct with
      any model string other than `openrouter/free`

## 8. Validation
- [x] `pytest` — 28/28 passing. Caught and fixed two real bugs during this
      pass:
      1. `BM25Okapi`'s classic IDF formula (`log(N-n+0.5) - log(n+0.5)`,
         no smoothing `+1`) returns exactly 0 for any term appearing in
         `n = N/2` documents — which is the normal case for a corpus that
         starts with just one or two ingested reports, silently zeroing out
         otherwise-relevant search results. Switched `corpus_store.py` to
         `BM25Plus` (positive-delta variant) and added a small stopword
         filter so common connective words don't dilute ranking once scores
         are guaranteed positive.
      2. `openai==1.51.0`'s internal httpx client construction passes a
         `proxies` kwarg that httpx>=0.28 removed, crashing client
         construction. Pinned `httpx==0.27.2` in requirements.txt (same fix
         already applied in `backend/`).
- [x] One live sanity call to OpenRouter with `model="openrouter/free"` —
      **succeeded**: key is valid, `openrouter/free` is a real, callable
      model id, `finish_reason="stop"`.
- [x] One small real end-to-end pass: `siac.org.sg/annual-reports` returned
      HTTP 403 (bot-blocked) on first attempt — reported as-is, not
      substituted silently. Switched to `icdr.org/rules_forms_fees` (also a
      PRD-cited source), which ingested cleanly (5 chunks). Ran the live
      extraction agent against it: it correctly returned `not_disclosed`
      for case-filing statistics and fee amounts (genuinely absent from that
      page) and returned real, verbatim-quoted excerpts for the facts that
      were actually present (e.g. "Construction Industry Arbitration Rules
      and Mediation Procedures – Amended and Effective March 1, 2024"), all
      passing the hallucination guard. No fabricated numbers anywhere in
      the output — see `data/facts/export.json` (gitignored, local only).

## Known gaps / next iteration
- [ ] `siac.org.sg` returns HTTP 403 to `ingestion/fetch.py`'s requests-based
      fetch (likely bot/WAF protection) — HKIAC/LCIA/ICDR fetched fine.
      Needs either a different fetch strategy (headless browser) or an
      alternate access path for SIAC sources before this pipeline can cover
      all five institutions.
- [ ] `ingestion/fetch.py`'s HTML extraction strips all markup including
      `<a href>` targets, so the model can't discover and follow a linked
      PDF report from an HTML index page on its own — annual report PDF
      URLs currently have to be supplied directly rather than discovered.
- [ ] Bulk multi-year ingestion across all five institutions' full report
      archives
- [ ] Sector/country dimension tables in the backend's Postgres schema to
      receive `storage/export.py` output (backend currently only has
      aggregate `annual_report_stats`)
- [ ] Scheduled re-ingestion job to catch new annual report publications
- [ ] Rate limiting / robots.txt compliance policy for `fetch_source` if
      ingestion scope grows beyond the five cited sources
