# Arbitrium — Backend

FastAPI + PostgreSQL backend implementing Iteration 1 of the Arbitrium PRD
(`../docs/project/product-requirements.md`). This pass covers the **backend only** — see
`../docs/project/implementation-checklist.md` for full scope/status and known gaps (frontend, live
rule-refresh job, replacing placeholder fee/annual-report figures with
verified numbers).

## Data honesty note

`app/seed/reference_data.py` seeds structural data (seats, institutions,
the PRD's cited rule/annual-report source URLs) plus **illustrative,
explicitly `verified=False`** fee schedules and qualitative recommendation
ratings. No case-count/fee/duration figures were fabricated as if real —
read that file's docstring before treating any seeded number as fact.

## Setup

```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate   # Windows; use `source .venv/bin/activate` on macOS/Linux
pip install -r requirements.txt
cp .env.example .env       # then edit DATABASE_URL / SECRET_KEY
```

Requires a running PostgreSQL instance matching `DATABASE_URL` in `.env`.

## Database

```bash
alembic upgrade head        # create schema
python -m app.seed.seed_db  # load seed reference data (idempotent)
```

## Run

```bash
uvicorn app.main:app --reload
```

API docs at `http://localhost:8000/docs`. Health check at `/health`.

## Test

```bash
pytest
```

Tests cover pure service logic (`cost_estimator`, `clause_generator`,
`recommendation_engine`) without requiring a live database.

## API surface

| Page (PRD)                     | Endpoints                                                                 |
|---------------------------------|----------------------------------------------------------------------------|
| Auth                             | `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me` |
| Dashboard                        | `GET /api/v1/dashboard`                                                   |
| Seat Allocation                  | `POST /api/v1/seat-allocation/upload-contract`, `POST /api/v1/seat-allocation/analyze`, `GET /api/v1/seat-allocation/{id}` |
| Live Rule Tracking & Components  | `GET /api/v1/rules`, `GET /api/v1/rules/sources`                          |
| Clause Generation                | `POST /api/v1/clauses/generate`, `GET /api/v1/clauses/{id}`, `GET /api/v1/clauses` |
| Cost and Duration Estimate       | `POST /api/v1/cost-estimate/calculate`                                    |
| (supporting)                     | `GET /api/v1/seats`, `GET /api/v1/institutions`                           |

All "analyze"/"generate"/"calculate" endpoints work for guests (no auth
header) as well as authenticated users — matching the PRD's guest vs.
authenticated dashboard split. When authenticated, results are attributed
to the user and surfaced back on `GET /api/v1/dashboard`.
