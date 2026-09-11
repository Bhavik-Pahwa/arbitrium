# Arbitrium AI Engine

Standalone Python module that turns arbitral institutions' annual
reports/rules pages into structured, source-cited facts (case volumes by
sector/country/seat, duration, tribunal composition) via a retrieval-
augmented, tool-calling LLM agent. See `../docs/project/ai-engine-checklist.md` for the full
architecture rationale and design decisions.

Decoupled from `backend/` — see `../docs/project/ai-engine-checklist.md` design decision 2. Its own
storage (`data/corpus/`, `data/facts/facts.db`) is local to this module;
`storage/export.py` produces a JSON bundle for a human (or a follow-up
task) to load into the backend.

## Non-negotiable rules this module enforces in code, not just docs
- `core/config.py` raises at startup if `OPENROUTER_MODEL` is ever set to
  anything other than `openrouter/free`; `core/client.py` enforces the same
  at the client-construction level.
- `extraction/hallucination_guard.py` rejects any numeric fact whose
  `source_excerpt` isn't a verbatim substring of the actual ingested source
  text, or whose claimed number doesn't appear in that excerpt.

## Setup

```bash
cd ai_engine
python -m venv .venv
. .venv/Scripts/activate   # Windows
pip install -r requirements.txt
cp .env.example .env       # fill in OPENROUTER_API_KEY
```

## Usage

```bash
# 1. Ingest a source into the local corpus
python main.py ingest SIAC https://siac.org.sg/siac-rules-2025

# 2. See what's ingested
python main.py sources

# 3. Run the extraction agent against ingested + on-demand-fetched sources
python main.py extract SIAC "How many new cases did SIAC administer in its most recent annual report, and what industry sectors were they in?"

# 4. Export accepted facts to JSON
python main.py export --output data/facts/export.json
```

## Test

```bash
pytest
```

All tests run offline against a mocked `OpenRouterClient` — no API key or
network access required to validate the agent loop, chunker, corpus
retrieval, hallucination guard, or the model-lock policy.

## What "extract" actually asks the model to look for

Per the PRD's cross-border data index (SIAC, HKIAC, ICDR/AAA, LCIA) plus
MCIA: new case filings, case value/quantum, industry-sector breakdown,
party-nationality breakdown, seat statistics, sole vs. 3-member tribunal
split, emergency arbitrator filings, and average case duration — each
tagged `disclosed`/`not_disclosed` per institution per report year, never
estimated.
